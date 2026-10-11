#!/usr/bin/env python3
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'stack.runtime.yaml'

class PrivatePreservedACLTests(unittest.TestCase):
    def script(self):
        text = SOURCE.read_text()
        body = text.split('    entrypoint:\n', 1)[1].split('    - |\n', 1)[1].split('    restart:', 1)[0]
        return '\n'.join(line[6:] for line in body.splitlines()).replace('$$', '$')

    def run_script(self, directory):
        script = self.script().replace('/etc/valkey', directory)
        script = script.replace('exec valkey-server ', 'exit 0 # valkey-server ')
        env = dict(os.environ, VALKEY_PASSWORD='public-unit-default', VALKEY_SEAFILE_PASSWORD='public-unit-seafile', VALKEY_MASTODON_PASSWORD='public-unit-mastodon')
        return subprocess.run(['sh'], input=script, text=True, capture_output=True, env=env)

    def test_existing_authored_acl_bytes_are_preserved_privately(self):
        with tempfile.TemporaryDirectory() as directory:
            acl = Path(directory, 'users.acl')
            original = b'user preserved on #public-fixture-hash ~owner:* +get\n'
            acl.write_bytes(original)
            self.assertEqual(self.run_script(directory).returncode, 0)
            self.assertEqual(acl.read_bytes(), original)
            self.assertEqual(acl.stat().st_mode & 0o777, 0o600)

    def test_fresh_declared_acl_and_symlink_refusal(self):
        with tempfile.TemporaryDirectory() as directory:
            acl = Path(directory, 'users.acl')
            self.assertEqual(self.run_script(directory).returncode, 0)
            self.assertIn('user mastodon', acl.read_text())
            self.assertEqual(acl.stat().st_mode & 0o777, 0o600)
            target = Path(directory, 'unrelated')
            target.write_text('preserved')
            acl.unlink()
            acl.symlink_to(target)
            self.assertNotEqual(self.run_script(directory).returncode, 0)
            self.assertEqual(target.read_text(), 'preserved')

    def test_private_native_cli_environment_not_auth_argv(self):
        text = SOURCE.read_text()
        self.assertIn('export REDISCLI_AUTH=', text)
        self.assertNotIn('-a "', text)

if __name__ == '__main__':
    unittest.main()

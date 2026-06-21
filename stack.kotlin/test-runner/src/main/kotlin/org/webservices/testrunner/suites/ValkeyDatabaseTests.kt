package org.webservices.testrunner.suites

import org.webservices.testrunner.framework.*

suspend fun TestRunner.valkeyDatabaseTests() = suite("Valkey Database Tests") {
test("Valkey configuration is accessible") {
        
        val valkeyEndpoint = env.endpoints.valkey
        require(valkeyEndpoint != null) { "Valkey endpoint not configured" }
        valkeyEndpoint shouldContain "valkey"
    }

    test("Valkey port is standard Redis port") {
        
        val valkeyEndpoint = env.endpoints.valkey
        require(valkeyEndpoint != null) { "Valkey not configured" }
        valkeyEndpoint shouldContain ":6379"
    }

    test("Valkey endpoint is reachable") {
        
        val valkeyEndpoint = env.endpoints.valkey
        require(valkeyEndpoint != null) { "Valkey not configured" }
        valkeyEndpoint shouldContain "valkey:6379"
    }
}

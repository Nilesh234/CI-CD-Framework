#!/bin/bash
set -e

echo "Starting Java CI pipeline..."

# Load stages configuration
STAGES=$(cat output_stages.json)

run_stage() {
    local stage=$1
    echo "$STAGES" | jq -e ".${stage}" > /dev/null
}

# Install Maven if not already available
if ! command -v mvn &> /dev/null
then
    echo "Maven not found, installing..."
    sudo apt-get update
    sudo apt-get install -y maven
fi

# Linting
if run_stage "lint"; then
    echo "Running linting (Checkstyle)..."
    mvn checkstyle:check
fi

# Static Analysis (Optional - SpotBugs or similar)
if run_stage "static_analysis"; then
    echo "Running static analysis (SpotBugs)..."
    mvn com.github.spotbugs:spotbugs-maven-plugin:spotbugs
fi

# Unit Tests
if run_stage "unit_tests"; then
    echo "Running unit tests (Maven test)..."
    mvn test
fi

# Integration Tests
if run_stage "integration_tests"; then
    echo "Running integration tests (Failsafe plugin)..."
    mvn verify
fi

# Security Scan
if run_stage "security_scan"; then
    echo "Running dependency security scans (OWASP Dependency Check)..."
    mvn org.owasp:dependency-check-maven:check
fi

# Package Artifact
if run_stage "package_artifact"; then
    echo "Packaging artifact (JAR)..."
    mvn package
    mkdir -p dist/
    cp target/*.jar dist/
fi

echo "Java CI pipeline completed successfully!"

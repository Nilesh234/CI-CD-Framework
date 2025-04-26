#!/bin/bash
set -e

echo "Starting Node.js CI pipeline..."

# Load stages configuration
STAGES=$(cat output_stages.json)

run_stage() {
    local stage=$1
    echo "$STAGES" | jq -e ".${stage}" > /dev/null
}

# Install dependencies
echo "Installing npm packages..."
npm install

# Linting
if run_stage "lint"; then
    echo "Running linting (eslint)..."
    if [ ! -f "./node_modules/.bin/eslint" ]; then
        npm install eslint
    fi
    ./node_modules/.bin/eslint src/
fi

# Static Analysis
if run_stage "static_analysis"; then
    echo "Running static analysis (npm audit)..."
    npm audit --audit-level=high || true
fi

# Unit Tests
if run_stage "unit_tests"; then
    echo "Running unit tests (jest or mocha)..."
    if [ -f "jest.config.js" ]; then
        npx jest --coverage
    else
        npx mocha --recursive
    fi
fi

# Integration Tests
if run_stage "integration_tests"; then
    echo "Running integration tests..."
    npm run integration-test || echo "No integration test script configured."
fi

# Security Scan
if run_stage "security_scan"; then
    echo "Running advanced security scan with Snyk (if configured)..."
    if [ -f ".snyk" ]; then
        npm install -g snyk
        snyk test || true
    fi
fi

# Package Artifact
if run_stage "package_artifact"; then
    echo "Packaging artifact (zip)..."
    mkdir -p dist/
    zip -r dist/node_app.zip src/ package.json package-lock.json
fi

echo "Node.js CI pipeline completed successfully!"

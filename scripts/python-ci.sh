#!/bin/bash
set -e

echo "Starting Python CI pipeline..."

# Load stages configuration
STAGES=$(cat output_stages.json)

run_stage() {
    local stage=$1
    echo "$STAGES" | jq -e ".${stage}" > /dev/null
}

# Linting
if run_stage "lint"; then
    echo "Running linting (flake8)..."
    pip install flake8
    flake8 src/
fi

# Static Analysis (Security)
if run_stage "static_analysis"; then
    echo "Running static analysis (bandit)..."
    pip install bandit
    bandit -r src/
fi

# Unit Tests
if run_stage "unit_tests"; then
    echo "Running unit tests (pytest)..."
    pip install pytest pytest-cov
    pytest tests/ --cov=src/ --cov-fail-under=80
fi

# Integration Tests
if run_stage "integration_tests"; then
    echo "Running integration tests (pytest)..."
    pytest integration_tests/
fi

# Security Scan
if run_stage "security_scan"; then
    echo "Running additional security scans (safety)..."
    pip install safety
    safety check
fi

# Package Artifact
if run_stage "package_artifact"; then
    echo "Packaging artifact..."
    mkdir -p dist/
    zip -r dist/python_app.zip src/
fi

echo "Python CI pipeline completed successfully!"

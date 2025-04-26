#!/bin/bash
set -e

# Fetch current branch or tag
CURRENT_REF=$(echo "${GITHUB_REF#refs/heads/}")
CURRENT_TAG=$(echo "${GITHUB_REF#refs/tags/}")

echo "Checking branch/tag compliance..."

# Enforce branch naming
if [[ "${GITHUB_REF}" == refs/heads/* ]]; then
  echo "Branch detected: $CURRENT_REF"

  if [[ "$CURRENT_REF" =~ ^(main|dev|staging)$ ]]; then
    echo "Valid branch name: $CURRENT_REF"
  else
    echo "Invalid branch name: $CURRENT_REF"
    echo "Allowed branches: main, dev, staging"
    exit 1
  fi

# Enforce tag semantic versioning
elif [[ "${GITHUB_REF}" == refs/tags/* ]]; then
  echo "Tag detected: $CURRENT_TAG"

  if [[ "$CURRENT_TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Valid semantic versioning tag: $CURRENT_TAG"
  else
    echo "Invalid tag format: $CURRENT_TAG"
    echo "Allowed tag format: v{MAJOR}.{MINOR}.{PATCH} (Example: v1.0.0)"
    exit 1
  fi

else
  echo "Neither branch nor tag detected properly. Failing..."
  exit 1
fi

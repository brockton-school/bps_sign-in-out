#!/bin/bash

# Get the latest Git commit hash and version tag
GIT_COMMIT=$(git rev-parse --short HEAD)
GIT_VERSION=$(git describe --tags --abbrev=0)

# Export these as environment variables to use in docker-compose
export GIT_COMMIT
export GIT_VERSION

# Run docker-compose with the build arguments
docker-compose build --build-arg GIT_COMMIT=$GIT_COMMIT --build-arg GIT_VERSION=$GIT_VERSION
docker-compose up
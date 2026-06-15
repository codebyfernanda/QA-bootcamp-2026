# 1. Base Image Selection
# Uses an official, lightweight, and minimal Python image based on Debian.
# The "-slim" variant excludes unnecessary system packages, which drastically 
# reduces the final image size and minimizes the security attack surface, making 
# it ideal for CI/CD test automation pipelines.
FROM python:3.12-slim

# 2. Working Directory Definition
# Creates and establishes "/app" as the absolute working directory inside the container.
# All subsequent instructions (like COPY, RUN, and CMD) will be executed from this path.
# This prevents cluttering the root directory of the container system.
WORKDIR /app

# 3. Dependencies Pre-copy (Cache Optimization)
# Copies only the requirements file from the host machine to the current directory inside the container.
# By isolating this step before copying the rest of the source code, we take advantage 
# of Docker's layer caching mechanism. If requirements.txt hasn't changed, Docker skips 
# the heavy installation step (Step 4) during future builds, saving valuable build time.
COPY requirements.txt .

# 4. QA Dependency Installation
# Executes the pip installer to install all specified testing frameworks (such as pytest, requests, jsonschema).
# The "--no-cache-dir" flag is a production best practice: it forces pip to delete downloaded 
# .whl files and temporary installers immediately after installation, keeping the container image ultra-lean.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Source Code Copying
# Copies the entire content of your current local directory (test suites, conftest.py, schemas) 
# into the container's working directory. 
# Note: Ensure you have a .dockerignore file configured to prevent copying local artifacts 
# like .venv/ or __pycache__ folders into this layer.
COPY . .

# 6. Default Container Command
# Defines the primary instruction that will trigger automatically whenever the container is spun up.
# Using the preferred JSON array syntax (exec form), it fires up the Pytest test runner in verbose mode (-v).
# This default behavior can easily
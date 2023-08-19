#!/bin/bash


# Set the virtual environment name
VENV_NAME="venv"

# Set the Python command if it's not in your PATH
PYTHON_CMD="python" # Modify this if your Python command is different

# Check for Python version
$PYTHON_CMD --version

# Check if virtual environment directory already exists
if [ ! -d "$VENV_NAME" ]; then
  # Create a virtual environment with detected Python version
  $PYTHON_CMD -m venv $VENV_NAME
fi

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Install dependencies from requirements.txt (if exists)
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
fi

# Run the Python script
$PYTHON_CMD run.py

# Deactivate the virtual environment
deactivate
echo "Bot has been stopped. Virtual environment has been deactivated."

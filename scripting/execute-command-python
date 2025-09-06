#!/bin/bash
#  This script sets up the necessary environment and allows the kikit_tools module to run correctly. It's required
# because of the (current) extreme fragility of the KiCad jobset execute command. Most usual path management techniques
# fail silently.

# Check required environment variables
check_var() {
    if [ -z "$1" ]; then
        echo "ERROR: $2 is not set." >&2
        exit 1
    fi
}

check_var "$IREX_KIKIT_VENV_DIR" "IREX_KIKIT_VENV_DIR"
check_var "$IREX_KIKIT_ROOT_DIR" "IREX_KIKIT_ROOT_DIR"


# Set Python path so kikit_tools can be imported
export PYTHONPATH="$IREX_KIKIT_ROOT_DIR/scripting:$PYTHONPATH"

# Activate virtual environment
. "$IREX_KIKIT_VENV_DIR/bin/activate"

# Execute Python with passed arguments
exec python "$@"

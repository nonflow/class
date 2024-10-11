#!/bin/bash

# Function to run tests
run_tests() {
    if [ "$1" = "-v" ]; then
        python -m unittest discover -v tests
    elif [ -n "$1" ]; then
        python -m unittest tests/test_"$1".py
    else
        python -m unittest discover tests
    fi
}

# Check if a specific test or verbose flag is provided
if [ $# -eq 0 ]; then
    run_tests
elif [ "$1" = "-v" ]; then
    run_tests -v
else
    run_tests "$1"
fi

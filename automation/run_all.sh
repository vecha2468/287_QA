#!/bin/bash

# Define the output log file
LOG_FILE="output.log"

# Clear the log file if it already exists
> $LOG_FILE

# Function to print headers in the log
print_header() {
    echo "==================================================" >> $LOG_FILE
    echo "Running $1..."
    echo "==================================================" >> $LOG_FILE
    echo -e "\n\nRunning $1... Check output.log for detailed output."
}

# Function to print completion message
print_completion() {
    echo -e "\n$1 executed successfully. Starting next script...\n"
}

# Run main.py and log output
print_header "main.py"
python3 main.py >> $LOG_FILE 2>&1
print_completion "main.py"

# Run my_nlp_script.py and log output
print_header "my_nlp_script.py"
python3 my_nlp_script.py >> $LOG_FILE 2>&1
print_completion "my_nlp_script.py"

# Run ReportGenerator.py and log output
print_header "ReportGenerator.py"
python3 ReportGenerator.py >> $LOG_FILE 2>&1
print_completion "ReportGenerator.py"

echo "All scripts executed successfully. Check output.log for details."

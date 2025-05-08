@echo off
SET LOG_FILE=output.log

:: Clear the log file if it exists
IF EXIST %LOG_FILE% del %LOG_FILE%

:: Function-like macro to print headers in the log
CALL :print_header "main.py"
python main.py >> %LOG_FILE% 2>&1
CALL :print_completion "main.py"

CALL :print_header "my_nlp_script.py"
python my_nlp_script.py >> %LOG_FILE% 2>&1
CALL :print_completion "my_nlp_script.py"

CALL :print_header "ReportGenerator.py"
python ReportGenerator.py >> %LOG_FILE% 2>&1
CALL :print_completion "ReportGenerator.py"

echo All scripts executed successfully. Check output.log for details.
GOTO :EOF

:print_header
echo ================================================== >> %LOG_FILE%
echo Running %1... >> %LOG_FILE%
echo ================================================== >> %LOG_FILE%
echo.
echo Running %1... Check output.log for detailed output.
GOTO :EOF

:print_completion
echo.
echo %1 executed successfully. Starting next script...
echo.
GOTO :EOF

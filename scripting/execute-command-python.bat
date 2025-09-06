@echo off
REM Equivalent to execute-command-python.sh for Windows

REM Check required environment variables
IF NOT DEFINED IREX_KIKIT_VENV_DIR (
  echo ERROR: IREX_KIKIT_VENV_DIR is not set. 1>&2
  exit /b 1
)
IF NOT DEFINED IREX_KIKIT_ROOT_DIR (
  echo ERROR: IREX_KIKIT_ROOT_DIR is not set. 1>&2
  exit /b 1
)

REM Set PYTHONPATH so kikit_tools can be imported
SET "PYTHONPATH=%IREX_KIKIT_ROOT_DIR%\scripting;%PYTHONPATH%"

REM Activate virtual environment
CALL "%IREX_KIKIT_VENV_DIR%\Scripts\activate.bat"
IF ERRORLEVEL 1 (
  echo ERROR: Failed to activate virtual environment. 1>&2
  exit /b 1
)

REM Execute Python with passed arguments
python %*
exit /b %ERRORLEVEL%

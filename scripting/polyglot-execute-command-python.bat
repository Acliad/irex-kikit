echo \" <<'BATCH_SCRIPT' >/dev/null ">NUL "\" \`" <#"
@ECHO OFF
REM ===== Batch Script Begin =====
call "%CRONOS_KIKIT_ROOT_DIR%\scripting\execute-command-python.bat" %*
exit /b %ERRORLEVEL%
REM ====== Batch Script End ======
GOTO :eof
TYPE CON >NUL
BATCH_SCRIPT
#> | Out-Null


set +o histexpand 2>/dev/null
# ===== Bash Script Begin =====
exec "$CRONOS_KIKIT_ROOT_DIR/scripting/execute-command-python.sh" "$@"
# ====== Bash Script End ======
case $- in *"i"*) cat /dev/stdin >/dev/null ;; esac
exit
#>
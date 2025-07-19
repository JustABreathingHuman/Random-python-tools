@echo off

cd %~dp0

set /a number=0

:loop

md %number%

set /a number=%number%+1

goto loop
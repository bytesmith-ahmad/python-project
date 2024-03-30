@echo off

echo Current branch:
git branch
echo Proceed?
pause

echo ======================================================================= START
git diff
echo ************************
git add .
echo ************************
git commit
echo ************************
git push
echo ======================================================================= DONE
echo.
pause

@echo off

:: find the version number in package.json and increment it
for /F "tokens=2 delims==, " %%t in ('findstr /C:"VERSION " setup.py') do (
    set v=%%~t
    for /F "tokens=3 delims=." %%t in ('echo %%~t') do (
        set v=%%~t
        set /A v+=1
    )
)
set version="0.0.%v%"


:: replace the version number in package.json
echo import setuptools>setup.bkp
echo.>>setup.bkp
echo VERSION = %version%>>setup.bkp
:: copy the file from line 3 to the end of the file avoid last line
type setup.py | more +3 >>setup.bkp


:: write the version file

::commit and push the changes
set comment=%version%
cmd /c git add .
cmd /c git commit -m %comment%
cmd /c git push
::finally publish the package on npm
cmd /c npm run build 
cmd /c npm publish 


@echo off
setlocal

REM Build Windows .exe con PyInstaller
python -m pip install --upgrade pyinstaller
pyinstaller --noconfirm --onefile --windowed --name OrologioAnalogico analog_clock_transparent.py

echo.
echo Build completata. File generato:
echo dist\OrologioAnalogico.exe
endlocal

@echo off
echo Starting Django Backend Server...
echo.

cd /d "c:\Users\DELL\Desktop\school sasa report\backend"

echo Checking if virtual environment exists...
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python...
)

echo.
echo Starting Django development server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver 0.0.0.0:8000

pause
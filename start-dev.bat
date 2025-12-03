@echo off
echo Starting ArXiv Research Hub Development Environment...
echo.

echo Installing dependencies...
call npm run setup

echo.
echo Starting backend and frontend servers...
echo Please run the following commands in separate terminals:
echo 1. Backend: cd backend && python start.py
echo 2. Frontend: cd frontend && npm start

pause
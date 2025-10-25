@echo off
echo Setting up ProjectPulse for local development...

echo.
echo Installing backend dependencies...
cd backend-service
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing backend dependencies
    pause
    exit /b 1
)

echo.
echo Backend setup complete!
echo.
echo To run the backend service:
echo   cd backend-service
echo   uvicorn app.main:app --reload
echo.
echo To run the frontend service:
echo   cd frontend-service
echo   npm install
echo   npm run dev
echo.
echo Or use Docker Compose for full stack:
echo   docker-compose up --build
echo.
pause

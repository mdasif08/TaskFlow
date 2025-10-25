#!/bin/bash

echo "Setting up ProjectPulse for local development..."

echo ""
echo "Installing backend dependencies..."
cd backend-service
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing backend dependencies"
    exit 1
fi

echo ""
echo "Backend setup complete!"
echo ""
echo "To run the backend service:"
echo "  cd backend-service"
echo "  uvicorn app.main:app --reload"
echo ""
echo "To run the frontend service:"
echo "  cd frontend-service"
echo "  npm install"
echo "  npm run dev"
echo ""
echo "Or use Docker Compose for full stack:"
echo "  docker-compose up --build"
echo ""

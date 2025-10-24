#!/bin/bash
# ----------------------------------------
# Django Run Script (Professional Edition)
# Author: Sajad Seifi Lor
# ----------------------------------------

GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}🔹 Checking virtual environment...${NC}"
if [ ! -d "env" ]; then
  echo -e "${RED}[ERROR] Virtual environment 'env' not found!${NC}"
  echo "Please create it first using: python3 -m venv env"
  exit 1
fi

echo -e "${CYAN}🔹 Activating virtual environment...${NC}"
source env/Scripts/activate

if [ $? -ne 0 ]; then
  echo -e "${RED}[ERROR] Failed to activate virtual environment.${NC}"
  exit 1
fi

read -p "Enter port (default 8000): " PORT
PORT=${PORT:-8000}

echo -e "${GREEN}🚀 Starting Django server on http://127.0.0.1:${PORT} ...${NC}"
xdg-open "http://127.0.0.1:${PORT}" >/dev/null 2>&1 &
python manage.py runserver ${PORT}

deactivate
echo -e "${YELLOW}✅ Server stopped. Virtual environment deactivated.${NC}"

@echo off
echo Configurando LashManager...

echo.
echo === Configurando Backend ===
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo === Configurando Frontend ===
cd ..\frontend
npm install

echo.
echo === Setup Completo! ===
echo.
echo Para iniciar o sistema:
echo 1. Backend: cd backend && venv\Scripts\activate && python app.py
echo 2. Frontend: cd frontend && npm run dev
echo.
echo Acesse: http://localhost:3000
echo Login: admin / admin123
pause
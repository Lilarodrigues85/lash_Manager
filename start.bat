@echo off
echo Iniciando LashManager...

echo.
echo === Inicializando Banco de Dados ===
cd backend
call venv\Scripts\activate
python init_db.py

echo.
echo === Iniciando Backend ===
start cmd /k "cd /d %cd% && venv\Scripts\activate && python app.py"

echo.
echo === Iniciando Frontend ===
cd ..\frontend
start cmd /k "cd /d %cd% && npm run dev"

echo.
echo Sistema iniciado!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo Login: admin / admin123
pause
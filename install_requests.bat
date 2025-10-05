@echo off
echo Instalando requests...
cd backend
call venv\Scripts\activate
pip install requests==2.31.0
echo Requests instalado com sucesso!
pause
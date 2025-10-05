@echo off
echo Fazendo deploy para GitHub...

echo.
echo === Inicializando Git ===
git init

echo.
echo === Adicionando arquivos ===
git add .

echo.
echo === Fazendo commit inicial ===
git commit -m "🚀 Initial commit: LashManager - Sistema completo de gestão para salão"

echo.
echo === Adicionando repositório remoto ===
git remote add origin https://github.com/Lilarodrigues85/lash_Manager.git

echo.
echo === Enviando para GitHub ===
git branch -M main
git push -u origin main

echo.
echo ✅ Deploy concluído!
echo Repositório: https://github.com/Lilarodrigues85/lash_Manager.git
pause
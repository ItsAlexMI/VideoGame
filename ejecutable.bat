@echo off

REM Crear y activar el entorno virtual
python -m venv venv
call venv\Scripts\activate

REM Instalar las dependencias desde requirements.txt
pip install -r requirements.txt

REM Ejecutar el código Python principal
python menu.py

REM Desactivar el entorno virtual al finalizar
deactivate

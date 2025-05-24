#!/bin/bash

echo "--- BUILD START ---"

# Actualizar pip (buena práctica)
echo ">>> Upgrading pip..."
pip install --upgrade pip

# Instalar dependencias
echo ">>> Installing dependencies..."
pip install -r requirements.txt

# Ejecutar collectstatic (usando 'python' directamente)
echo ">>> Running collectstatic..."
python manage.py collectstatic --noinput --clear

echo "--- BUILD END ---"
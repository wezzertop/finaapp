#!/bin/bash

echo "--- BUILD START ---"

# Instalar dependencias
echo ">>> Installing dependencies..."
python3.9 -m pip install -r requirements.txt

# Ejecutar collectstatic
echo ">>> Running collectstatic..."
python3.9 manage.py collectstatic --noinput --clear

echo "--- BUILD END ---"
## Paso1: Instalar entorno virtual !DENTRO DE LA CARPETA¡

virtualenv -p python3 .env

o

python3 -m venv .env

## Paso2: Activacion del entorno virtual

.env/bin/activate

o

source .env/bin/activate

## Paso3: Instalar dependencias

pip3 install -r requieriments.txt

## Actualizar pip3

python -m pip3 install --upgrade pip

## Desactivar el entorno virtual

deactivate .env

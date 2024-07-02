# system-carpet

## Instalación

Para instalar y ejecutar este proyecto, sigue los siguientes pasos:

1. Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/Kurai2610/system-carpet
```

2. Navega al directorio del proyecto:

```bash
cd system-carpet
```

3. Asegúrate de estar en el directorio raíz del proyecto y luego navega a la carpeta `server` donde se encuentra el archivo `requirements.txt`:

```bash
cd server
```

4. Crea un entorno virtual para el proyecto:

```bash
python -m venv venv
```

5. Activa el entorno virtual:

- En Windows:

```bash
.\venv\Scripts\activate
```

- En Unix o MacOS:

```bash
source venv/bin/activate
```

6. Instala las dependencias del proyecto utilizando `pip`:

```bash
pip install -r requirements.txt
```

7. Copia el archivo `.env.example` a un nuevo archivo llamado `.env` y modifica las variables de entorno según sea necesario para tu configuración local:

- En Windows:

```bash
copy .env.example .env
```

- En Unix o MacOS:

```bash
cp .env.example .env
```

8. Realiza las migraciones necesarias para configurar la base de datos de Django:

```bash
python manage.py makemigrations
python manage.py migrate
```

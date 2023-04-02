# Backend APIs

This repo contains backend REST API for Smart Waste Segregator and Route Planner.

## Installation

- clone/download this repo

  ```bash
  git clone https://github.com/SmartWasteSegregatorAndRoutePlanner/Backend-APIs.git
  ```

- Change directory

  ```bash
  cd Backend-APIs
  ```

- Install requirements
  
  - Install [Poetry](https://python-poetry.org/docs/)
  
  - Install virtualenv
  
    ```bash
    python -m pip install virtualenv
    ```

  - Create Virtual env
  
    ```bash
    python -m virtualenv env
    ```

- Install dependencies

  ```bash
  poetry install
  ```

- Create Migrations

  ```bash
  python manage.py makemigrations
  ```

- Migrate DB

  ```bash
  python manage.py migrate
  ```
  
- Collect Static Files

  ```bash
  python manage.py collectstatic
  ```

- Start Web Application

  ```bash
  python manage.py runserver 0.0.0.0:8000
  ```

  > **Note**: Allow Port `8000` through firewall.

## Common Installation Error Fix Cases on Windows

- Check python installed arch version using

  ```python
  import struct
  print(struct.calcsize("P") * 8)
  ```

- [Fiona](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona) and [GDAL](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal) needs to be installed manually using pre-complied wheel package

  ```bash
  python -m pip install <path-to-wheel-file>
  ```

  > Note: Check python version 3.x and cpu arch then download wheel file accordingly

# Backend APIs

This repo contains backend REST API for Smart Waste Segregator and Route Planner.

## Prerequisites

### AWS 

- Create new user for AWS Rekognition service from IAM dashboard

- Create new policy with below JSON rules

  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualRecognitionAccess",
            "Effect": "Allow",
            "Action": [
                "rekognition:DetectLabels"
            ],
            "Resource": "*"
        }
    ]
  }
  ```

- Create programmatic access keys for the user

- Update access keys in `.env` file

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

- Generate DJANGO_SECRET_KEY using below command:

  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key());"
  ```

- Update `.env` file

  ```bash
  DJANGO_SECRET_KEY=l#kcn**xhq(mux@h4w_+nk1n($y2krhgoo9mab5ur^ebgh8y(6
  DEBUG=False
  ALLOWED_HOSTS=*
  AWS_ACCESS_KEY_ID=your-aws-access-key-id
  AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
  AWS_DEFAULT_REGION=your-aws-region
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

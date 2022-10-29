# Backend APIs

This repo contains backend APIs for Smart Waste Segregator and Route Planner

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

  ```bash
  python -m pip install -r requirements
  ```

- Start Web Application

  ```bash
  python main.py
  ```

## Installation Error Cases for Windows

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

## Run During Development

- Start project with devtools

  ```bash
  adev runserver .
  ```

## Running with Normal Configuration

```bash
python main.py
```

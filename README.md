# MLR-WSC-File-Exporter
[![Build Status](https://travis-ci.org/USGS-CIDA/MLR-WSC-File-Exporter.svg?branch=master)](https://travis-ci.org/USGS-CIDA/MLR-WSC-File-Exporter)
[![Coverage Status](https://coveralls.io/repos/github/USGS-CIDA/MLR-WSC-File-Exporter/badge.svg?branch=master)](https://coveralls.io/github/USGS-CIDA/MLR-WSC-File-Exporter?branch=master)

Provides services which take an MLR Legacy location and write a MLR Legacy transaction file to a directory. The
directory can be specified with the environment variable, EXPORT_DIRECTORY, or by providing a alternative configuration file
in .env. If neither are provided, the file will be written to the project's home directory.

This project has been built and tested with python 3.6.x. To build the project locally you will need
python 3 and virtualenv installed.
```bash
% virtualenv --python=python3 env
% env/bin/pip install -r requirements.txt
```
To run the tests:
```bash
env/bin/python -m unittest
```

To run the application locally execute the following:
```bash
% env/bin/python app.py
```

The swagger documentation can then be accessed at http://127.0.0.1:5000/api

The 
Default configuration variables can be overridden be creating a .env file. For instance, to turn debug on and to specify
a location to write the exported files you will want to create an .env with the following:
```python
DEBUG = True
EXPORT_DIRECTORY='/path/to/where/you/want/export/files'
```
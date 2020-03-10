# MLR-WSC-File-Exporter

[![Build Status](https://travis-ci.org/USGS-CIDA/MLR-WSC-File-Exporter.svg?branch=master)](https://travis-ci.org/USGS-CIDA/MLR-WSC-File-Exporter)
[![Coverage Status](https://coveralls.io/repos/github/USGS-CIDA/MLR-WSC-File-Exporter/badge.svg?branch=master)](https://coveralls.io/github/USGS-CIDA/MLR-WSC-File-Exporter?branch=master)

## Service Description

This service is part of the MLR microservices and is responsible for generating single-location transaction files and uploading those files into a specified S3 bucket to be processed by the MLR Legacy System side of the application and applied to the Legacy Host databases. More information about the whole MLR export process and why we generate and send files to legacy hosts (as well as how the process works after the file is uploaded to S3) can be found in the MLR project documentation. This service represents the end of the scope of the Cloud-based MLR microservices, and what happens to these files after they're uploaded to S3 is completely out of the control of the MLR services (and fully in the control of the MLR Legacy System).

This service creates a single transaction file for each transaction processed in a DDot file (meaning each location added or updated). That means that this service is called multiple times for a single DDot file: once for each transaction within the uploaded DDot file. The transaction file format was decided upon jointly between the MLR Services team and the MLR Legacy System team and is documented in the MLR project documentation.

This service expects a JSON document containing the _FULL_ set of data for a single location to be sent to it in the request. We expect the _FULL_ set of data for a location to be sent rather than just the fields that were changed or updated because of the way that the MLR Legacy System was implemented and to simplify the export process overall. This requirement allows us to use the same export method for sending changes to the Legacy Hosts _and_ for sending a specific location from MLR to all of the Legacy Hosts that may not have already had that site locally in their system.

Transaction files are named in a special format that allows the MLR Legacy System to properly order and process the files and apply the changes to the correct corresponding locations in the Host databases. This format is: `mlr.[agency code].[site number].[updated date/time]`. The transformation from the location JSON received from the MLR Legacy CRU service and the transaction file format includes mapping the location fields names from the names used in MLR to the corresponding column names used in the legacy Host databases. This field-to-column mapping is stored in the `export_utils.py` file. After the field names are properly transformed they are printed out to the export file using the proper formatting.

Once the transaction file has been constructed this service then uses the Python AWS Boto client to upload the file into an S3 bucket configured by the application configuration file (or corresponding system environment variables). The relevant configuration properties can be viewed in the `config.py` file.

Specific details about the API methods of this service, including the request and response formats, can be seen in the service Swagger API documentation.

## Building and Running

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

The test output (for success) looks like:

```bash
$ env/bin/python -m unittest
............[2018-11-19 10:54:17,956] ERROR in services: An error occurred while attempting to upload the file to S3:
.[2018-11-19 10:54:17,960] ERROR in services: An error occurred while attempting to upload the file to S3: Parameter validation failed:
Some validation error
.[2018-11-19 10:54:17,963] ERROR in services: An error occurred while attempting to upload the file to S3:
......[2018-11-19 10:54:17,993] ERROR in services: An error occurred while attempting to upload the file to S3:
.[2018-11-19 10:54:17,996] ERROR in services: An error occurred while attempting to upload the file to S3: Parameter validation failed:
Some validation error
.[2018-11-19 10:54:18,005] ERROR in services: An error occurred while attempting to upload the file to S3:
.
----------------------------------------------------------------------
Ran 23 tests in 0.898s
OK
```

To run the application locally execute the following:

```bash
% env/bin/python app.py
```

The swagger documentation can then be accessed at <http://127.0.0.1:5000/api> (when running locally using the above command).

Default configuration variables can be overridden be creating a .env file. For instance, to turn debug on you will want to create an .env with the following:

```python
DEBUG = True
```

For local development, you will need to provide a JWT token to the service. This can be done through the Swagger
documents by clicking the Authorize button and entering 'Bearer your.jwt.token'.

You can use a valid JWT token generated by another service. You will need to set it's JWT_PUBLIC_KEY to the public key
used to generate the token, as well as the JWT_DECODE_AUDIENCE (if any) and the JWT_ALGORITHM (if different than RS256).
If you don't want to verify the cert on this service, set AUTH_CERT_PATH to False.

Alternatively, you can generate your own token by using the python package jwt. In the python interpreter, do the following

```python
import jwt
jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret', algorithm='HS256')
```

The output of this command will be the token that you can use. You will need to set JWT_SECRET_KEY to 'secret' in your local .env file.
See <http://flask-jwt-simple.readthedocs.io/en/latest/options.html> for the other options that you can use.

Since this service requires authentication, you will also need to set AUTHORIZED_ROLES in your .env file to whatever you use to
generate the token.

## Running with Docker

This application can also be run locally using the docker container built during the build process, though this does not allow the application to be run in debug mode. The included `docker-compose` file has 2 profiles to choose from when running the application locally:

1. mlr-wsc-file-exporter: This is the default profile which runs the application as it would be in our cloud environment. This is not recommended for local development as it makes configuring connections to other services running locally on your machine more difficult.

2. mlr-wsc-file-exporter-local-dev: This is the profile which runs the application as it would be in the mlr-local-dev project, and is configured to make it easy to replace the mlr-wsc-file-exporter instance in the local-dev project with this instance. It is run the same as the `mlr-wsc-file-exporter` profile, except it uses the docker host network driver.

### Setting up SSL

This application is configured to run over HTTPS and thus requires SSL certificates to be setup before it can be run via Docker. When running this container alone and not with an MLR Local Dev setup SSL certificates can be configured easily by simply running the included `create_keys.sh` script in the `docker/certificates` directory.

When intending to run this application alongside other MLR service running from the MLR Local Dev project you should use the certificate files generated by the MLR Local Dev project. This is important because in order for the MLR Local Dev services to connect to this service they must trust the certificate it is serving, which is most easily accomplished locally by using the same certificate for SSL among all of the MLR services.

In addition to its own SSL certs, this service must also be able to connect to a running Water Auth server locally, and thus must trust the SSL certificate being served by Water Auth. This can be accomplished by copy-pasting the .crt file that Water Auth is serving into the `docker/certificates/import_certs` folder of this project. Any .crt file put into the `import_certs` directory will be loaded into the certificate store used by Python within the container and trusted by the application.

When using MLR Local Dev this means copying the certificates that MLR Local Dev generates into 2 places in this project:

1. `docker/certificates` to be used as the SSL certs served by this service

2. `docker/certificates/import_certs` to have this service trust other services serving the MLR Local Dev SSL certs

### Building Changes

To build and run the application after completing the above steps you can run: `docker-compose up --build {profile}`, replacing `{profile}` with one of the options listed above.

The swagger documentation can then be accessed at <http://127.0.0.1:6024/api>

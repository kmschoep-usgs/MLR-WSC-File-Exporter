# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html). (Patch version X.Y.0 is implied if not specified.)

## UNRELEASED

### Added
- Added a configuration param to disable uploading created export files to S3 (done to support integration testing)

## [0.6.0] - 2018-08-23

### Updated
- isuftin@usgs.gov - Updated the version constraint for pyca/cryptography due to
CVE https://nvd.nist.gov/vuln/detail/CVE-2018-10903

### Added
- Dockerfile Healthcheck

### Removed
- Dockerfile
- Dockerfile-DOI
- gunicorn_config.py

## [0.5.0] - 2017-11-20
### Added
- GET endpoint /version to show the current version and artifact name
- Authorization for /file_export/add and /file_export/update
- HTTPS Support

## [0.4.0] - 2017-11-01

### Changed
- Trim trailing spaces from siteNumber when used to construct the file name.

## [0.3.0] - 2017-10-18

### Added
- Write the transaction file to AWS S3 bucket.

## 0.2.0 - 2017-10-04

### Added
- POST endpoint /file_export/add which creates an add transaction file for the location in the payload.
- POST endpoint /file_export/update which creates an update transaction file for the location in the payload.
- Swagger docs endpoint /api

[Unreleased]: https://github.com/USGS-CIDA/MLR-WSC-File-Exporter/compare/MLR-WSC-File-Exporter-0.5.0...master
[0.5.0]: https://github.com/USGS-CIDA/MLR-WSC-File-Exporter/compare/MLR-WSC-File-Exporter-0.4.0...MLR-WSC-File-Exporter-0.5.0
[0.4.0]: https://github.com/USGS-CIDA/MLR-WSC-File-Exporter/compare/MLR-WSC-File-Exporter-0.3.0...MLR-WSC-File-Exporter-0.4.0
[0.3.0]: https://github.com/USGS-CIDA/MLR-WSC-File-Exporter/compare/MLR-WSC-File-Exporter-0.2.0...MLR-WSC-File-Exporter-0.3.0

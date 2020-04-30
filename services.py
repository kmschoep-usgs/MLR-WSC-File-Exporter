from io import BytesIO
import pkg_resources
import logging

from botocore.exceptions import ParamValidationError
from flask import request
from flask_restplus import Api, Resource, fields

from app import application
from export_utils import write_transaction, transaction_file_name, upload_to_s3
from flask_restplus_jwt import JWTRestplusManager, jwt_role_required

# This will add the Authorize button to the swagger docs
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(application,
          title='MLR WSC File Exporter',
          description='Provides a service whose payload is a JSON legacy location object and writes out a MLR legacy output file',
          default='WSC File Export',
          doc='/api',
          authorizations=authorizations
          )

# Setup the Flask-JWT-Simple extension
jwt = JWTRestplusManager(api, application)

location_model = api.model('LocationModel', {
    "agencyCode": fields.String,
    "agencyUseCode": fields.String,
    "altitude": fields.String(),
    "altitudeAccuracyValue": fields.String(),
    "altitudeDatumCode": fields.String(),
    "altitudeMethodCode": fields.String(),
    "aquiferCode": fields.String(),
    "aquiferTypeCode": fields.String(),
    "basinCode": fields.String(),
    "contributingDrainageArea": fields.String(),
    "coordinateAccuracyCode": fields.String(),
    "coordinateDatumCode": fields.String(),
    "coordinateMethodCode": fields.String(),
    "countryCode": fields.String(),
    "countyCode": fields.String(),
    "created": fields.String(),
    "createdBy": fields.String(),
    "dataReliabilityCode": fields.String(),
    "dataTypesCode": fields.String(),
    "daylightSavingsTimeFlag": fields.String(),
    "decimalLatitude": fields.Integer(),
    "decimalLongitude": fields.Integer(),
    "districtCode": fields.String(),
    "drainageArea": fields.String(),
    "firstConstructionDate": fields.String(),
    "gwFileCode": fields.String(),
    "holeDepth": fields.String(),
    "hydrologicUnitCode": fields.String(),
    "id": fields.Integer(),
    "instrumentsCode": fields.String(),
    "landNet": fields.String(),
    "latitude": fields.String(),
    "longitude": fields.String(),
    "mapName": fields.String(),
    "mapScale": fields.String(),
    "minorCivilDivisionCode": fields.String(),
    "nationalAquiferCode": fields.String(),
    "nationalWaterUseCode": fields.String(),
    "primaryUseOfSite": fields.String(),
    "primaryUseOfWaterCode": fields.String(),
    "projectNumber": fields.String(),
    "remarks": fields.String(),
    "secondaryUseOfSite": fields.String(),
    "secondaryUseOfWaterCode": fields.String(),
    "siteEstablishmentDate": fields.String(),
    "siteNumber": fields.String(),
    "siteTypeCode": fields.String(),
    "siteWebReadyCode": fields.String(),
    "sourceOfDepthCode": fields.String(),
    "stateFipsCode": fields.String(),
    "stationIx": fields.String(),
    "stationName": fields.String(),
    "tertiaryUseOfSiteCode": fields.String(),
    "tertiaryUseOfWaterCode": fields.String(),
    "timeZoneCode": fields.String(),
    "topographicCode": fields.String(),
    "updated": fields.String(),
    "updatedBy": fields.String(),
    "wellDepth": fields.String()
})

location_change_model = api.model('LocationChangeModel', {
    "agencyCode": fields.String(),
    "siteNumber": fields.String(),
    "newAgencyCode": fields.String(),
    "newSiteNumber": fields.String(),
    "requesterName": fields.String(),
    "updated": fields.String(),
    "reasonText": fields.String()
})

expected_keys = set(iter(location_model.keys()))

expected_change_keys = set(iter(location_change_model.keys()))

def _missing_keys(json_data, transaction_type):
    """
    :param dict json_data:
    :return: list of strings - missing keys
    """
    request_keys = set(iter(json_data.keys()))
    if transaction_type == "Change": 
        return expected_change_keys.difference(request_keys)
    else:
        return expected_keys.difference(request_keys)


def _process_post(location, transaction_type=''):
    """
    :param dict location:
    :param str transaction_type: Will be assigned to the 'trans_type' field in the exported file
    :return: tuple (response_data, response_status)
    """
    missing_keys = _missing_keys(location, transaction_type)
    if missing_keys:
        return {
           'error_message': 'Missing keys: {0}'.format(', '.join(missing_keys))
        }, 400

    else:
        file_name = transaction_file_name(location)
        output_fd = BytesIO()
        s3_bucket = application.config['S3_BUCKET']
        aws_region = application.config['AWS_REGION']
        endpoint = application.config['S3_ENDPOINT_URL']
        destination_key = 'transactions/{0}'.format(file_name)
        write_transaction(output_fd, location, transaction_type=transaction_type)
        output_fd.seek(0)
        try:
            upload_to_s3(output_fd, destination_key, s3_bucket, aws_region, endpoint)
        except (OSError, ValueError, ParamValidationError) as err:
            application.logger.error("An error occurred while attempting to upload the file to S3: " + str(err))
            return {'error_message':'Unable to write the file to S3.'}, 500
        else:
            return 'File written to s3://{0}/{1}'.format(s3_bucket, destination_key), 200


@api.route('/file_export/add')
class AddFileExporter(Resource):

    @api.response(200, "Successfully wrote transaction file")
    @api.response(400, "Bad request")
    @api.response(401, 'Not authorized')
    @api.response(500, "Unable to write the file")
    @api.doc(security='apikey')
    @api.expect(location_model)
    @jwt_role_required(application.config['AUTHORIZED_ROLES'])
    def post(self):
        return _process_post(request.get_json(), transaction_type='Create')


@api.route('/file_export/update')
class UpdateFileExporter(Resource):

    @api.response(200, "Successfully wrote transaction file")
    @api.response(400, "Bad request")
    @api.response(401, 'Not authorized')
    @api.response(500, "Unable to write the file")
    @api.doc(security='apikey')
    @api.expect(location_model)
    @jwt_role_required(application.config['AUTHORIZED_ROLES'])
    def post(self):
        return _process_post(request.get_json(), transaction_type='Update')

@api.route('/file_export/change')
class ChangeFileExporter(Resource):

    @api.response(200, "Successfully wrote transaction file")
    @api.response(400, "Bad request")
    @api.response(401, 'Not authorized')
    @api.response(500, "Unable to write the file")
    @api.doc(security='apikey')
    @api.expect(location_change_model)
    @jwt_role_required(application.config['AUTHORIZED_ROLES'])
    def post(self):
        return _process_post(request.get_json(), transaction_type='Change')

version_model = api.model('VersionModel', {
    'version': fields.String,
    'artifact': fields.String
})

@api.route('/version')
class Version(Resource):

    @api.response(200, 'Success', version_model)
    def get(self):
        try:
            distribution = pkg_resources.get_distribution('usgs_wma_mlr_wsc_file_exporter')
        except pkg_resources.DistributionNotFound:
            resp = {
                "version": "local_development",
                "artifact": None
            }
        else:
            resp = {
                "version": distribution.version,
                "artifact": distribution.project_name
            }
        return resp

@api.errorhandler
def default_error_handler(error):
    '''Default error handler'''
    return {'error_message': str(error)}, getattr(error, 'code', 500)
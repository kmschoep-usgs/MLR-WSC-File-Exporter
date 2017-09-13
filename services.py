from io import StringIO
import os

from flask import request
from flask_restplus import Api, Resource, fields, marshal, reqparse

from app import application
from export_utils import write_transaction, transaction_file_name

api = Api(application,
          title='MLR WSC File Exporter',
          description='Provides a service whose payload is a JSON legacy location object and writes out a MLR legacy output file',
          default='WSC File Export',
          doc='/api')

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

expected_keys = set(iter(location_model.keys()))

def _missing_keys(json_data):
    '''

    :param dict json_data:
    :return: list of strings - missing keys
    '''
    request_keys = set(iter(json_data.keys()))
    return expected_keys.difference(request_keys)


def _get_post_response(location, transaction_type=''):
    missing_keys = _missing_keys(location)
    if missing_keys:
        return {
           'error_message': 'Missing keys: {0}'.format(', '.join(missing_keys))
       }, 400

    else:
        file_name = transaction_file_name(location)
        output_fd = open(os.path.join(application.config['EXPORT_DIRECTORY'], file_name), 'w')
        write_transaction(output_fd, location, transaction_type=transaction_type)
        output_fd.close()
        return None, 200

@api.route('/file_export/add')
class AddFileExporter(Resource):

    @api.response(200, "Successfully wrote transaction file")
    @api.response(400, "Bad request")
    @api.response(500, "Unable to write the file")
    @api.expect(location_model)
    def post(self):
        return _get_post_response(request.get_json(), transaction_type='Create')


@api.route('/file_export/update')
class UpdateFileExporter(Resource):

    @api.response(200, "Successfully wrote transaction file")
    @api.response(400, "Bad request")
    @api.response(500, "Unable to write the file")
    @api.expect(location_model)
    def post(self):
        return _get_post_response(request.get_json(), transaction_type='Update')

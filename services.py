
from flask import request
from flask_restplus import Api, Resource, fields, marshal, reqparse

from app import application

api = Api(application,
          title='MLR WSC File Exporter',
          description='Provides a service whose payload is a JSON legacy location object and writes out a MLR legacy output file',
          default='WSC File Export',
          doc='/api')

location_model = api.model('LocationModel', {
    "agencyCode": fields.String(required=True),
    "agencyUseCode": fields.String(required=True),
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
    "decimalLatitude": fields.String(),
    "decimalLongitude": fields.String(),
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

def valid_payload():
    '''
    Determines if the payload has the expected keys
    :return: bool
    '''
    request_keys = set(iter(request.get_json().keys()))
    return len(expected_keys.difference(request_keys)) == 0


@api.route('/file_export/add')
class AddFileExporter(Resource):

    @api.expect(location_model)
    def post(self):
        data = request.get_json()
        if valid_payload:
            return 'Not yet implemented', 200
        else:
            return {
                'error_message':'Not all keys where found'
            }, 400

@api.route('/file_export/update')
class UpdateFileExporter(Resource):

    @api.expect(location_model)
    def post(self):
        return 'Not yet implemented', 400
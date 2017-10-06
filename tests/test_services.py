import json
from unittest import TestCase, mock

import app


@mock.patch('services.write_transaction')
@mock.patch('builtins.open', new_callable=mock.mock_open)
class AddFileExportTestCase(TestCase):
    def setUp(self):
        app.application.testing = True
        app.application.config['EXPORT_DIRECTORY'] = '/tmp'
        self.app_client = app.application.test_client()

        self.location = {
            'id': 1234,
            'agencyCode': 'USGS ',
            "siteNumber": "123456789012345",
            "stationName": "This station name ",
            "stationIx": "station_ix",
            "latitude": "           ",
            "longitude": "            ",
            "decimalLatitude": None,
            "decimalLongitude": None,
            "coordinateMethodCode": " ",
            "coordinateAccuracyCode": " ",
            "coordinateDatumCode": "          ",
            "districtCode": "WIS",
            "landNet": " ",
            "mapName": "Map Name",
            "countryCode": "US",
            "stateFipsCode": "55",
            "countyCode": "121",
            "mapScale": "       ",
            "altitude": "        ",
            "altitudeMethodCode": " ",
            "altitudeAccuracyValue": "   ",
            "altitudeDatumCode": "          ",
            "hydrologicUnitCode": "07010204",
            "agencyUseCode": "Y",
            "basinCode": "  ",
            "siteTypeCode": "well",
            "topographicCode": " ",
            "dataTypesCode": "                              ",
            "instrumentsCode": "instruments_cd",
            "remarks": "Remarks",
            "siteEstablishmentDate": "        ",
            "drainageArea": "        ",
            "contributingDrainageArea": "        ",
            "timeZoneCode": "UTC   ",
            "daylightSavingsTimeFlag": "N",
            "gwFileCode": "                              ",
            "firstConstructionDate": "        ",
            "dataReliabilityCode": " ",
            "aquiferCode": "        ",
            "nationalAquiferCode": "          ",
            "primaryUseOfSite": "A",
            "secondaryUseOfSite": " ",
            "tertiaryUseOfSiteCode": " ",
            "primaryUseOfWaterCode": "W",
            "secondaryUseOfWaterCode": " ",
            "tertiaryUseOfWaterCode": " ",
            "nationalWaterUseCode": "  ",
            "aquiferTypeCode": "X",
            "wellDepth": "        ",
            "holeDepth": "        ",
            "sourceOfDepthCode": " ",
            "projectNumber": "123456789012",
            "siteWebReadyCode": "N",
            "createdBy": "asmith  ",
            "created": "20171101144535",
            "updatedBy": "bjones  ",
            "updated": "20171214120244",
            "minorCivilDivisionCode": None
        }

    def test_good_location(self, mopen, mtransaction):
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        mopen.assert_called_with('/tmp/mlr.filename', 'w')
        self.assertEqual(mtransaction.call_args[0][1], self.location)
        self.assertEqual(mtransaction.call_args[1].get('transaction_type'), 'Create')

    def test_location_with_missing_keys(self, mopen, mtransaction):
        del self.location['wellDepth']
        del self.location['holeDepth']
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 400)
        resp_data = json.loads(response.data)

    def test_unable_to_write_file(self, mopen, mtransaction):
        mopen.side_effect = IOError
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 500)


@mock.patch('services.write_transaction')
@mock.patch('builtins.open', new_callable=mock.mock_open)
class UpdateFileExportTestCase(TestCase):
    def setUp(self):
        app.application.testing = True
        app.application.config['EXPORT_DIRECTORY'] = '/tmp'
        self.app_client = app.application.test_client()

        self.location = {
            'id': 1234,
            'agencyCode': 'USGS ',
            "siteNumber": "123456789012345",
            "stationName": "This station name ",
            "stationIx": "station_ix",
            "latitude": "           ",
            "longitude": "            ",
            "decimalLatitude": None,
            "decimalLongitude": None,
            "coordinateMethodCode": " ",
            "coordinateAccuracyCode": " ",
            "coordinateDatumCode": "          ",
            "districtCode": "WIS",
            "landNet": " ",
            "mapName": "Map Name",
            "countryCode": "US",
            "stateFipsCode": "55",
            "countyCode": "121",
            "mapScale": "       ",
            "altitude": "        ",
            "altitudeMethodCode": " ",
            "altitudeAccuracyValue": "   ",
            "altitudeDatumCode": "          ",
            "hydrologicUnitCode": "07010204",
            "agencyUseCode": "Y",
            "basinCode": "  ",
            "siteTypeCode": "well",
            "topographicCode": " ",
            "dataTypesCode": "                              ",
            "instrumentsCode": "instruments_cd",
            "remarks": "Remarks",
            "siteEstablishmentDate": "        ",
            "drainageArea": "        ",
            "contributingDrainageArea": "        ",
            "timeZoneCode": "UTC   ",
            "daylightSavingsTimeFlag": "N",
            "gwFileCode": "                              ",
            "firstConstructionDate": "        ",
            "dataReliabilityCode": " ",
            "aquiferCode": "        ",
            "nationalAquiferCode": "          ",
            "primaryUseOfSite": "A",
            "secondaryUseOfSite": " ",
            "tertiaryUseOfSiteCode": " ",
            "primaryUseOfWaterCode": "W",
            "secondaryUseOfWaterCode": " ",
            "tertiaryUseOfWaterCode": " ",
            "nationalWaterUseCode": "  ",
            "aquiferTypeCode": "X",
            "wellDepth": "        ",
            "holeDepth": "        ",
            "sourceOfDepthCode": " ",
            "projectNumber": "123456789012",
            "siteWebReadyCode": "N",
            "createdBy": "asmith  ",
            "created": "20171101144535",
            "updatedBy": "bjones  ",
            "updated": "20171214120244",
            "minorCivilDivisionCode": None
        }

    def test_good_location(self, mopen, mtransaction):
        response = self.app_client.post('/file_export/update',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        mopen.assert_called_with('/tmp/mlr.filename', 'w')
        self.assertEqual(mtransaction.call_args[0][1], self.location)
        self.assertEqual(mtransaction.call_args[1].get('transaction_type'), 'Update')

    def test_location_with_missing_keys(self, mopen, mtransaction):
        del self.location['wellDepth']
        del self.location['holeDepth']
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 400)
        resp_data = json.loads(response.data)

    def test_unable_to_write_file(self, mopen, mtransaction):
        mopen.side_effect = IOError
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 500)
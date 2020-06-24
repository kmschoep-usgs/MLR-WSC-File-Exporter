import json
import os
from unittest import TestCase, mock

from botocore.exceptions import ParamValidationError
import jwt



@mock.patch('export_utils.boto3.client')
@mock.patch('services.write_transaction')
class AddFileExportTestCase(TestCase):

    def setUp(self):
        os.environ['authorized_roles'] = 'admin, developer'

        import app
        app.application.config['JWT_SECRET_KEY'] = 'secret'
        app.application.config['JWT_PUBLIC_KEY'] = None
        app.application.config['JWT_ALGORITHM'] = 'HS256'
        app.application.config['AUTH_TOKEN_KEY_URL'] = ''
        app.application.config['JWT_DECODE_AUDIENCE'] = None

        app.application.testing = True
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
            "primaryUseOfSiteCode": "A",
            "secondaryUseOfSiteCode": " ",
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

    def test_good_upload(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mtransaction.call_args[0][1], self.location)
        self.assertEqual(mtransaction.call_args[1].get('transaction_type'), 'Create')

    def test_no_auth_header(self, mtransaction, mclient):
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        data=json.dumps(self.location))

        self.assertEqual(response.status_code, 401)

    def test_bad_token(self, mtransaction, mclient):
        bad_token = jwt.encode({'authorities': ['developer', 'tester']}, 'bad_secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(bad_token.decode('utf-8'))},
                                        data=json.dumps(self.location))

        self.assertEqual(response.status_code, 422)

    def test_not_authorized(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['student', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))

        self.assertEqual(response.status_code, 401)


    def test_location_with_missing_keys(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        del self.location['wellDepth']
        del self.location['holeDepth']
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 400)

    def test_s3_upload_oserror(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.side_effect = OSError
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 500)

    def test_s3_upload_valueerror(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.side_effect = ValueError
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 500)

    def test_s3_upload_paramvalidationerror(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.side_effect = ParamValidationError(report='Some validation error')
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 500)


@mock.patch('export_utils.boto3.client')
@mock.patch('services.write_transaction')
class UpdateFileExportTestCase(TestCase):
    def setUp(self):
        os.environ['authorized_roles'] = 'admin, developer'

        import app
        app.application.config['JWT_SECRET_KEY'] = 'secret'
        app.application.config['JWT_PUBLIC_KEY'] = None
        app.application.config['JWT_ALGORITHM'] = 'HS256'
        app.application.config['AUTH_TOKEN_KEY_URL'] = ''
        app.application.config['JWT_DECODE_AUDIENCE'] = None

        app.application.testing = True
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
            "primaryUseOfSiteCode": "A",
            "secondaryUseOfSiteCode": " ",
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

    def test_good_upload(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/update',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mtransaction.call_args[0][1], self.location)
        self.assertEqual(mtransaction.call_args[1].get('transaction_type'), 'Update')

    def test_no_auth_header(self, mtransaction, mclient):
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/update',
                                        content_type='application/json',
                                        data=json.dumps(self.location))

        self.assertEqual(response.status_code, 401)

    def test_bad_token(self, mtransaction, mclient):
        bad_token = jwt.encode({'authorities': ['developer', 'tester']}, 'bad_secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/update',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(bad_token.decode('utf-8'))},
                                        data=json.dumps(self.location))

        self.assertEqual(response.status_code, 422)

    def test_not_authorized(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['student', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/update',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))

        self.assertEqual(response.status_code, 401)


    def test_location_with_missing_keys(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        del self.location['wellDepth']
        del self.location['holeDepth']
        response = self.app_client.post('/file_export/add',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 400)

    def test_s3_upload_oserror(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.side_effect = OSError
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/update',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 500)

    def test_s3_upload_valueerror(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.side_effect = ValueError
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/update',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 500)

    def test_s3_upload_paramvalidationerror(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.side_effect = ParamValidationError(report='Some validation error')
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/update',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 500)

@mock.patch('export_utils.boto3.client')
@mock.patch('services.write_transaction')
class ChangeFileExportTestCase(TestCase):

    def setUp(self):
        os.environ['authorized_roles'] = 'admin, developer'

        import app
        app.application.config['JWT_SECRET_KEY'] = 'secret'
        app.application.config['JWT_PUBLIC_KEY'] = None
        app.application.config['JWT_ALGORITHM'] = 'HS256'
        app.application.config['AUTH_TOKEN_KEY_URL'] = ''
        app.application.config['JWT_DECODE_AUDIENCE'] = None

        app.application.testing = True
        self.app_client = app.application.test_client()

        self.location_change = {
            'agencyCode': 'USGS ',
            "siteNumber": "123456789012345",
            'newAgencyCode': 'USGS ',
            "newSiteNumber": "9999999999",
            "updated": "20171214120244",
            "requesterName": "tester",
            "reasonText": "Test primary key update"
        }

    def test_good_upload(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/change',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location_change))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mtransaction.call_args[0][1], self.location_change)
        self.assertEqual(mtransaction.call_args[1].get('transaction_type'), 'Change')

    def test_no_auth_header(self, mtransaction, mclient):
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/change',
                                        content_type='application/json',
                                        data=json.dumps(self.location_change))

        self.assertEqual(response.status_code, 401)

    def test_bad_token(self, mtransaction, mclient):
        bad_token = jwt.encode({'authorities': ['developer', 'tester']}, 'bad_secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/change',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(bad_token.decode('utf-8'))},
                                        data=json.dumps(self.location_change))

        self.assertEqual(response.status_code, 422)

    def test_not_authorized(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['student', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.return_value = None
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/change',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location_change))

        self.assertEqual(response.status_code, 401)

    def test_location_change_with_missing_keys(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        del self.location_change['newAgencyCode']
        response = self.app_client.post('/file_export/change',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location_change))
        self.assertEqual(response.status_code, 400)

    def test_s3_upload_oserror(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.side_effect = OSError
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/change',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location_change))
        self.assertEqual(response.status_code, 500)

    def test_s3_upload_valueerror(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.side_effect = ValueError
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/change',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location_change))
        self.assertEqual(response.status_code, 500)

    def test_s3_upload_paramvalidationerror(self, mtransaction, mclient):
        good_token = jwt.encode({'authorities': ['developer', 'tester']}, 'secret', algorithm='HS256')
        s3_connection_mock = mock.Mock()
        s3_connection_mock.upload_fileobj.side_effect = ParamValidationError(report='Some validation error')
        mclient.return_value = s3_connection_mock
        response = self.app_client.post('/file_export/change',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(self.location_change))
        self.assertEqual(response.status_code, 500)
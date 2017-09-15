
from collections import OrderedDict
from datetime import datetime, timezone
from io import StringIO
from unittest import TestCase, mock

from export_utils import transaction_file_name, write_transaction

class TestTransactionFileName(TestCase):

    def setUp(self):
        self.now = datetime(2017, 10, 3, hour=13, minute=30, second=45, tzinfo=timezone.utc )

    def test_no_site_number(self):
        with mock.patch('export_utils.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value=self.now
            mock_datetime.side_effect=lambda *args, **kw: datetime(*args, **kw)
            self.assertEqual(transaction_file_name({'agencyCode': 'USGS'}), 'mlr..20171003133045')

    def test_with_site_number(self):
        with mock.patch('export_utils.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value=self.now
            mock_datetime.side_effect=lambda *args, **kw: datetime(*args, **kw)
            self.assertEqual(transaction_file_name({'agencyCode': 'USGS', 'siteNumber': '0123456789012'}),
                             'mlr.0123456789012.20171003133045')


class TestWriteTransaction(TestCase):

    def setUp(self):
        self.fd = StringIO()
        # Using an ordered dictionary to guarentee iteration order
        self.location = OrderedDict({
            'id' : 1234,
            'agencyCode' : 'USGS ',
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
        })

        self.expected_response = (
        "agency_cd=USGS \n"
        "site_no=123456789012345\n"
        "station_nm=This station name \n"
        "station_ix=station_ix\n"
        "lat_va=           \n"
        "long_va=            \n"
        "dec_lat_va=\n"
        "dec_long_va=\n"
        "coord_meth_cd= \n"
        "coord_acy_cd= \n"
        "coord_datum_cd=          \n"
        "district_cd=WIS\n"
        "land_net_ds= \n"
        "map_nm=Map Name\n"
        "country_cd=US\n"
        "state_cd=55\n"
        "county_cd=121\n"
        "map_scale_fc=       \n"
        "alt_va=        \n"
        "alt_meth_cd= \n"
        "alt_acy_va=   \n"
        "alt_datum_cd=          \n"
        "huc_cd=07010204\n"
        "agency_use_cd=Y\n"
        "basin_cd=  \n"
        "site_tp_cd=well\n"
        "topo_cd= \n"
        "data_types_cd=                              \n"
        "instruments_cd=instruments_cd\n"
        "site_rmks_tx=Remarks\n"
        "inventory_dt=        \n"
        "drain_area_va=        \n"
        "contrib_drain_area_va=        \n"
        "tz_cd=UTC   \n"
        "local_time_fg=N\n"
        "gw_file_cd=                              \n"
        "construction_dt=        \n"
        "reliability_cd= \n"
        "aqfr_cd=        \n"
        "nat_aqfr_cd=          \n"
        "site_use_1_cd=A\n"
        "site_use_2_cd= \n"
        "site_use_3_cd= \n"
        "water_use_1_cd=W\n"
        "water_use_2_cd= \n"
        "water_use_3_cd= \n"
        "nat_water_use_cd=  \n"
        "aqfr_type_cd=X\n"
        "well_depth_va=        \n"
        "hole_depth_va=        \n"
        "depth_src_cd= \n"
        "project_no=123456789012\n"
        "site_web_cd=N\n"
        "site_cn=asmith  \n"
        "site_cr=20171101144535\n"
        "site_mn=bjones  \n"
        "site_md=20171214120244\n"
        "mcd_cd=\n"
        "DONE"
        )

    def tearDown(self):
        self.fd.close()

    def test_empty_dict(self):
        write_transaction(self.fd, {}, transaction_type='Create')
        self.assertEqual(self.fd.getvalue(), 'trans_type=Create\nDONE')

    def test_normal_location(self):
        self.maxDiff = None
        write_transaction(self.fd, self.location, transaction_type= 'Update')
        self.assertEqual(self.fd.getvalue(), 'trans_type=Update\n{0}'.format(self.expected_response))

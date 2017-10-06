
import re

import boto3


KEY_TO_COLUMN_MAPPING = {
    "agencyCode": "agency_cd",
    "siteNumber": "site_no",
    "stationName": "station_nm",
    "stationIx": "station_ix",
    "latitude": "lat_va",
    "longitude": "long_va",
    "decimalLatitude": "dec_lat_va",
    "decimalLongitude": "dec_long_va",
    "coordinateMethodCode": "coord_meth_cd",
    "coordinateAccuracyCode": "coord_acy_cd",
    "coordinateDatumCode": "coord_datum_cd",
    "districtCode": "district_cd",
    "landNet": "land_net_ds",
    "mapName": "map_nm",
    "countryCode": "country_cd",
    "stateFipsCode": "state_cd",
    "countyCode": "county_cd",
    "mapScale": "map_scale_fc",
    "altitude": "alt_va",
    "altitudeMethodCode": "alt_meth_cd",
    "altitudeAccuracyValue": "alt_acy_va",
    "altitudeDatumCode": "alt_datum_cd",
    "hydrologicUnitCode": "huc_cd",
    "agencyUseCode": "agency_use_cd",
    "basinCode": "basin_cd",
    "siteTypeCode": "site_tp_cd",
    "topographicCode": "topo_cd",
    "dataTypesCode": "data_types_cd",
    "instrumentsCode": "instruments_cd",
    "remarks": "site_rmks_tx",
    "siteEstablishmentDate": "inventory_dt",
    "drainageArea": "drain_area_va",
    "contributingDrainageArea": "contrib_drain_area_va",
    "timeZoneCode": "tz_cd",
    "daylightSavingsTimeFlag": "local_time_fg",
    "gwFileCode": "gw_file_cd",
    "firstConstructionDate": "construction_dt",
    "dataReliabilityCode": "reliability_cd",
    "aquiferCode": "aqfr_cd",
    "nationalAquiferCode": "nat_aqfr_cd",
    "primaryUseOfSite": "site_use_1_cd",
    "secondaryUseOfSite": "site_use_2_cd",
    "tertiaryUseOfSiteCode": "site_use_3_cd",
    "primaryUseOfWaterCode": "water_use_1_cd",
    "secondaryUseOfWaterCode": "water_use_2_cd",
    "tertiaryUseOfWaterCode": "water_use_3_cd",
    "nationalWaterUseCode": "nat_water_use_cd",
    "aquiferTypeCode": "aqfr_type_cd",
    "wellDepth": "well_depth_va",
    "holeDepth": "hole_depth_va",
    "sourceOfDepthCode": "depth_src_cd",
    "projectNumber": "project_no",
    "siteWebReadyCode": "site_web_cd",
    "createdBy": "site_cn",
    "created": "site_cr",
    "updatedBy": "site_mn",
    "updated": "site_md",
    "minorCivilDivisionCode": "mcd_cd"
}

DATE_TRANSFORM_REGEX = re.compile('[^\d]')

def _value_str(value):
    return '' if value is None else str(value)


def transaction_file_name(location):
    '''

    :param dict location:
    :return: str
    '''
    return 'mlr.{0}.{1}'.format(location.get('siteNumber', ''), re.sub(DATE_TRANSFORM_REGEX, '', location.get('updated', '')))


def write_transaction(fd, location, transaction_type=''):
    '''

    :param file object fd:
    :param dict location:
    :param transaction:
    '''
    # Transform the two date fields
    transformed_location = location.copy()
    transformed_location['updated'] = re.sub(DATE_TRANSFORM_REGEX, '', location.get('updated', ''))
    transformed_location['created'] = re.sub(DATE_TRANSFORM_REGEX, '', location.get('created', ''))
    fd.write('trans_type={0}\n'.format(transaction_type).encode())
    for key in location.keys():
        if key in KEY_TO_COLUMN_MAPPING:
            fd.write('{0}={1}\n'.format(KEY_TO_COLUMN_MAPPING.get(key),
                                        _value_str(transformed_location.get(key)
                                                   )
                                        ).encode()
                     )
    fd.write('DONE'.encode())


def upload_to_s3(payload, destination_key, bucket='mlr-exports', region='us-west-2'):
    s3_client = boto3.client('s3', region_name=region)
    s3_client.upload_fileobj(payload, Bucket=bucket, Key=destination_key)

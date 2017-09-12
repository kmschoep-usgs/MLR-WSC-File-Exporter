
from datetime import datetime

def file_name(location):
    '''

    :param dict location:
    :return: str
    '''
    return 'mlr.{0}.{1}'.format(location.get('siteNumber', ''), datetime.utcnow().strftime('%Y%m%d%H%M%S'))

from datetime import datetime, timezone
from unittest import TestCase, mock

from export_utils import file_name

class TestFileName(TestCase):

    def setUp(self):
        self.now = datetime(2017, 10, 3, hour=13, minute=30, second=45, tzinfo=timezone.utc )

    def test_no_site_number(self):
        with mock.patch('export_utils.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value=self.now
            mock_datetime.side_effect=lambda *args, **kw: datetime(*args, **kw)
            self.assertEqual(file_name({'agencyCode': 'USGS'}), 'mlr..20171003133045')

    def test_with_site_number(self):
        with mock.patch('export_utils.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value=self.now
            mock_datetime.side_effect=lambda *args, **kw: datetime(*args, **kw)
            self.assertEqual(file_name({'agencyCode': 'USGS', 'siteNumber': '0123456789012'}),
                             'mlr.0123456789012.20171003133045')
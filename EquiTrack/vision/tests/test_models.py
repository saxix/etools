from __future__ import absolute_import, division, print_function, unicode_literals

from django.test import SimpleTestCase


from users.tests.factories import CountryFactory
from vision.models import VisionSyncLog


class TestStrUnicode(SimpleTestCase):
    '''Ensure calling str() on model instances returns the right text.'''

    def test_vision_sync_log(self):
        country = CountryFactory.build(name='M\xe9xico', schema_name='Mexico', domain_url='mexico.example.com')
        instance = VisionSyncLog(country=country)
        self.assertTrue(str(instance).startswith(u'M\xe9xico'))

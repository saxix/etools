from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from unittest import skipIf

from django.utils.encoding import force_text

from EquiTrack.factories import AgreementFactory, NotificationFactory, PartnerFactory
from EquiTrack.tests.cases import EToolsTenantTestCase


@skipIf(sys.version_info.major == 3, "This test can be deleted under Python 3")
class TestStrUnicode(EToolsTenantTestCase):
    '''Ensure calling str() on model instances returns UTF8-encoded text and force_text() returns unicode.'''
    def test_notification(self):
        agreement = AgreementFactory(partner=PartnerFactory(name=b'xyz'))
        notification = NotificationFactory(sender=agreement)
        self.assertIn(b'Email Notification from', str(notification))
        self.assertIn(b'for xyz', str(notification))

        self.assertIn(u'Email Notification from', force_text(notification))
        self.assertIn(u'for xyz', force_text(notification))

        agreement = AgreementFactory(partner=PartnerFactory(name=u'R\xe4dda Barnen'))
        notification = NotificationFactory(sender=agreement)
        self.assertIn(b'Email Notification from', str(notification))
        self.assertIn(b'for R\xc3\xa4dda Barnen', str(notification))

        self.assertIn(u'Email Notification from', force_text(notification))
        self.assertIn(u'for R\xe4dda Barnen', force_text(notification))

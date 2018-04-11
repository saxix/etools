from __future__ import absolute_import, division, print_function, unicode_literals

from EquiTrack.tests.cases import BaseTenantTestCase
from notification.tests.factories import NotificationFactory
from partners.tests.factories import AgreementFactory, PartnerFactory


class TestStrUnicode(BaseTenantTestCase):
    '''Ensure calling str() on model instances returns the right text.'''

    def test_notification(self):
        agreement = AgreementFactory(partner=PartnerFactory(name='xyz'))
        notification = NotificationFactory(sender=agreement)

        self.assertIn('Email Notification from', str(notification))
        self.assertIn('for xyz', str(notification))

        agreement = AgreementFactory(partner=PartnerFactory(name='R\xe4dda Barnen'))
        notification = NotificationFactory(sender=agreement)
        self.assertIn('Email Notification from', str(notification))
        self.assertIn('for R\xe4dda Barnen', str(notification))

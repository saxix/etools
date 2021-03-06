from __future__ import unicode_literals

from django.core import mail
from django.test.utils import override_settings

from EquiTrack.tests.cases import BaseTenantTestCase
from publics.tests.factories import PublicsBusinessAreaFactory
from t2f.models import Invoice
from t2f.serializers.mailing import TravelMailSerializer
from t2f.tests.factories import ItineraryItemFactory, TravelFactory
from users.tests.factories import UserFactory


class MailingTest(BaseTenantTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.traveler = UserFactory(first_name='Jane',
                                   last_name='Doe')
        cls.traveler.profile.vendor_number = 'usrvnd'
        cls.traveler.profile.save()

        cls.unicef_staff = UserFactory(is_staff=True,
                                       first_name='John',
                                       last_name='Doe')
        cls.travel = TravelFactory(traveler=cls.traveler,
                                   supervisor=cls.unicef_staff)
        ItineraryItemFactory(travel=cls.travel)
        ItineraryItemFactory(travel=cls.travel)
        mail.outbox = []

    @override_settings(DISABLE_INVOICING=False)
    def test_mailing(self):
        tenant_country = self.travel.traveler.profile.country
        tenant_country.business_area_code = '0'
        tenant_country.save()
        PublicsBusinessAreaFactory(code=self.travel.traveler.profile.country.business_area_code)

        self.travel.submit_for_approval()
        self.travel.approve()
        self.travel.send_for_payment()
        self.travel.invoices.all().update(status=Invoice.SUCCESS)
        self.travel.submit_certificate()
        self.travel.approve_certificate()
        self.travel.mark_as_certified()
        self.travel.report_note = 'Note'
        self.travel.mark_as_completed()

        self.assertEqual(len(mail.outbox), 7)

        for email in mail.outbox:
            self.assertIn(self.travel.reference_number, email.subject, email.subject)

    def test_mailing_serializer(self):
        serializer = TravelMailSerializer(self.travel, context={})
        self.assertKeysIn(['reference_number',
                           'cost_summary',
                           'supervisor',
                           'end_date',
                           'cost_assignments',
                           'rejection_note',
                           'currency',
                           'estimated_travel_cost',
                           'location',
                           'traveler',
                           'start_date',
                           'purpose'],
                          serializer.data,
                          exact=True)

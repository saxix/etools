__author__ = 'unicef-leb-inn'

from datetime import timedelta, datetime
from django.db.models.fields.related import ManyToManyField

from tenant_schemas.test.cases import TenantTestCase

from EquiTrack.factories import TripFactory, UserFactory, PartnershipFactory
from trips.forms import TripForm, TravelRoutesForm
from trips.models import Trip
import trips.errors as err


class SimpleObject(object):
    pass

def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data


class TestTripForm(TenantTestCase):

    def setUp(self):
        self.trip = TripFactory(
            status=Trip.PLANNED,
            owner__first_name='Fred',
            owner__last_name='Test',
            purpose_of_travel='To test some trips'
        )

    def create_form(self, data=None, instance=None):
        trip_dict = to_dict(self.trip)
        if data:
            for k, v in data.iteritems():
                trip_dict[k] = v

        form = TripForm(data=trip_dict, instance=instance)

        form.request = SimpleObject()
        form.request.user = self.trip.owner
        return form

    def test_form_validation_for_programme_monitoring(self):
        form = self.create_form()

        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['travel_type_valid'], form.non_field_errors())

    def test_form_validation_for_international_travel(self):
        data = {
            'travel_type': u'advocacy',
            'international_travel': True
        }
        form = self.create_form(data)

        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['international_travel_valid'], form.non_field_errors()),

    def test_form_validation_for_bigger_date(self):
        trip_dict = to_dict(self.trip)
        data = {
            'travel_type': u'advocacy',
            'from_date': trip_dict['from_date'] + timedelta(days=3)
        }
        form = self.create_form(data)
        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['trip_dates_valid'], form.non_field_errors())

    def test_form_validation_for_past_trip(self):
        self.trip.status = Trip.PLANNED
        trip_dict = to_dict(self.trip)
        trip_dict['travel_type'] = u'advocacy'
        trip_dict['from_date'] = trip_dict['from_date'] - timedelta(days=3)
        trip_dict['to_date'] = trip_dict['to_date'] - timedelta(days=2)
        trip_dict['status'] = u'submitted'

        form = self.create_form(trip_dict, self.trip)
        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['trip_ends_before_now'], form.non_field_errors())

    def test_form_validation_for_owner_is_supervisor(self):
        trip_dict = to_dict(self.trip)
        trip_dict['travel_type'] = u'advocacy'
        trip_dict['supervisor'] = trip_dict['owner']

        form = self.create_form(trip_dict)
        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['self_supervised'], form.non_field_errors())

    def test_form_validation_for_status_approved(self):
        self.trip.status = Trip.SUBMITTED
        trip_dict = to_dict(self.trip)
        trip_dict['travel_type'] = u'advocacy'
        trip_dict['status'] = u'approved'

        form = self.create_form(trip_dict, self.trip)
        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['not_supervisor_approved'], form.non_field_errors())

    def test_form_validation_for_ta_required(self):
        trip_dict = to_dict(self.trip)
        trip_dict['travel_type'] = u'advocacy'
        trip_dict['ta_required'] = True
        form = self.create_form(trip_dict)
        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['ta_required_valid'], form.non_field_errors())

    def test_form_validation_for_approved_by_supervisor(self):
        self.trip.status = Trip.SUBMITTED
        trip_dict = to_dict(self.trip)
        trip_dict['travel_type'] = u'advocacy'
        trip_dict['approved_by_supervisor'] = True

        form = self.create_form(trip_dict, self.trip)
        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['valid_supervisor_approved'], form.non_field_errors())

    def test_form_validation_for_approved_by_budget_owner(self):
        self.trip.status = Trip.SUBMITTED
        trip_dict = to_dict(self.trip)
        trip_dict['travel_type'] = u'advocacy'
        trip_dict['approved_by_budget_owner'] = True

        form = self.create_form(trip_dict, self.trip)
        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['approved_by_budget_owner_valid'], form.non_field_errors())

    def test_form_validation_for_ta_drafted_vision(self):
        self.trip.status = Trip.SUBMITTED
        self.trip.approved_by_supervisor = True
        self.trip.approved_date = datetime.today()
        self.trip.date_supervisor_approved = datetime.today()
        trip_dict = to_dict(self.trip)
        trip_dict['status'] = Trip.APPROVED
        trip_dict['travel_type'] = u'advocacy'
        trip_dict['ta_drafted'] = True

        form = self.create_form(trip_dict, self.trip)
        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['no_vision_approver'], form.non_field_errors())

    def test_form_validation_for_completed_no_report(self):
        self.trip.status = Trip.APPROVED
        trip_dict = to_dict(self.trip)
        trip_dict['travel_type'] = u'advocacy'
        trip_dict['status'] = u'completed'

        form = self.create_form(trip_dict, self.trip)
        self.assertFalse(form.is_valid())
        self.assertIn(err.trip['trip_report_required'], form.non_field_errors())

    def test_form_validation_for_completed_no_report_staff_entl(self):
        self.trip.status = Trip.APPROVED
        trip_dict = to_dict(self.trip)
        trip_dict['travel_type'] = u'staff_entitlement'
        trip_dict['status'] = u'completed'

        form = self.create_form(trip_dict, self.trip)
        self.assertTrue(form.is_valid())

    # def test_form_validation_for_completed_ta_required(self):
    #     trip_dict = to_dict(self.trip)
    #     trip_dict['travel_type'] = u'advocacy'
    #     trip_dict['status'] = u'completed'
    #     trip_dict['programme_assistant'] = UserFactory().id
    #     trip_dict['ta_required'] = True
    #     trip_dict['ta_trip_took_place_as_planned'] = False
    #     trip_dict['main_observations'] = 'Test'
    #     form = TripForm(data=trip_dict)
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual(form.non_field_errors()[0],
    #                      'Only the TA travel assistant can complete the trip')


    # def test_form_validation_for_staff_development(self):
    #     trip_dict = to_dict(self.trip)
    #     trip_dict['travel_type'] = u'staff_development'
    #     trip_dict['status'] = u'completed'
    #     trip_dict['main_observations'] = u'Testing completed'
    #     form = TripForm(data=trip_dict)
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual(form.non_field_errors()[0],
    #                      'STAFF DEVELOPMENT trip must be certified by Human '
    #                      'Resources before it can be completed')

    def test_form_validation_for_date_greater(self):
        form = TravelRoutesForm(data={'trip': self.trip.id,
                                      'origin': 'Test1',
                                      'destination': 'Test2',
                                      'depart': datetime.now() + timedelta(hours=3),
                                      'arrive': datetime.now()})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors()[0], 'Arrival must be greater than departure')

    def test_form_validation_for_programme_monitoring_2(self):
        trip_dict = to_dict(self.trip)
        trip_dict['travel_type'] = u'programme_monitoring'
        trip_dict['status'] = u'submitted'
        trip_dict['programme_assistant'] = UserFactory().id
        trip_dict['pcas'] = PartnershipFactory().id
        form = self.create_form(trip_dict)
        self.assertFalse(form.is_valid())
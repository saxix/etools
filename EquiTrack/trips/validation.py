#  __author__ = 'Robi'

import datetime


from django.utils.functional import cached_property

from django_fsm import can_proceed, has_transition_perm

from . import errors


class SimpleObject(object):
    pass


class TripValidationMixin(object):
    """
        Mixin that handles the validation.

        Whenever the object gets instantiated, before validation make sure to call the
        set_data(your_data) and the set_user(request.user) functions



        Important functions:

    """
    def __init__(self, *args, **kwargs):

        self.trip = self
        self.data = {}
        self.user = None
        self.transition_errors = []

    def set_data(self, data):
        self.data = data

    def set_user(self, user):
        self.user = user

    def get_field(self, field_name):
        if self.data:
            # this will test if the key is in the data dict
            # if it is and it's set to None or Null it means it's meant to be that
            if field_name in self.data:
                field = self.data.get(field_name)
            elif self.trip:
                try:
                    field = getattr(self.trip, field_name, None)
                except Exception as e:
                    field = None
        elif self.trip:
            field = getattr(self.trip, field_name)
        else:
            return None

        return field

    def get_validator_object(self, needed_fields):
        t = SimpleObject()
        for field in needed_fields:
            setattr(t, field, self.get_field(field))
        return t

    def make_auto_transitions(self):
        for possible_transition in self.AUTO_TRANSITIONS_ALLOWED:
            if self.trip.status in possible_transition['FROM']:
                for transition_status in possible_transition['TO']:
                    my_transition = self.trip.get_transition({'status': transition_status})
                    if my_transition and can_proceed(my_transition):
                        self.make_auto_transition_updates(transition_status)
                        return True
        return False

    @cached_property
    def trip_dates_valid(self):
        needed_fields = [u'from_date', u'to_date']
        t = self.get_validator_object(needed_fields)

        if (t.from_date and
                t.to_date and
                t.to_date >= t.from_date):
            return True, None

        return False, errors.trip['trip_dates_valid']
    
    @cached_property
    def not_self_supervised(self):
        needed_fields = [u'supervisor', u'owner']
        t = self.get_validator_object(needed_fields)

        if t.supervisor != t.owner:
            return True, None

        return False, errors.trip['self_supervised']

    @cached_property
    def travel_type_valid(self):
        needed_fields = [u'pcas', u'travel_type']
        t = self.get_validator_object(needed_fields)

        if not t.pcas and t.travel_type == self.PROGRAMME_MONITORING:
            return False, errors.trip['travel_type_valid']

        return True, False

    @cached_property
    def ta_required_valid(self):
        needed_fields = [u'ta_required', u'programme_assistant']
        t = self.get_validator_object(needed_fields)

        if t.ta_required and not t.programme_assistant:
            return False, errors.trip['ta_required_valid']

        return True, None

    @cached_property
    def international_travel_valid(self):
        needed_fields = [u'international_travel', u'representative']
        t = self.get_validator_object(needed_fields)

        if t.international_travel and not t.representative:
            return False, errors.trip['international_travel_valid']

        return True, None

    @cached_property
    def valid_supervisor_approved(self):
        needed_fields = [u'approved_by_supervisor', u'date_supervisor_approved']
        t = self.get_validator_object(needed_fields)

        if t.approved_by_supervisor:
            if not t.date_supervisor_approved:
                return False, errors.trip['valid_supervisor_approved']
            # allow for other validation points here:
            #TODO: can a supervisor approve a trip after the to_date

        return True, None

    @cached_property
    def trip_is_planned(self):
        needed_fields = [u'status']
        t = self.get_validator_object(needed_fields)

        if t.status == self.PLANNED:
            return True, None

        return False, errors.trip['trip_is_planned']

    @cached_property
    def approved_by_budget_owner_valid(self):
        needed_fields = [u'approved_by_budget_owner', u'date_budget_owner_approved']

        t = self.get_validator_object(needed_fields)

        if t.approved_by_budget_owner and not t.date_budget_owner_approved:
            return False, errors.trip['approved_by_budget_owner_valid']

        return True, None

    @cached_property
    def status_cancelled_valid(self):
        needed_fields = [u'cancelled_reason']
        t = self.get_validator_object(needed_fields)

        if not t.cancelled_reason:
            return False, errors.trip['status_cancelled_valid']
        return True, None

    @cached_property
    def status_planned_valid(self):

        rigid_fields = [u'approved_by_supervisor', u'approved_by_budget_owner', u'date_human_resources_approved',
                        u'representative_approval', u'date_representative_approved']

        # note the ManyToMany related fields require a different approach
        for field in rigid_fields:
            if self.data.get(field) != getattr(self.trip, field):
                return False, errors.trip['status_planned_valid']+" "+field
        return True, None

    @cached_property
    def status_approved_valid(self):
        # here goes validation for trip being valid if it stays approved
        # like what are the fields that cannot be changed while status stays approved
        rigid_fields = [u'approved_by_supervisor', u'approved_by_budget_owner', u'international_travel',
                        u'ta_required', u'travel_type', u'supervisor', u'owner',u'from_date', u'to_date',
                        u'purpose_of_travel', u'vision_approver', u'programme_assistant']

        # note the ManyToMany related fields require a different approach
        for field in rigid_fields:
            print self.data.get(field), getattr(self.trip, field)
            if self.data.get(field) != getattr(self.trip, field):
                return False, errors.trip['status_approved_valid']+" "+field
        return True, None

    @cached_property
    def status_submitted_valid(self):
        if not self.valid_supervisor_approved[0]:
            return False, self.valid_supervisor_approved[1]

        if not self.approved_by_budget_owner_valid[0]:
            return False, self.approved_by_budget_owner_valid[1]

        rigid_fields = []

        # note the ManyToMany related fields require a different approach
        for field in rigid_fields:
            print self.data.get(field), getattr(self.trip, field)
            if self.data.get(field) != getattr(self.trip, field):
                return False, errors.trip['status_submitted_valid']+" "+field
        return True, None

    @cached_property
    def status_completed_valid(self):
        # TODO: MAKE SURE TO IMPLEMENT THIS
        return True, None

    @cached_property
    def current_state_is_valid(self):
        if "status" in self.data:
            status = self.data['status']
        else:
            status = self.trip.status

        return getattr(self, "status_"+status+"_valid")

    @cached_property
    def transition_to_submitted_valid(self):
        if self.trip.to_date < datetime.datetime.date(datetime.datetime.now()):
            # TODO: move this error in the errors file
            self.transition_errors.append(errors.trip['trip_ends_before_now'])
            return False
        return True

    @cached_property
    def transition_to_cancelled_valid(self):
        if self.trip.cancelled_reason:
            return True
        return False

    @cached_property
    def transition_to_completed_valid(self):
        if self.trip.cancelled_reason:
            return False
        if (not self.trip.main_observations and
                self.travel_type != self.trip.STAFF_ENTITLEMENT):
            self.transition_errors.append(errors.trip['trip_report_required'])
            return False
        return True

    @cached_property
    def transition_to_approved_valid(self):

        if not self.trip.approved_by_supervisor:
            self.transition_errors.append(errors.trip["not_supervisor_approved"])
            return False
        if not self.valid_supervisor_approved[0]:
            self.transition_errors.append(self.valid_supervisor_approved[1])
            return False
        if not self.approved_by_budget_owner_valid[0]:
            self.transition_errors.append(self.approved_by_budget_owner_valid[1])
            return False

        if self.trip.ta_drafted:
            if (not self.trip.vision_approver or
                    not self.trip.programme_assistant):
                self.transition_errors.append(errors.trip['no_vision_approver'])
                return False
        if (self.trip.requires_hr_approval and
                not self.trip.approved_by_human_resources):
            return False
        if (self.trip.requires_rep_approval and
                not self.trip.representative_approval):
            return False
        if self.trip.cancelled_reason:
            return False
        return True

    @cached_property
    def basic_validation(self):
        """
            This ensures that all fields are valid in a very general sense, applicable to all states
        """
        my_errors = []
        if not self.trip_dates_valid[0]:
            my_errors.append(self.trip_dates_valid[1])

        if not self.not_self_supervised[0]:
            my_errors.append(self.not_self_supervised[1])

        if not self.travel_type_valid[0]:
            my_errors.append(self.travel_type_valid[1])

        if not self.ta_required_valid[0]:
            my_errors.append(self.ta_required_valid[1])

        if not self.international_travel_valid[0]:
            my_errors.append(self.international_travel_valid[1])

        if my_errors:
            return False, my_errors
        return True, None

    @cached_property
    def transitional_validation(self):
        """
            This ensures that if there is a transition required (a status change) that transition can be satisfied
        """
        my_errors = []
        trip_transition = self.trip.get_transition(self.data)
        if trip_transition:
            status = self.data.get('status')
            for key, value in self.data.iteritems():
                if hasattr(self.trip, key) and key != 'status':
                    setattr(self.trip, key, value)

            if not can_proceed(trip_transition):
                # TODO: move this error in the errors file
                my_errors.append('Cannot transition to {}'.format(status))
                my_errors.extend(self.transition_errors)
            elif not has_transition_perm(trip_transition, self.user):
                # TODO: move this error in the errors file
                my_errors.append('Cannot transition to {}, User Permission Denied.'.format(status))
            else:
                if status == self.trip.APPROVED:
                    self.trip.approved_date = datetime.date.today()
        else:
            print "not good"
            if not self.current_state_is_valid[0]:
                my_errors.append(self.current_state_is_valid[1])

        if my_errors:
            return False, my_errors
        return True, None

    @cached_property
    def new_object_is_valid(self):
        """
            This ensures that a new object submission has all the required fields filled correctly
        """
        my_errors = []
        if not self.basic_validation[0]:
            my_errors.extend(self.basic_validation[1])

        if not self.trip_is_planned[0]:
            my_errors.append(self.trip_is_planned[1])

        if my_errors:
            return False, my_errors
        return True, None

    @cached_property
    def update_is_valid(self):
        if not self.basic_validation[0]:
            return False, self.basic_validation[1]
        if not self.transitional_validation[0]:
            return False, self.transitional_validation[1]
        return True, None



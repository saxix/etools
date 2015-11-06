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

        # For readability set the trip
        self.trip = self

        # Data with which we intend to update/instantiate the object
        self.data = {}

        # User that is intending to perform this action
        # The user is needed for validating updates and transitions
        self.user = None

        # A list of errors that gets populated if a transition is not possible
        self.transition_errors = []

    def set_data(self, data):
        self.data = data

    def set_user(self, user):
        self.user = user

    def get_field(self, field_name):
        """
            :param field_name: [string] the name of the field to be returned
            :return: the value of the coresponding field name
                    in the self.data or self.trip if it's not present in the data
                    otherwise None
        """
        if self.data:
            # this will test if the key is in the data dict
            # if it is and it's set to None or Null it means it's meant to be that
            if field_name in self.data:
                field = self.data.get(field_name)
            elif self.trip:
                # try to get the field name from the object
                # this will throw an exception for ManytoMany fields that don't exist
                try:
                    field = getattr(self.trip, field_name, None)
                except Exception as e:
                    field = None

        elif self.trip:
            try:
                field = getattr(self.trip, field_name)
            except Exception as e:
                field = None
        else:
            return None

        return field

    def get_validator_object(self, needed_fields):
        """
            :param needed_fields: [list of strings] intended to be returned as properties on an object
            :return: an object with the needed fields set as properties and the values the corresponding
                    values according to get_field()
        """

        t = SimpleObject()
        for field in needed_fields:
            setattr(t, field, self.get_field(field))
        return t

    def make_auto_transitions(self):
        """
            Function meant to apply any possible transition according
            to AUTO_TRANSITIONS_ALLOWED set on the model
        :return: Bool whether an auto transition happened.
        """
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

    def rigid_fields_check(self, rigid_fields):
        """

            :param rigid_fields: [list strings] all the fields that are not allowed to be changed
            :return: a list of all of the fields that are changed
        """
        fields = []
        for field in rigid_fields:
            if self.get_field(field) != getattr(self.trip, field):
                fields.append(field)
        return fields

    @cached_property
    def status_cancelled_valid(self):
        """
            function that checks if the present status fulfills the requirements to stay that way
            (eg if a status is cancelled, the cancelled reason should not be able to be removed)
            :return:
        """
        needed_fields = [u'cancelled_reason']
        t = self.get_validator_object(needed_fields)

        if not t.cancelled_reason:
            return False, errors.trip['status_cancelled_valid']
        return True, None

    @cached_property
    def status_planned_valid(self):
        """
            function that checks if the present status fulfills the requirements to stay that way
            (eg if a status is cancelled, the cancelled reason should not be able to be removed)
            (eg certain fields should not be able to be changed while still in a particular status)
            :return:
        """
        rigid_fields = [u'approved_by_supervisor', u'approved_by_budget_owner', u'date_human_resources_approved',
                        u'representative_approval', u'date_representative_approved']

        # note the ManyToMany related fields require a different approach
        fields = self.rigid_fields_check(rigid_fields)
        if fields:
            return False, errors.trip['status_planned_valid']+" "+" ".join(fields)
        return True, None

    @cached_property
    def status_approved_valid(self):
        """
            function that checks if the present status fulfills the requirements to stay that way
            (eg certain fields should not be able to be changed while still in a particular status)
            :return:
        """
        # here goes validation for trip being valid if it stays approved
        # like what are the fields that cannot be changed while status stays approved
        rigid_fields = [u'approved_by_supervisor', u'approved_by_budget_owner', u'international_travel',
                        u'ta_required', u'travel_type', u'supervisor', u'owner',u'from_date', u'to_date',
                        u'purpose_of_travel', u'vision_approver', u'programme_assistant']

        # note the ManyToMany related fields require a different approach
        fields = self.rigid_fields_check(rigid_fields)
        if fields:
            return False, errors.trip['status_approved_valid']+" "+" ".join(fields)
        return True, None

    @cached_property
    def status_submitted_valid(self):
        """
            function that checks if the present status fulfills the requirements to stay that way
            :return:
        """
        if not self.valid_supervisor_approved[0]:
            return False, self.valid_supervisor_approved[1]

        if not self.approved_by_budget_owner_valid[0]:
            return False, self.approved_by_budget_owner_valid[1]

        rigid_fields = []

        fields = self.rigid_fields_check(rigid_fields)
        if fields:
            return False, errors.trip['status_submitted_valid']+" "+" ".join(fields)
        return True, None

    @property
    def requires_hr_approval(self):
        return self.trip.travel_type in [
            # Trip.STAFF_DEVELOPMENT
        ]

    @property
    def requires_rep_approval(self):
        return self.trip.international_travel

    @cached_property
    def status_completed_valid(self):
        # TODO: MAKE SURE TO IMPLEMENT THIS
        # Maybe none of the fields should be able to be changed after a trip is completed
        return True, None

    @cached_property
    def current_state_is_valid(self):
        """
            function that figures out what state the instance is supposed to be in and
            calls the function that insures that the current status is valid
            (this function relies on the fact that it won't be called unless there is no
            transition requested)
        :return:
        """
        if "status" in self.data:
            status = self.data['status']
        else:
            status = self.trip.status

        return getattr(self, "status_"+status+"_valid")

    def transition_to_submitted_valid(self):
        """
            Function that insures that a particular transition satisfies all the field requirements
            Note that these checks should not include user permission checks
        :return:
            Bool, if the transition can happen safely
        """
        if self.trip.to_date < datetime.datetime.date(datetime.datetime.now()):
            # TODO: move this error in the errors file
            self.transition_errors.append(errors.trip['trip_ends_before_now'])
            return False
        return True

    def transition_to_cancelled_valid(self):
        """
            Function that insures that a particular transition satisfies all the field requirements
            Note that these checks should not include user permission checks
        :return:
            Bool, if the transition can happen safely
        """
        if self.trip.cancelled_reason:
            return True
        return False

    def transition_to_completed_valid(self):
        """
            Function that insures that a particular transition satisfies all the field requirements
            Note that these checks should not include user permission checks
        :return:
            Bool, if the transition can happen safely
        """
        if self.trip.cancelled_reason:
            return False
        if (not self.trip.main_observations and
                self.travel_type != self.trip.STAFF_ENTITLEMENT):
            self.transition_errors.append(errors.trip['trip_report_required'])
            return False
        return True

    def transition_to_approved_valid(self):
        """
            Function that insures that a particular transition satisfies all the field requirements
            Note that these checks should not include user permission checks
        :return:
            Bool, if the transition can happen safely
        """

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
        # List of errors to be returned if any
        my_errors = []

        # get the transition that is required
        trip_transition = self.trip.get_transition(self.data)
        if trip_transition:
            status = self.data.get('status')
            # since the transition check is performed on the validity of the instance fields,
            # update the instance with the proposed changes.
            # (transition checks happen last in this manner therefore it's safe)
            for key, value in self.data.iteritems():
                # make sure that the proposed status is not set
                if hasattr(self.trip, key) and key != 'status':
                    setattr(self.trip, key, value)

            if not can_proceed(trip_transition):
                # TODO: move this error in the errors file and make it more meaningful
                my_errors.append('Cannot transition to {}'.format(status))
                my_errors.extend(self.transition_errors)
            elif not has_transition_perm(trip_transition, self.user):
                # TODO: move this error in the errors file
                my_errors.append('Cannot transition to {}, User Permission Denied.'.format(status))
            else:
                if status == self.trip.APPROVED:
                    self.trip.approved_date = datetime.date.today()

        # if no transition is required:
        else:
            # make sure the current state can remain valid
            if not self.current_state_is_valid[0]:
                my_errors.append(self.current_state_is_valid[1])

        if my_errors:
            return False, my_errors
        return True, None

    @cached_property
    def new_object_is_valid(self):
        """
            This ensures that a new object submission has all the required fields filled correctly
            This function calls basic_validation
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
        """
            Function that insures that the update is valid and any proposed transitions can happen safely
            This function calls basic_validation and transitional_validation
        :return:
        """
        if not self.basic_validation[0]:
            return False, self.basic_validation[1]
        if not self.transitional_validation[0]:
            return False, self.transitional_validation[1]
        return True, None



__author__ = 'jcranwellward'

from datetime import datetime


from django_fsm import can_proceed, has_transition_perm
from django.forms import ModelForm, fields, Form
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from suit.widgets import AutosizedTextarea
from suit_ckeditor.widgets import CKEditorWidget
from datetimewidget.widgets import DateTimeWidget, DateWidget

from partners.models import PCA
from .models import Trip, TravelRoutes, TripLocation
from .validation import TripValidation

class TravelRoutesForm(ModelForm):

    class Meta:
        model = TravelRoutes

    depart = fields.DateTimeField(label='Depart', widget=DateTimeWidget(bootstrap_version=3),
                                  input_formats=['%d/%m/%Y %H:%M'])
    arrive = fields.DateTimeField(label='Arrive', widget=DateTimeWidget(bootstrap_version=3),
                                  input_formats=['%d/%m/%Y %H:%M'])

    def clean(self):
        cleaned_data = super(TravelRoutesForm, self).clean()
        depart = cleaned_data.get('depart')
        arrive = cleaned_data.get('arrive')

        if arrive and depart:
            if arrive < depart:
                raise ValidationError(
                    'Arrival must be greater than departure'
                )

            if self.instance and self.instance.trip_id is not None:
                from_date = datetime.strptime(self.data.get('from_date'), '%Y-%m-%d').date()
                to_date = datetime.strptime(self.data.get('to_date'), '%Y-%m-%d').date()
                depart = depart.date()
                arrive = arrive.date()

                # check if itinerary dates are outside the entire trip date range
                if to_date < depart or depart < from_date or to_date < arrive or arrive < from_date:
                    raise ValidationError(
                        'Travel dates must be within overall trip dates'
                    )
        return cleaned_data


class TripForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Trip
        widgets = {
            'purpose_of_travel':
                AutosizedTextarea(attrs={'class': 'input-xlarge'}),
            'main_observations':
                CKEditorWidget(editor_options={'startupFocus': False}),
        }
    #
    # def full_clean(self):
    #     print self.instance.purpose_of_travel
    #
    #     #raise ValidationError("i hope it doesn't save")
    #     return super(TripForm, self).full_clean()
    # #
    # def save(self, *args, **kwargs):
    #     raise ValidationError("i hope it doesn't save")
    #     return super(TripForm, self).save(*args, **kwargs)


    def clean(self):
        cleaned_data = super(TripForm, self).clean()
        status = cleaned_data.get(u'status')
        travel_type = cleaned_data.get(u'travel_type')
        #from_date = cleaned_data.get(u'from_date')
        to_date = cleaned_data.get(u'to_date')
        owner = cleaned_data.get(u'owner')
        supervisor = cleaned_data.get(u'supervisor')
        budget_owner = cleaned_data.get(u'budget_owner')
        ta_required = cleaned_data.get(u'ta_required')
        pcas = cleaned_data.get(u'pcas')
        no_pca = cleaned_data.get(u'no_pca')
        international_travel = cleaned_data.get(u'international_travel')
        representative = cleaned_data.get(u'representative')
        ta_drafted = cleaned_data.get(u'ta_drafted')
        vision_approver = cleaned_data.get(u'vision_approver')
        programme_assistant = cleaned_data.get(u'programme_assistant')
        approved_by_supervisor = cleaned_data.get(u'approved_by_supervisor')
        date_supervisor_approved = cleaned_data.get(u'date_supervisor_approved')
        approved_by_budget_owner = cleaned_data.get(u'approved_by_budget_owner')
        date_budget_owner_approved = cleaned_data.get(u'date_budget_owner_approved')
        approved_by_human_resources = cleaned_data.get(u'approved_by_human_resources')
        trip_report = cleaned_data.get(u'main_observations')
        ta_trip_took_place_as_planned = cleaned_data.get(u'ta_trip_took_place_as_planned')

        print "here comes the instance:"
        print self.instance.id

        validator = TripValidation(data=cleaned_data, instance=self.instance)

        if not validator.trip_dates_valid[0]:
            raise ValidationError(validator.trip_dates_valid[1])

        if not validator.not_self_supervised[0]:
            raise ValidationError(validator.self_supervised[1])

        if not validator.travel_type_valid[0]:
            raise ValidationError(validator.travel_type_valid[1])

        if not validator.ta_required_valid[0]:
            raise ValidationError(validator.ta_required_valid[1])

        if not validator.international_travel_valid[0]:
            raise ValidationError(validator.international_travel_valid[1])

        if not self.instance.id:
            # this means that this is the point of creation
            # one validation is that it needs to be with status "planned"
            if not validator.trip_is_planned[0]:
                raise ValidationError(validator.trip_is_planned[1])

        else:
            # From here the following trips need to be existing instances
            print "woo hoo instance evaluates as true"

            # validation that only happens if a trip has already been instantiated
            if not validator.valid_supervisor_approved[0]:
                raise ValidationError(validator.valid_supervisor_approved[1])

            if not validator.approved_by_budget_owner_valid[0]:
                raise ValidationError(validator.approved_by_budget_owner_valid[1])

            trip_transition = self.instance.get_transition(cleaned_data)

            if trip_transition:
                status = cleaned_data.pop('status')
                for key, value in cleaned_data.iteritems():
                    if hasattr(self.instance, key):
                        setattr(self.instance, key, value)

                if not can_proceed(trip_transition):
                    raise ValidationError('Cannot transition to {}'.format(status))
                else:
                    cleaned_data['status'] = status
                    if status == Trip.APPROVED:
                        self.instance.approved_date = datetime.date.today()

            else:
                #if validator.auto_transition_possible[0]:
                #    cleaned_data = validator.auto_transition_possible[1]
                #elif validator.current_state_is_valid[0]:
                #    raise ValidationError(validator.current_state_is_valid[1])
                pass
        # THIS IS A TRANSITION VALIDATION
        # if status == Trip.SUBMITTED and to_date < datetime.date(datetime.now()):
        #     raise ValidationError(
        #         'This trip\'s dates happened in the past and therefore cannot be submitted'
        #     )


        # THIS IS A TRANSITION VALIDATION
        # if status == Trip.APPROVED and ta_drafted:
        #     if not vision_approver:
        #         raise ValidationError(
        #             'For TA Drafted trip you must select a Vision Approver'
        #         )
        #     if not programme_assistant:
        #         raise ValidationError(
        #             'For TA Drafted trip you must select a Staff Responsible for TA'
        #         )

        # THIS IS A TRANSITION VALIDATION
        # if status == Trip.APPROVED and not self.instance.approved_by_supervisor:
        #     raise ValidationError(
        #         'Only the supervisor can approve this trip'
        #     )

        if status == Trip.COMPLETED:
            if not trip_report and travel_type != Trip.STAFF_ENTITLEMENT:
                raise ValidationError(
                    'You must provide a narrative report before the trip can be completed'
                )

            if ta_required and ta_trip_took_place_as_planned is False and self.request.user != programme_assistant:
                raise ValidationError(
                    'Only the TA travel assistant can complete the trip'
                )

            # if not approved_by_human_resources and travel_type == Trip.STAFF_DEVELOPMENT:
            #     raise ValidationError(
            #         'STAFF DEVELOPMENT trip must be certified by Human Resources before it can be completed'
            #     )

        #TODO: this can be removed once we upgrade to 1.7
        return cleaned_data


class RequireOneLocationFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        form_count = len([f for f in self.forms if f.cleaned_data])
        if form_count < 1 and self.instance.travel_type == Trip.PROGRAMME_MONITORING:
            raise ValidationError('At least one Trip Location is required.')


class TripFilterByDateForm(Form):

    depart = fields.DateField(
        label='From',
        widget=DateWidget(
            bootstrap_version=3,
            attrs={}
        )
    )
    arrive = fields.DateField(
        label='To',
        widget=DateWidget(
            bootstrap_version=3,
            attrs={}
        )
    )
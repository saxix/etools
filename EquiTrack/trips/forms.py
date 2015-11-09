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

    def clean(self):
        cleaned_data = super(TripForm, self).clean()


        validator = self.instance.validator
        validator.set_data(cleaned_data)
        validator.set_user(self.request.user)

        if not self.instance.id:
            # this means that this is the point of creation
            if not validator.new_object_is_valid[0]:
                raise ValidationError([ValidationError(err) for err in validator.new_object_is_valid[1]])

        else:
            # validation that only happens if a trip has already been instantiated
            if not validator.update_is_valid[0]:
                raise ValidationError([ValidationError(err) for err in validator.update_is_valid[1]])



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
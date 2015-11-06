__author__ = 'jcranwellward'

import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property

from django_fsm import FSMField, transition

from smart_selects.db_fields import ChainedForeignKey
from django.contrib.contenttypes.generic import (
    GenericForeignKey, GenericRelation
)
from django.db.models.signals import post_save
from django.contrib.sites.models import Site

from filer.fields.file import FilerFileField
import reversion

from EquiTrack.mixins import AdminURLMixin
from reports.models import Result
from funds.models import Grant
from users.models import Office, Section
from locations.models import Governorate, Locality, Location, Region
from . import emails
from .validation import TripValidationMixin


BOOL_CHOICES = (
    (None, "N/A"),
    (True, "Yes"),
    (False, "No")
)


class Trip(AdminURLMixin, models.Model, TripValidationMixin):

    PLANNED = u'planned'
    SUBMITTED = u'submitted'
    APPROVED = u'approved'
    COMPLETED = u'completed'
    CANCELLED = u'cancelled'
    TRIP_STATUS = (
        (PLANNED, u"Planned"),
        (SUBMITTED, u"Submitted"),
        (APPROVED, u"Approved"),
        (COMPLETED, u"Completed"),
        (CANCELLED, u"Cancelled"),
    )
    # transitions that are checked if possible (and applied) at save time
    AUTO_TRANSITIONS_ALLOWED = [
        {'FROM': [SUBMITTED], 'TO': [APPROVED, CANCELLED]},
        {'FROM': [APPROVED], 'TO': [COMPLETED, CANCELLED]},
        {'FROM': [PLANNED], 'TO': [CANCELLED]},
    ]

    PROGRAMME_MONITORING = u'programme_monitoring'
    SPOT_CHECK = u'spot_check'
    ADVOCACY = u'advocacy'
    TECHNICAL_SUPPORT = u'technical_support'
    MEETING = u'meeting'
    DUTY_TRAVEL = u'duty_travel'
    HOME_LEAVE = u'home_leave'
    FAMILY_VISIT = u'family_visit'
    EDUCATION_GRANT = u'education_grant'
    STAFF_DEVELOPMENT = u'staff_development'
    STAFF_ENTITLEMENT = u'staff_entitlement'
    TRAVEL_TYPE = (
        (PROGRAMME_MONITORING, u'PROGRAMMATIC VISIT'),
        (SPOT_CHECK, u'SPOT CHECK'),
        (ADVOCACY, u'ADVOCACY'),
        (TECHNICAL_SUPPORT, u'TECHNICAL SUPPORT'),
        (MEETING, u'MEETING'),
        (STAFF_DEVELOPMENT, u"STAFF DEVELOPMENT"),
        (STAFF_ENTITLEMENT, u"STAFF ENTITLEMENT"),
    )

    status = FSMField(
        max_length=32L,
        choices=TRIP_STATUS,
        default=PLANNED,
    )

    cancelled_reason = models.CharField(
        max_length=254,
        blank=True, null=True,
        help_text='Please provide a reason if the mission is cancelled'
    )
    purpose_of_travel = models.CharField(
        max_length=254
    )
    travel_type = models.CharField(
        max_length=32L,
        choices=TRAVEL_TYPE,
        default=PROGRAMME_MONITORING
    )
    security_clearance_required = models.BooleanField(
        default=False,
        help_text='Do you need security clarance for this trip?'
    )
    international_travel = models.BooleanField(
        default=False,
        help_text='International travel will require approval from the representative'
    )
    from_date = models.DateField()
    to_date = models.DateField()

    pcas = models.ManyToManyField(
        u'partners.PCA',
        blank=True, null=True,
        verbose_name=u"Related Interventions"
    )
    partners = models.ManyToManyField(
        u'partners.PartnerOrganization',
        blank=True, null=True
    )
    main_observations = models.TextField(
        blank=True, null=True
    )
    constraints = models.TextField(
        blank=True, null=True
    )
    lessons_learned = models.TextField(
        blank=True, null=True
    )
    opportunities = models.TextField(
        blank=True, null=True
    )

    ta_required = models.BooleanField(
        default=False,
        help_text='Is a Travel Authorisation (TA) is required?'
    )
    programme_assistant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        verbose_name='Staff Responsible for TA',
        help_text='Needed if a Travel Authorisation (TA) is required',
        related_name='managed_trips'
    )

    ta_drafted = models.BooleanField(
        default=False,
        verbose_name='TA',
        help_text='Has the TA been drafted in vision if applicable?'
    )
    ta_drafted_date = models.DateField(blank=True, null=True)
    ta_reference = models.CharField(max_length=254, blank=True, null=True)
    vision_approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        verbose_name='VISION Approver'
    )

    locations = GenericRelation('locations.LinkedLocation')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Traveller', related_name='trips')
    section = models.ForeignKey(Section, blank=True, null=True)
    office = models.ForeignKey(Office, blank=True, null=True)
    travel_assistant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        related_name='organised_trips',
        verbose_name='Travel focal point'
    )
    transport_booked = models.BooleanField(default=False)
    security_granted = models.BooleanField(default=False)

    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supervised_trips')
    approved_by_supervisor = models.BooleanField(default=False)
    date_supervisor_approved = models.DateField(blank=True, null=True)

    budget_owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='budgeted_trips', blank=True, null=True,)
    approved_by_budget_owner = models.BooleanField(default=False)
    date_budget_owner_approved = models.DateField(blank=True, null=True)

    human_resources = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='certified_trips', blank=True, null=True)
    approved_by_human_resources = models.NullBooleanField(
        default=None,
        choices=BOOL_CHOICES,
        verbose_name='Certified by human resources',
        help_text='HR must approve all trips relating to training and staff development')
    date_human_resources_approved = models.DateField(blank=True, null=True)

    representative = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_trips', blank=True, null=True)
    representative_approval = models.NullBooleanField(default=None, choices=BOOL_CHOICES)
    date_representative_approved = models.DateField(blank=True, null=True)

    approved_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    approved_email_sent = models.BooleanField(default=False)

    ta_trip_took_place_as_planned = models.BooleanField(
        default=False,
        verbose_name='Ta trip took place as attached',
        help_text='I certify that the travel took place exactly as per the attached Travel Authorization and'
                  ' that there were no changes to the itinerary'
    )
    ta_trip_repay_travel_allowance = models.BooleanField(
        default=False,
        help_text='I certify that I will repay any travel allowance to which I am not entitled'
    )
    ta_trip_final_claim = models.BooleanField(
        default=False,
        help_text='I authorize UNICEF to treat this as the FINAL Claim'
    )
    class Meta:
        ordering = ['-created_date']

    def __unicode__(self):
        return u'{}   {} - {}: {}'.format(
            self.reference(),
            self.from_date,
            self.to_date,
            self.purpose_of_travel
        )

    @cached_property
    def validator(self, data=None, *args, **kwargs):
        """
            Property that is set for easier comprehension of the separation of concerns,
            and standardizing access to the validation class.
        """
        return super(models.Model, self)

    def reference(self):
        return '{}/{}-{}'.format(
            self.created_date.year,
            self.id,
            self.trip_revision
        ) if self.id else None
    reference.short_description = 'Reference'

    def outstanding_actions(self):
        return self.actionpoint_set.filter(
            status='open').count()


    @property
    def trip_revision(self):
        return reversion.get_for_object(self).count()

    @property
    def trip_overdue(self):
        if self.to_date < datetime.date.today() and self.status != Trip.COMPLETED:
            return True
        return False

    def user_has_approval_permission(self, user):
        # here we would check if the user has the specific permissions as well
        # if not user.has_perm(mypermission)
        #   return False
        return user in [self.supervisor, self.travel_assistant, self.budget_owner]

    def user_can_modify(self, user):
        return user in [self.owner, self.supervisor, self.travel_assistant, self.budget_owner]

    def user_can_complete(self, user):
        if (self.ta_required and
                self.ta_trip_took_place_as_planned is False and
                user != self.programme_assistant):
            return False

        return user in [self.owner, self.travel_assistant]

    def valid_transition_to_approved(self):
        return self.validator.transition_to_approved_valid()

    def valid_transition_to_submitted(self):
        return self.validator.transition_to_submitted_valid()

    def valid_transition_to_cancelled(self):
        return self.validator.transition_to_cancelled_valid()

    def valid_transition_to_completed(self):
        return self.validator.transition_to_completed_valid()

    def get_transition(self, data):
        """
        :param data: a dict that contains the potential transition "status"
        :return: a callable transition function or None
        """

        # return None if the proposed status was not present or
        # is not different form the instance status
        if (not data.get('status') in [s[0] for s in self.TRIP_STATUS] or
                data.get('status') == self.status):
            return None
        else:
            try:
                return getattr(self, 'transition_to_'+data.get('status'))
            except AttributeError as e:
                return None

    @transition(
        field=status,
        source=SUBMITTED,
        target=APPROVED,
        permission=user_can_modify,  #user_can_approve
        conditions=[valid_transition_to_approved]
    )
    def transition_to_approved(self, *args, **kwargs):
        pass

    @transition(
        field=status,
        source=[PLANNED, APPROVED],
        target=SUBMITTED,
        permission=user_can_modify,
        conditions=[valid_transition_to_submitted]
    )
    def transition_to_submitted(self, *args, **kwargs):
        pass

    @transition(
        field=status,
        source=[PLANNED, SUBMITTED, APPROVED],
        target=CANCELLED,
        permission=user_can_modify,
        conditions=[valid_transition_to_cancelled]
    )
    def transition_to_cancelled(self, *args, **kwargs):
        pass

    @transition(
        field=status,
        source=[APPROVED],
        target=COMPLETED,
        permission=user_can_complete,
        conditions=[valid_transition_to_completed]
    )
    def transition_to_completed(self, *args, **kwargs):
        pass

    def make_auto_transition_updates(self, status):
        """
            Function that makes all the necessary updates for any automatic_transition that was performed
            This function only gets called if an auto_transmition is performed
        """
        if status == self.APPROVED:
            self.approved_date = datetime.date.today()
            self.status = Trip.APPROVED
        if status == self.CANCELLED:
            self.status = Trip.CANCELLED

    def save(self, **kwargs):
        # check if trip can be approved
        self.validator.make_auto_transitions()

        super(Trip, self).save(**kwargs)

    @property
    def all_files(self):
        return FileAttachment.objects.filter(object_id=self.id)

    @classmethod
    def get_all_trips(cls, user):
        super_trips = user.supervised_trips.filter(
            Q(status=Trip.APPROVED) | Q(status=Trip.SUBMITTED)
        )
        my_trips = user.trips.filter(
            Q(status=Trip.APPROVED) | Q(status=Trip.SUBMITTED) | Q(status=Trip.PLANNED)
        )
        return my_trips | super_trips

    @classmethod
    def send_trip_request(cls, sender, instance, created, **kwargs):
        """
        Trip emails alerts are sent at various stages...
        """
        # default list of recipients
        recipients = [
            instance.owner.email,
            instance.supervisor.email]

        #TODO: Make this work now that offices are moved into the global schema
        # get zonal chiefs emails if travelling in their respective zones
        # locations = instance.locations.all().values_list('governorate__id', flat=True)
        # offices = Office.objects.filter(location_id__in=locations)
        # zonal_chiefs = [office.zonal_chief.email for office in offices if office.zonal_chief]

        if instance.budget_owner:
            if instance.budget_owner.email not in recipients:
                recipients.append(instance.budget_owner.email)

        if instance.status == Trip.SUBMITTED:
            emails.TripCreatedEmail(instance).send(
                instance.owner.email,
                *recipients
            )
            if instance.international_travel and instance.approved_by_supervisor:
                recipients.append(instance.representative.email)
                emails.TripRepresentativeEmail(instance).send(
                    instance.owner.email,
                    *recipients
                )

        elif instance.status == Trip.CANCELLED:
            # send an email to everyone if the trip is cancelled
            if instance.travel_assistant:
                recipients.append(instance.travel_assistant.email)

            #recipients.extend(zonal_chiefs)
            emails.TripCancelledEmail(instance).send(
                instance.owner.email,
                *recipients
            )

        elif instance.status == Trip.APPROVED:
            if instance.travel_assistant and not instance.transport_booked:
                emails.TripTravelAssistantEmail(instance).send(
                    instance.owner.email,
                    instance.travel_assistant.email
                )

            if instance.ta_required and instance.programme_assistant and not instance.ta_drafted:
                emails.TripTAEmail(instance).send(
                    instance.owner.email,
                    instance.programme_assistant.email
                )

            if instance.ta_drafted and instance.vision_approver:
                emails.TripTADraftedEmail(instance).send(
                    instance.programme_assistant.email,
                    instance.vision_approver.email
                )

            if not instance.approved_email_sent:
                if instance.international_travel:
                    recipients.append(instance.representative.email)

                #recipients.extend(zonal_chiefs)
                emails.TripApprovedEmail(instance).send(
                    instance.owner.email,
                    *recipients
                )
                instance.approved_email_sent = True
                instance.save()

        elif instance.status == Trip.COMPLETED:
            emails.TripCompletedEmail(instance).send(
                instance.owner.email,
                *recipients
            )

post_save.connect(Trip.send_trip_request, sender=Trip)


class TripFunds(models.Model):

    trip = models.ForeignKey(Trip)
    wbs = models.ForeignKey(
        Result, verbose_name='WBS'
    )
    grant = models.ForeignKey(Grant)
    amount = models.PositiveIntegerField(
        verbose_name='Percentage (%)'
    )

    class Meta:
        verbose_name = u'Funding'
        verbose_name_plural = u'Funding'


class TripLocation(models.Model):
    trip = models.ForeignKey(Trip)
    governorate = models.ForeignKey(Governorate)
    region = ChainedForeignKey(
        Region,
        chained_field="governorate",
        chained_model_field="governorate",
        show_all=False,
        auto_choose=True,
    )
    locality = ChainedForeignKey(
        Locality,
        chained_field="region",
        chained_model_field="region",
        show_all=False,
        auto_choose=True,
        null=True, blank=True
    )
    location = ChainedForeignKey(
        Location,
        chained_field="locality",
        chained_model_field="locality",
        show_all=False,
        auto_choose=False,
        null=True, blank=True
    )

    def __unicode__(self):
        desc = u'{} -> {}'.format(
            self.governorate.name,
            self.region.name,
        )
        if self.locality:
            desc = u'{} -> {}'.format(
                desc,
                self.locality.name
            )
        if self.location:
            desc = u'{} -> {} ({})'.format(
                desc,
                self.location.name,
                self.location.gateway.name
            )

        return desc


class TravelRoutes(models.Model):

    trip = models.ForeignKey(Trip)
    origin = models.CharField(max_length=254)
    destination = models.CharField(max_length=254)
    depart = models.DateTimeField()
    arrive = models.DateTimeField()
    remarks = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name = u'Travel Itinerary'
        verbose_name_plural = u'Travel Itinerary'


class ActionPoint(models.Model):

    STATUS = (
        ('closed', 'Closed'),
        ('ongoing', 'On-going'),
        ('open', 'Open'),
        ('cancelled', 'Cancelled')
    )

    trip = models.ForeignKey(Trip)
    description = models.CharField(max_length=254)
    due_date = models.DateField()
    person_responsible = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='for_action')
    actions_taken = models.TextField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS, max_length=254, null=True, verbose_name='Status')
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.description

    @property
    def overdue(self):
        return self.due_date <= datetime.date.today()

    @property
    def due_soon(self):
        delta = (self.due_date - datetime.date.today()).days
        return delta <= 2

    @property
    def traffic_color(self):
        if self.overdue:
            return 'red'
        elif self.due_soon:
            return 'yellow'
        else:
            return 'green'

    @classmethod
    def send_action(cls, sender, instance, created, **kwargs):

        recipients = [instance.person_responsible.email, instance.trip.supervisor.email]

        if created:
            emails.TripActionPointCreated(instance).send(
                instance.trip.owner.email,
                *recipients
            )
        elif instance.status == 'closed':
            emails.TripActionPointClosed(instance).send(
                instance.trip.owner.email,
                *recipients
            )
        else:
            emails.TripActionPointUpdated(instance).send(
                instance.trip.owner.email,
                *recipients
            )


post_save.connect(ActionPoint.send_action, sender=ActionPoint)


def get_report_filename(instance, filename):
    return '/'.join([
        'trip_reports',
        instance.trip.owner.profile.country.name,
        str(instance.trip.id),
        filename
    ])


class FileAttachment(models.Model):

    trip = models.ForeignKey(Trip, null=True, blank=True, related_name=u'files')
    type = models.ForeignKey(u'partners.FileType')
    file = FilerFileField(null=True, blank=True)
    caption = models.TextField(
        null=True,
        blank=True,
        verbose_name='Caption / Description',
        help_text='Description of the file to upload: optional',
    )
    report = models.FileField(
        upload_to=get_report_filename
    )

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u'{}: {}'.format(
            self.type.name,
            self.report.name
        )

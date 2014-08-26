__author__ = 'jcranwellward'

from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline

from reversion import VersionAdmin

from trips.models import FileAttachment
from partners.models import GwPCALocation, PartnerOrganization
from .models import TPMVisit


class FileAttachmentInlineAdmin(GenericTabularInline):
    model = FileAttachment


class TPMVisitAdmin(VersionAdmin):
    list_display = (
        u'status',
        u'pca',
        u'sectors',
        u'location',
        u'tentative_date',
        u'completed_date'
    )
    readonly_fields = (
        u'pca',
        u'location',
        u'unicef_manager',
        u'partner_manager',
    )
    inlines = (
        FileAttachmentInlineAdmin,
    )

    def sectors(self, obj):
        return obj.pca.sectors

    def unicef_manager(self, obj):
        return u'{} {} ({})'.format(
            obj.pca.unicef_mng_first_name,
            obj.pca.unicef_mng_last_name,
            obj.pca.unicef_mng_email
        )

    def partner_manager(self, obj):
        return u'{} {} ({})'.format(
            obj.pca.partner_mng_first_name,
            obj.pca.partner_mng_last_name,
            obj.pca.partner_mng_email
        )


class TPMPartnerFilter(admin.SimpleListFilter):

    title = 'Partner'
    parameter_name = 'partner'

    def lookups(self, request, model_admin):

        return [
            (partner.id, partner.name) for partner in PartnerOrganization.objects.all()
        ]

    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(pca__partner__id=self.value())
        return queryset


class TPMLocationsAdmin(admin.ModelAdmin):

    list_display = (
        u'pca',
        u'governorate',
        u'region',
        u'locality',
        u'location',
        u'view_location',
        u'tpm_visit',
    )
    list_filter = (
        u'pca',
        u'governorate',
        u'region',
        u'locality',
        u'location',
    )
    search_fields = (
        u'pca__number',
        u'governorate__name',
        u'region__name',
        u'locality__name',
        u'location__name',
        u'location__gateway__name',
    )
    readonly_fields = (
        u'view_location',
    )
    list_editable = (
        u'tpm_visit',
    )


admin.site.register(TPMVisit, TPMVisitAdmin)
admin.site.register(GwPCALocation, TPMLocationsAdmin)
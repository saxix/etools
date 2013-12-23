__author__ = 'jcranwellward'

from django.contrib import admin

from reports.models import (
    Sector,
    WBS,
    Goal,
    Unit,
    Activity,
    Indicator,
    Rrp5Output,
    IntermediateResult,
    ResultStructure
)


class GoalAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(ResultStructure)
admin.site.register(Sector)
admin.site.register(Activity)
admin.site.register(IntermediateResult)
admin.site.register(Rrp5Output)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Unit)
admin.site.register(Indicator)
admin.site.register(WBS)
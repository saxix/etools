import operator

from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from rest_framework import permissions

from audit.models import AuditPermission, UNICEFAuditFocalPoint
from utils.permissions.models.models import BasePermission


class HasCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        model = getattr(view, 'model', None) or view.get_queryset().model
        model_names = [model._meta.model_name] + [parent._meta.model_name
                                                  for parent in model._meta.get_parent_list()]
        conditions = six.moves.reduce(operator.or_, [models.Q(target__startswith=model_name)
                                                     for model_name in model_names])

        permissions = AuditPermission.objects.filter(
            conditions,
            permission_type=BasePermission.TYPES.allow,
            permission=BasePermission.PERMISSIONS.edit
        ).filter(user=request.user).filter(
            instance_status=AuditPermission.STATUSES.new
        )

        return view.action != 'create' or permissions.exists()


class CanCreateStaffMembers(permissions.BasePermission):
    message = _('User is not UNICEF audit focal point')

    def has_permission(self, request, view):
        return request.user.groups.filter(
            id=UNICEFAuditFocalPoint.as_group().id
        ).exists()

"""
Project wide mixins for models and classes
"""
from django.contrib.auth import get_user_model
from django.db import connection


class CountryUsersAdminMixin(object):

    staff_only = True

    def filter_users(self, kwargs):

        filters = {}
        if connection.tenant:
            filters['profile__country'] = connection.tenant
        if self.staff_only:
            filters['is_staff'] = True

        if filters:
            # preserve existing filters if any
            queryset = kwargs.get("queryset", get_user_model().objects)
            kwargs["queryset"] = queryset.filter(**filters)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.rel.to is get_user_model():
            self.filter_users(kwargs)

        return super(CountryUsersAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if db_field.rel.to is get_user_model():
            self.filter_users(kwargs)

        return super(CountryUsersAdminMixin, self).formfield_for_manytomany(db_field, request, **kwargs)


class ExportModelMixin(object):
    def set_labels(self, serializer_fields, model):
        labels = {}
        model_labels = {}
        for f in model._meta.fields:
            model_labels[f.name] = f.verbose_name
        for f in serializer_fields:
            if model_labels.get(f, False):
                labels[f] = model_labels.get(f)
            elif serializer_fields.get(f) and serializer_fields[f].label:
                labels[f] = serializer_fields[f].label
            else:
                labels[f] = f.replace("_", " ").title()
        return labels

    def get_renderer_context(self):
        context = super(ExportModelMixin, self).get_renderer_context()
        if hasattr(self, "get_serializer_class"):
            serializer_class = self.get_serializer_class()
            serializer = serializer_class()
            serializer_fields = serializer.get_fields()
            model = getattr(serializer.Meta, "model")
            context["labels"] = self.set_labels(
                serializer_fields,
                model
            )
        return context

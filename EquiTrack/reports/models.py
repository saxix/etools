__author__ = 'jcranwellward'

from django.db import models


class ResultStructure(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name


class Sector(models.Model):

    name = models.CharField(max_length=45L, unique=True)
    description = models.CharField(max_length=256L, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Rrp5Output(models.Model):

    result_structure = models.ForeignKey(ResultStructure, blank=True, null=True)
    sector = models.ForeignKey(Sector)
    code = models.CharField(max_length=16L)
    name = models.CharField(max_length=256L, unique=True)

    class Meta:
        verbose_name = 'RRP5 Output'

    def __unicode__(self):
        return self.name


class Goal(models.Model):
    sector = models.ForeignKey(Sector)
    name = models.CharField(max_length=512L, unique=True)
    description = models.CharField(max_length=512L, blank=True)

    def __unicode__(self):
        return self.name


class Unit(models.Model):
    type = models.CharField(max_length=45L, unique=True)

    def __unicode__(self):
        return self.type


class Indicator(models.Model):

    goal = models.ForeignKey(Goal)
    name = models.CharField(max_length=128L, unique=True)
    unit = models.ForeignKey(Unit)
    total = models.IntegerField()

    def __unicode__(self):
        return self.name


class IntermediateResult(models.Model):
    sector = models.ForeignKey(Sector)
    ir_wbs_reference = models.CharField(max_length=50L)
    name = models.CharField(max_length=128L, unique=True)

    def __unicode__(self):
        return self.name


class WBS(models.Model):
    Intermediate_result = models.ForeignKey(IntermediateResult)
    name = models.CharField(max_length=128L, unique=True)
    code = models.CharField(max_length=10L)

    def __unicode__(self):
        return self.name


class Activity(models.Model):
    sector = models.ForeignKey(Sector)
    name = models.CharField(max_length=128L, unique=True)
    type = models.CharField(max_length=30L, blank=True, null=True)

    def __unicode__(self):
        return self.name
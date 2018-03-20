from django.db import models


class RosterRecord(models.Model):
    # todo: integrate with Commander model?

    roster_num = models.PositiveSmallIntegerField('roster number', blank=False)
    application_date = models.DateTimeField()
    # cmdr_name
    # call_sign
    # timezone
    # ship_type
    # ship_name
    # ship_id
    range = models.FloatField('jump range')
    # roles (booleans)
    dw1_veteran = models.BooleanField(default=False)
    visited_beagle_point = models.BooleanField(default=False)
    # platform



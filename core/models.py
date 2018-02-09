from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Location(models.Model):
    # system
    system = models.CharField(max_length=128, null=False, blank=False)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    z = models.FloatField(null=True)

    # body
    body = models.CharField(max_length=64, null=True, blank=True)
    gravity = models.FloatField(null=True, blank=True)

    # surface
    site_name = models.CharField(max_length=128, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    # edsm
    edsm_id = models.IntegerField(null=True)  # system id

    # todo: integrate with edsm

    def __str__(self):
        s = ['{system}'.format(system=self.system)]
        if self.body:
            s.append('{body}'.format(body=self.body))
        if self.lat and self.lon:
            s.append('[{lat:.4f}/{lon:.4f}]'.format(lat=self.lat, lon=self.lon))
        return str.join(' ', s)

    def get_absolute_url(self):
        pass  # todo


class Waypoint(models.Model):
    id = models.IntegerField(primary_key=True)          # waypoint number
    name = models.CharField(max_length=128)             # waypoint name
    # base_camp_name = models.CharField(max_length=128)   # base camp name stored in base_camp.site_name

    # todo: defaults - if upload date is before or on arrival date, sort into this waypoint folder
    arrival_date = models.DateField()
    base_camp = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Waypoint {:02d}: {}".format(self.id, self.base_camp.site_name)

    @property
    def abbrev(self):
        if self.id == 0:
            return "Pre-Expedition"
        elif self.id == -1:
            return "Post-Expedition"
        else:
            return "WP{:02d}".format(self.id)


class Ship(models.Model):

    # region constants
    ADDER = 'adder'
    ANACONDA = 'conda'
    ASP_EXPLORER = 'aspx'
    ASP_SCOUT = 'asps'
    BELUGA = 'beluga'
    CHIEFTAIN = 'chieftain'
    COBRA_MK_III = 'cobra3'
    COBRA_MK_IV = 'cobra4'
    DIAMONDBACK_EXPLORER = 'dbx'
    DIAMONDBACK_SCOUT = 'dbs'
    DOLPHIN = 'dolphin'
    EAGLE = 'eagle'
    FEDERAL_ASSAULT_SHIP = 'fas'
    FEDERAL_CORVETTE = 'corvette'
    FEDERAL_DROPSHIP = 'dropship'
    FEDERAL_GUNSHIP = 'gunship'
    FER_DE_LANCE = 'fdl'
    HAULER = 'hauler'
    IMPERIAL_CLIPPER = 'clipper'
    IMPERIAL_COURIER = 'courier'
    IMPERIAL_CUTTER = 'cutter'
    IMPERIAL_EAGLE = 'ieagle'
    KEELBACK = 'keelback'
    KRAIT = 'krait'
    ORCA = 'orca'
    PYTHON = 'python'
    SIDEWINDER = 'sidewinder'
    TYPE_10 = 't10'
    TYPE_6 = 't6'
    TYPE_7 = 't7'
    TYPE_9 = 't9'
    VIPER_MK_III = 'viper3'
    VIPER_MK_IV = 'viper4'
    VULTURE = 'vulture'

    SHIP_TYPES = (
        (ADDER, 'Adder'),
        (ANACONDA, 'Anaconda'),
        (ASP_EXPLORER, 'Asp Explorer'),
        (ASP_SCOUT, 'Asp Scout'),
        (BELUGA, 'Beluga Liner'),
        (CHIEFTAIN, 'Chieftain'),
        (COBRA_MK_III, 'Cobra Mk III'),
        (COBRA_MK_IV, 'Cobra Mk IV'),
        (DIAMONDBACK_EXPLORER, 'Diamondback Explorer'),
        (DIAMONDBACK_SCOUT, 'Diamondback Scout'),
        (DOLPHIN, 'Dolphin'),
        (EAGLE, 'Eagle Mk II'),
        (FEDERAL_ASSAULT_SHIP, 'Federal Assault Ship'),
        (FEDERAL_CORVETTE, 'Federal Corvette'),
        (FEDERAL_DROPSHIP, 'Federal Dropship'),
        (FEDERAL_GUNSHIP, 'Federal Gunship'),
        (FER_DE_LANCE, 'Fer-De-Lance'),
        (HAULER, 'Hauler'),
        (IMPERIAL_CLIPPER, 'Imperial Clipper'),
        (IMPERIAL_COURIER, 'Imperial Courier'),
        (IMPERIAL_CUTTER, 'Imperial Cutter'),
        (IMPERIAL_EAGLE, 'Imperial Eagle'),
        (KEELBACK, 'Keelback'),
        (KRAIT, 'Krait'),
        (ORCA, 'Orca'),
        (PYTHON, 'Python'),
        (SIDEWINDER, 'Sidewinder Mk I'),
        (TYPE_10, 'Type-10 Defender'),
        (TYPE_6, 'Type-6 Transporter'),
        (TYPE_7, 'Type-7 Transporter'),
        (TYPE_9, 'Type-9 Heavy'),
        (VIPER_MK_III, 'Viper Mk III'),
        (VIPER_MK_IV, 'Viper Mk IV'),
        (VULTURE, 'Vulture')
    )
    # endregion

    model = models.CharField('ship model', max_length=16, choices=SHIP_TYPES)
    name = models.CharField('ship name', max_length=24, null=True, blank=True)
    range = models.FloatField('jump range')
    livery = models.CharField('ship livery', max_length=48)

    call_sign = models.CharField('call sign', max_length=8)

    def __str__(self):
        return '{}: {} ({:.2f})'.format(self.call_sign, self.get_model_display(), self.range)


class Commander(models.Model):
    # relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # commander info
    cmdr_name = models.CharField('commander name', max_length=25, blank=False, null=True)

    # distant worlds 2 info (see roster)
    roster_num = models.PositiveSmallIntegerField('roster number', blank=False, null=True)

    # scrape roster
    ship = models.ForeignKey(Ship, on_delete=models.SET_NULL)
    comms_id = models.CharField('comms nickname', max_length=15, null=True)
    timezone = models.CharField(max_length=8)
    platform = models.CharField(max_length=8)
    dwe_veteran = models.BooleanField(default=False)
    visited_beagle_point = models.BooleanField(default=False)

    # fixme: maybe don't include these?
    primary_role = models.CharField(max_length=24)
    secondary_role = models.CharField(max_length=24, null=True)

    def __str__(self):
        return "CMDR {}".format(self.cmdr_name)

    def scrape_roster(self):
        pass  # todo


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Commander.objects.create(user=instance)
    instance.commander.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.commander.save()


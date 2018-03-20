from django.contrib.auth.models import User
from django.db import models


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


class Commander(models.Model):

    # region constants
    EXPL = 0
    RAT = 1
    MINER = 2
    MECH = 3
    GUIDE = 4
    PHOTO = 5
    ESCORT = 6
    GEOL = 7
    SCI = 8
    MEDIA = 9
    MCORP = 10
    LOGIST = 11

    PC = 0
    XBOX = 1
    PS4 = 2
    MACOS = 3

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

    NO = 0
    YES = 1
    MAYBE = 2

    DW2_SHIP_TYPES = (
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

    DW2_ROLES = (
        (EXPL,   'Explorer'),
        (RAT,    'Fuel Rat'),
        (MINER,  'Miner'),
        (MECH,   'Fleet Mechanic'),
        (GUIDE,  'Tour Guide'),
        (PHOTO,  'Astrophotographer'),
        (ESCORT, 'Fighter Escort'),
        (GEOL,   'Geologist'),
        (SCI,    'Scientist'),
        (MEDIA,  'Media'),
        (MCORP,  'MediCorp'),
        (LOGIST, 'Fleet Logistics')
    )

    DW2_PLATFORMS = (
        (PC,    'PC'),
        (XBOX,  'XBOne'),
        (PS4,   'PS4'),
        (MACOS, 'Mac')
    )

    DW2_PATCHES = (
        (NO, 'No'),
        (YES, 'Yes'),
        (MAYBE, 'Maybe')
    )
    # endregion

    # relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    # commander info
    cmdr_name = models.CharField('Commander Name', max_length=25, blank=False)

    # distant worlds 2 info (see roster)
    roster_num = models.PositiveSmallIntegerField('DW2 Roster #', blank=False, null=True)

    validation = models.BooleanField('Validated', default=True)
    staff = models.BooleanField('Expedition staff', default=False)

    modified = models.DateTimeField()

    ship_model = models.CharField('Ship Model', max_length=16, choices=DW2_SHIP_TYPES)
    ship_name = models.CharField('Ship Name', max_length=24, null=True, blank=True)
    ship_id = models.CharField('Ship ID', max_length=6)
    ship_range = models.FloatField('Jump Range (LY)')
    livery = models.CharField('ship livery', max_length=48, null=True)

    comms_id = models.CharField('Comms Nickname', max_length=15, null=True)
    timezone = models.CharField('Timezone', max_length=8, null=True)
    platform = models.CharField('Platform', max_length=8, choices=DW2_PLATFORMS, default="PC")
    dwe_veteran = models.BooleanField('Participated in DWE 3302', default=False)
    visited_beagle_point = models.BooleanField('Has visited Beagle Point', default=False)

    role1 = models.IntegerField('Primary Role', choices=DW2_ROLES, default=EXPL)
    role2 = models.IntegerField('Secondary Role', choices=DW2_ROLES, null=True)

    avg_playtime = models.CharField('Average hours played per week', max_length=16)

    dw_patch = models.PositiveSmallIntegerField('Interested in embroidered patch', choices=DW2_PATCHES)

    # region expeditions
    exp_01 = models.BooleanField('Expedition: Nebulae Research Voyages', default=False)
    exp_02 = models.BooleanField('Expedition: REGOR Border Mapping', default=False)
    exp_03 = models.BooleanField('Expedition: Sagittarius-Carina Mission', default=False)
    exp_04 = models.BooleanField('Expedition: Dumbbell Project', default=False)
    exp_05 = models.BooleanField('Expedition: Distant Worlds 3302', default=False)
    exp_06 = models.BooleanField('Expedition: Formidine Rift Survey', default=False)
    exp_07 = models.BooleanField('Expedition: Meet & Greet Expedition', default=False)
    exp_08 = models.BooleanField('Expedition: Crab Nebula Expedition', default=False)
    exp_09 = models.BooleanField('Expedition: Borderlands Venture', default=False)
    exp_10 = models.BooleanField('Expedition: Western Expedition', default=False)
    exp_11 = models.BooleanField('Expedition: August Exodus - A Jaunt To Jaques', default=False)
    exp_12 = models.BooleanField('Expedition: Lost Stars - DWE XBox', default=False)
    exp_13 = models.BooleanField('Expedition: Formidine Rift Expedition', default=False)
    exp_14 = models.BooleanField('Expedition: Small Worlds Expedition', default=False)
    exp_15 = models.BooleanField('Expedition: Go West', default=False)
    exp_16 = models.BooleanField('Expedition: Galactic Nebula Expedition', default=False)
    exp_17 = models.BooleanField('Expedition: Colonia Core Circuit 3302', default=False)
    exp_18 = models.BooleanField('Expedition: Cassiopeia Project', default=False)
    exp_19 = models.BooleanField('Expedition: S.H.E.P.A.R.D. Mission', default=False)
    exp_20 = models.BooleanField('Expedition: Christmas Carriers Convoy', default=False)
    exp_21 = models.BooleanField('Expedition: Distant Stars - Unknown Origins', default=False)
    exp_22 = models.BooleanField('Expedition: Meet & Greet Expedition 2', default=False)
    exp_23 = models.BooleanField('Expedition: Heavy Weight Champions Circuit', default=False)
    exp_24 = models.BooleanField('Expedition: La Grande Expédition Remlok', default=False)
    exp_25 = models.BooleanField('Expedition: Mind The Gap', default=False)
    exp_26 = models.BooleanField('Expedition: Silly Ships Expedition', default=False)
    exp_27 = models.BooleanField('Expedition: Pioneers And Explorers', default=False)
    exp_28 = models.BooleanField('Expedition: Mercury 7 Expedition', default=False)
    exp_29 = models.BooleanField('Expedition: Helium Hunt', default=False)
    exp_30 = models.BooleanField("Expedition: Helicon's Peak Expedition", default=False)
    exp_31 = models.BooleanField('Expedition: Local Sightseeing Tour', default=False)
    exp_32 = models.BooleanField('Expedition: Azophi Expedition', default=False)
    exp_33 = models.BooleanField('Expedition: Silly Ships Expedition 2', default=False)
    exp_34 = models.BooleanField('Expedition: Summer Great Expedition', default=False)
    exp_35 = models.BooleanField('Expedition: Small Worlds Expedition 2', default=False)
    exp_36 = models.BooleanField('Expedition: Monoceros Mission', default=False)
    exp_37 = models.BooleanField('Expedition: Land Of Giants', default=False)
    exp_38 = models.BooleanField('Expedition: Grand Day Out', default=False)
    exp_39 = models.BooleanField('Expedition: Devos Expedition Program #1', default=False)
    exp_40 = models.BooleanField('Expedition: CCN Short Expedition', default=False)
    exp_41 = models.BooleanField('Expedition: Miskatonic University Galactic Expedition', default=False)
    exp_42 = models.BooleanField("Expedition: Dead End's Circumnavigation Expedition", default=False)
    exp_43 = models.BooleanField('Expedition: DSN Luxury Tour', default=False)
    exp_44 = models.BooleanField('Expedition: Distant Friends Expedition', default=False)
    exp_45 = models.BooleanField('Expedition: Minerva Centaurus Expedition', default=False)
    exp_46 = models.BooleanField('Expedition: Christmas Delights', default=False)
    exp_47 = models.BooleanField('Expedition: INRA Expedition', default=False)
    exp_48 = models.BooleanField('Expedition: Christmas Carriers Convoy 2', default=False)
    exp_49 = models.BooleanField('Expedition: Orange Run', default=False)
    exp_50 = models.BooleanField('Expedition: Enigma Expedition', default=False)
    exp_51 = models.BooleanField('Expedition: Beagle Point Expedition', default=False)
    exp_52 = models.BooleanField('Expedition: Perseus Survey', default=False)
    exp_53 = models.BooleanField('Expedition: Saud Kruger Buoy Tour', default=False)
    exp_54 = models.BooleanField('Expedition: Adder Tour', default=False)
    exp_55 = models.BooleanField('Expedition: A Fallen Commander', default=False)
    # endregion

    def __str__(self):
        return 'CMDR {cmdr}'.format(cmdr=self.cmdr_name)

    @classmethod
    def scrape_roster(cls):
        pass  # todo

import dateutil.parser
import gspread
from dateutil import tz
from django.contrib.auth.models import User
from django.db import models
from oauth2client.service_account import ServiceAccountCredentials
from tqdm import tqdm

from .utils import ChoiceEnum


# todo fixme note: get enums working


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

    class Role(ChoiceEnum):
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

    class Platform(ChoiceEnum):
        PC = 0
        XBOX = 1
        PS4 = 2
        MAC = 3

    class Ship(ChoiceEnum):
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

    # application number (pk)
    app_num = models.PositiveIntegerField('App. #', primary_key=True)

    # relationship
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    # commander info
    cmdr_name = models.CharField('Commander Name', max_length=25)

    # distant worlds 2 info (see roster)
    roster_num = models.PositiveSmallIntegerField('DW2 Roster #', unique=True)

    staff = models.BooleanField('Expedition staff', default=False)

    modified = models.DateTimeField()

    ship_model = models.CharField('Ship Model', max_length=16, choices=Ship.choices())
    ship_name = models.CharField('Ship Name', max_length=24, null=True, blank=True)
    call_sign = models.CharField('Ship ID', max_length=6)
    ship_range = models.FloatField('Jump Range (LY)')
    ship_showcase_link = models.CharField('Showcase Image Link', max_length=256, null=True, blank=True)
    livery = models.CharField('ship livery', max_length=48, null=True)

    comms_id = models.CharField('Comms Nickname', max_length=15, null=True)
    timezone = models.CharField('Timezone', max_length=8, null=True)
    platform = models.CharField('Platform', max_length=8, choices=Platform.choices(), default=Platform.PC.value)
    dwe_veteran = models.BooleanField('Participated in DWE 3302', default=False)
    visited_beagle_point = models.BooleanField('Has visited Beagle Point', default=False)

    role1 = models.IntegerField('Primary Role', choices=Role.choices(), default=Role.EXPL.value)
    role2 = models.IntegerField('Secondary Role', choices=Role.choices(), null=True)

    avg_playtime = models.CharField('Average hours played per week', max_length=16)

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
        # connect to google api
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('core/google_api_secret.json', scope)
        client = gspread.authorize(credentials)

        print('Connected to Google sheet.')
        print('Fetching data....', end='', flush=True)

        # get worksheet
        wbk = client.open('DW2 Roster Django Interface')
        roster = wbk.get_worksheet(0).get_all_records()
        print('done.')

        # helper dicts for switch case statements
        ships = {
            'Alliance Chieftain':   cls.Ship.CHIEFTAIN.value,
            'Anaconda':             cls.Ship.ANACONDA.value,
            'Asp Explorer':         cls.Ship.ASP_EXPLORER.value,
            'Asp Scout':            cls.Ship.ASP_SCOUT.value,
            'Beluga Liner':         cls.Ship.BELUGA.value,
            'Cobra Mk III':         cls.Ship.COBRA_MK_III.value,
            'Cobra Mk IV':          cls.Ship.COBRA_MK_IV.value,
            'Diamondback Explorer': cls.Ship.DIAMONDBACK_EXPLORER.value,
            'Diamondback Scout':    cls.Ship.DIAMONDBACK_SCOUT.value,
            'Dolphin':              cls.Ship.DOLPHIN.value,
            'Eagle Mk II':          cls.Ship.EAGLE.value,
            'Federal Assault Ship': cls.Ship.FEDERAL_ASSAULT_SHIP.value,
            'Federal Corvette':     cls.Ship.FEDERAL_CORVETTE.value,
            'Federal Dropship':     cls.Ship.FEDERAL_DROPSHIP.value,
            'Federal Gunship':      cls.Ship.FEDERAL_GUNSHIP.value,
            'Fer-De-Lance':         cls.Ship.FER_DE_LANCE.value,
            'Hauler':               cls.Ship.HAULER.value,
            'Imperial Clipper':     cls.Ship.IMPERIAL_CLIPPER.value,
            'Imperial Courier':     cls.Ship.IMPERIAL_COURIER.value,
            'Imperial Cutter':      cls.Ship.IMPERIAL_CUTTER.value,
            'Imperial Eagle':       cls.Ship.IMPERIAL_EAGLE.value,
            'Keelback':             cls.Ship.KEELBACK.value,
            'Krait':                cls.Ship.KRAIT.value,
            'Orca':                 cls.Ship.ORCA.value,
            'Python':               cls.Ship.PYTHON.value,
            'Sidewinder Mk I':      cls.Ship.SIDEWINDER.value,
            'Type-10 Defender':     cls.Ship.TYPE_10.value,
            'Type-6 Transporter':   cls.Ship.TYPE_6.value,
            'Type-7 Transporter':   cls.Ship.TYPE_7.value,
            'Type-9 Heavy':         cls.Ship.TYPE_9.value,
            'Viper Mk III':         cls.Ship.VIPER_MK_III.value,
            'Viper Mk IV':          cls.Ship.VIPER_MK_IV.value,
            'Vulture':              cls.Ship.VULTURE.value
        }
        roles = {
            'Explorer':             cls.Role.EXPL.value,
            'Fuel Rat':             cls.Role.RAT.value,
            'Miner':                cls.Role.MINER.value,
            'Fleet Mechanic':       cls.Role.MECH.value,
            'Tour Guide':           cls.Role.GUIDE.value,
            'Photographer':         cls.Role.PHOTO.value,
            'Fighter Escort':       cls.Role.ESCORT.value,
            'Geologist':            cls.Role.GEOL.value,
            'Scientist':            cls.Role.SCI.value,
            'Media':                cls.Role.MEDIA.value,
            'MediCorp':             cls.Role.MCORP.value,
            'Fleet Logistics':      cls.Role.LOGIST.value
        }

        # tqdm preferences
        tqdm_args = {
            'desc': 'Updating database',
            'total': len(roster),
            'leave': True,
            'unit': '',
            'unit_scale': True,
            'dynamic_ncols': True,
            'bar_format': '{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}]'
        }

        # counters
        created, updated = 0, 0

        # process roster
        for entry in tqdm(roster, **tqdm_args):

            # skip non-validated entries
            if entry['Validation'] != 'Validated':
                continue

            data = {
                'app_num': entry['Valid Application Number'],
                'roster_num': entry['Roster Number'],
                'modified': dateutil.parser.parse(entry['Application Date']).replace(tzinfo=tz.gettz("Europe/Paris")),
                'timezone': entry['Timezone'] if entry['Timezone'] != '' else None,

                'cmdr_name': entry['CMDR Name'],
                'comms_id': entry['Comms ID'] if entry['Comms ID'] != '' else None,

                'ship_model': ships.get(entry['Ship Type'], 'INVALID SHIP'),
                'ship_name': entry['Ship Name'] if entry['Ship Name'] != '' else None,
                'ship_range': entry['Ship Range'],
                'call_sign': entry['Call Sign'],
                'livery': entry['Livery'],

                'role1': roles.get(entry['Primary Role'], cls.Role.EXPL.value),
                'role2': roles.get(entry['Secondary Role'], None),

                'dwe_veteran': True if entry['DWE Veteran'] == 'Yes' else False,
                'visited_beagle_point': True if entry['BP Veteran'] == 'Yes' else False,

                'staff': True if entry['Staff'] == 'Yes' else False,

                'platform': entry['Platform'],
                'avg_playtime': entry['Gametime']
            }

            expeditions = [e.strip() for e in entry['Expeditions'].split(',')]  # trim whitespace around strings
            for exp in expeditions:  # this is vile please don't judge me
                if exp == "Nebulae Research Voyages":
                    data['exp_01'] = True
                elif exp == "REGOR Border Mapping":
                    data['exp_02'] = True
                elif exp == "Sagittarius-Carina Mission":
                    data['exp_03'] = True
                elif exp == "Dumbbell Project":
                    data['exp_04'] = True
                elif exp == "Distant Worlds 3302":
                    data['exp_05'] = True
                elif exp == "Formidine Rift Survey":
                    data['exp_06'] = True
                elif exp == "Meet & Greet Expedition":
                    data['exp_07'] = True
                elif exp == "Crab Nebula Expedition":
                    data['exp_08'] = True
                elif exp == "Borderlands Venture":
                    data['exp_09'] = True
                elif exp == "Western Expedition":
                    data['exp_10'] = True
                elif exp == "August Exodus - A Jaunt To Jaques":
                    data['exp_11'] = True
                elif exp == "Lost Stars - DWE XBox":
                    data['exp_12'] = True
                elif exp == "Formidine Rift Expedition":
                    data['exp_13'] = True
                elif exp == "Small Worlds Expedition":
                    data['exp_14'] = True
                elif exp == "Go West":
                    data['exp_15'] = True
                elif exp == "Galactic Nebula Expedition":
                    data['exp_16'] = True
                elif exp == "Colonia Core Circuit 3302":
                    data['exp_17'] = True
                elif exp == "Cassiopeia Project":
                    data['exp_18'] = True
                elif exp == "S.H.E.P.A.R.D. Mission":
                    data['exp_19'] = True
                elif exp == "Christmas Carriers Convoy":
                    data['exp_20'] = True
                elif exp == "Distant Stars - Unknown Origins":
                    data['exp_21'] = True
                elif exp == "Meet & Greet Expedition 2":
                    data['exp_22'] = True
                elif exp == "Heavy Weight Champions Circuit":
                    data['exp_23'] = True
                elif exp == "La Grande Expédition Remlok":
                    data['exp_24'] = True
                elif exp == "Mind The Gap":
                    data['exp_25'] = True
                elif exp == "Silly Ships Expedition":
                    data['exp_26'] = True
                elif exp == "Pioneers And Explorers":
                    data['exp_27'] = True
                elif exp == "Mercury 7 Expedition":
                    data['exp_28'] = True
                elif exp == "Helium Hunt":
                    data['exp_29'] = True
                elif exp == "Helicon's Peak Expedition":
                    data['exp_30'] = True
                elif exp == "Local Sightseeing Tour":
                    data['exp_31'] = True
                elif exp == "Azophi Expedition":
                    data['exp_32'] = True
                elif exp == "Silly Ships Expedition 2":
                    data['exp_33'] = True
                elif exp == "Summer Great Expedition":
                    data['exp_34'] = True
                elif exp == "Small Worlds Expedition 2":
                    data['exp_35'] = True
                elif exp == "Monoceros Mission":
                    data['exp_36'] = True
                elif exp == "Land Of Giants":
                    data['exp_37'] = True
                elif exp == "Grand Day Out":
                    data['exp_38'] = True
                elif exp == "Devos Expedition Program #1":
                    data['exp_39'] = True
                elif exp == "CCN Short Expedition":
                    data['exp_40'] = True
                elif exp == "Miskatonic University Galactic Expedition":
                    data['exp_41'] = True
                elif exp == "Dead End's Circumnavigation Expedition":
                    data['exp_42'] = True
                elif exp == "DSN Luxury Tour":
                    data['exp_43'] = True
                elif exp == "Distant Friends Expedition":
                    data['exp_44'] = True
                elif exp == "Minerva Centaurus Expedition":
                    data['exp_45'] = True
                elif exp == "Christmas Delights":
                    data['exp_46'] = True
                elif exp == "INRA Expedition":
                    data['exp_47'] = True
                elif exp == "Christmas Carriers Convoy 2":
                    data['exp_48'] = True
                elif exp == "Orange Run":
                    data['exp_49'] = True
                elif exp == "Enigma Expedition":
                    data['exp_50'] = True
                elif exp == "Beagle Point Expedition":
                    data['exp_51'] = True
                elif exp == "Perseus Survey":
                    data['exp_52'] = True
                elif exp == "Saud Kruger Buoy Tour":
                    data['exp_53'] = True
                elif exp == "Adder Tour":
                    data['exp_54'] = True
                elif exp == "A Fallen Commander":
                    data['exp_55'] = True

            # create/update Commander object
            cmdr, new = Commander.objects.update_or_create(app_num=entry['Valid Application Number'], defaults=data)

            # count
            if new:
                created += 1
            else:
                updated += 1

            cmdr.save()

        print("{:>4d} new records created".format(created))
        print("{:>4d} records updated".format(updated))

        # note: todo: when making profile page, make it READ ONLY - can only make changes via google form

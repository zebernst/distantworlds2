from django.contrib import admin

from .models import *


# Register your models here.
class CommanderAdmin(admin.ModelAdmin):
    search_fields = ['cmdr_name', 'comms_id', '=roster_num']
    autocomplete_fields = ['user']
    list_filter = ('staff', 'timezone', 'role1', 'role2', 'platform')

    def cmdr_display(self, obj):
        return "#{}: CMDR {}".format(obj.roster_num, obj.cmdr_name)
    cmdr_display.short_description = 'Commander'
    list_display = ('cmdr_display',)
    ordering = ('roster_num',)

    fieldsets = (
        ('DW2 Roster Info', {
            'fields': ('app_num', 'roster_num', 'user', 'cmdr_name', 'comms_id', 'timezone',
                       'role1', 'role2', 'platform', 'avg_playtime', 'staff', 'dwe_veteran',
                       'visited_beagle_point', 'modified')
        }),
        ('Ship', {
            'fields': ('ship_model', 'ship_name', 'call_sign', 'ship_range', 'ship_showcase_link', 'livery')
        }),
        ('Past Expeditions', {
            'classes': ('collapse',),
            'fields': ('exp_01', 'exp_02', 'exp_03', 'exp_04', 'exp_05', 'exp_06', 'exp_07', 'exp_08', 'exp_09',
                       'exp_10', 'exp_11', 'exp_12', 'exp_13', 'exp_14', 'exp_15', 'exp_16', 'exp_17', 'exp_18',
                       'exp_19', 'exp_20', 'exp_21', 'exp_22', 'exp_23', 'exp_24', 'exp_25', 'exp_26', 'exp_27',
                       'exp_28', 'exp_29', 'exp_30', 'exp_31', 'exp_32', 'exp_33', 'exp_34', 'exp_35', 'exp_36',
                       'exp_37', 'exp_38', 'exp_39', 'exp_40', 'exp_41', 'exp_42', 'exp_43', 'exp_44', 'exp_45',
                       'exp_46', 'exp_47', 'exp_48', 'exp_49', 'exp_50', 'exp_51', 'exp_52', 'exp_53', 'exp_54',
                       'exp_55')
        })
    )
    readonly_fields = ('modified',)
    empty_value_display = 'None'


admin.site.register(Commander, CommanderAdmin)
admin.site.register(Location)
admin.site.register(Waypoint)

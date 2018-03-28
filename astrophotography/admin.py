from django.contrib import admin

from astrophotography.models import Image


# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):

    def img_str(self, obj):
        return "Image Object ({}) [{}x{}]".format(obj.pk, obj.img_width, obj.img_height)
    img_str.short_description = 'Image'

    list_display = ('img_str', 'owner', 'waypoint', 'public', 'edited')
    list_filter = ('waypoint', 'public', 'edited')
    search_fields = ['owner__cmdr_name',
                     'waypoint__id', 'waypoint__name',
                     'desc']

    autocomplete_fields = ['owner']
    fieldsets = (
        ('Image File', {
            'fields': ('image', 'orig_filename', 'img_height', 'img_width')
        }),
        ('Image Meta', {
            'fields': ('owner', 'desc', 'location', 'waypoint', 'public', 'edited')
        }),
        ('Imgur', {
            'classes': ('collapse',),
            'fields': ('imgur_url', 'del_hash')
        })
    )
    readonly_fields = ('orig_filename', 'img_height', 'img_width')
    view_on_site = True

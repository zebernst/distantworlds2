from django.contrib import admin
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin import AdminImageMixin

from astrophotography.models import Image


# Register your models here.
@admin.register(Image)
class ImageAdmin(AdminImageMixin, admin.ModelAdmin):

    def thumb(self, obj):
        html = '<figure><img src="{href}" /><figcaption>Image {id} [{w}x{h}]</figcaption></figure>'
        return format_html(html.format(href=get_thumbnail(obj.image, "x150").url,
                                       id=obj.pk, w=obj.image.width, h=obj.image.height))
    thumb.short_description = 'Image'

    list_display = ('thumb', 'owner', 'waypoint', 'public', 'edited')
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

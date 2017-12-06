import urllib

from django.contrib import admin
from .models import Guest, Party, Function


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('phone_number','send_whatsapp')
    readonly_fields = ('send_whatsapp',)
    def send_whatsapp(self, obj):
        return "<a href="+obj.whatsapp_message+ ">Send Message on Whatsapp</a>"
    send_whatsapp.allow_tags = True


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'invitation_opened', 'invitation_link')
    list_filter = ('function', 'groom_invite', 'invitation_opened')
    inlines = [GuestInline]
    search_fields = ['name']

    def invitation_link(self, obj):
        return "<a href=" + obj.invitation_link + ">Invite</a>"
    invitation_link.allow_tags = True


class GuestAdmin(admin.ModelAdmin):
    list_display = ('party', 'email', 'is_attending', 'phone_number','send_whatsapp')
    list_filter = ('first_name', 'last_name','is_attending', 'party__is_invited', 'party__category', 'party__rehearsal_dinner')
    def send_whatsapp(self, obj):
        return "<a href="+obj.whatsapp_message+ ">Send Message on Whatsapp</a>"
    send_whatsapp.allow_tags = True
    search_fields = ['party__name']

class FunctionAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Function, FunctionAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)

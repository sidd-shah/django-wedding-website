from django.contrib import admin
from .models import Guest, Party, Function


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('phone_number',)


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'category', 'save_the_date_sent', 'invitation_sent', 'rehearsal_dinner', 'invitation_opened',
                    'is_invited', 'is_attending')
    list_filter = ('type', 'category', 'is_invited', 'is_attending', 'rehearsal_dinner', 'invitation_opened')
    inlines = [GuestInline]
    search_fields = ['name']


class GuestAdmin(admin.ModelAdmin):
    list_display = ('party', 'email', 'is_attending', 'phone_number')
    list_filter = ('first_name', 'last_name','is_attending', 'party__is_invited', 'party__category', 'party__rehearsal_dinner')


class FunctionAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Function, FunctionAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)

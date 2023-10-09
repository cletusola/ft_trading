from django.contrib import admin

from .models import Profile, Trade


# profile admin 
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['firstname','lastname','username','email','date']
    list_display_links = ['firstname','lastname','username','email']

admin.site.register(Profile,ProfileAdmin)


# trade admin 
class TradeAdmin(admin.ModelAdmin):
    list_display = ['profit_or_loss','user','time','date']
    list_display_links = ['profit_or_loss','user','time']


admin.site.register(Trade,TradeAdmin)
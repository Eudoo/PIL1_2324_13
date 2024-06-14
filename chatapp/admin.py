from django.contrib import admin
from chatapp.models import Room, Messages

# Register your models here.

admin.site.register(Messages)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
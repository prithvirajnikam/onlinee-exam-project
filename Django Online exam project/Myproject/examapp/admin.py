from django.contrib import admin
from .models import Questions,UserData

# Register your models here.
admin.site.register( Questions)


@admin.register(UserData)
class useradmin(admin.ModelAdmin):
    list_display=('username','percentage','subject')
    search_fields=('username','subject')

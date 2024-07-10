from django.contrib import admin

from rpd.models import ExceptionNames, AllowedNames


# Register your models here.
@admin.register(ExceptionNames)
class ExceptionNamesAdmin(admin.ModelAdmin):
    pass


@admin.register(AllowedNames)
class AllowedNamesAdmin(admin.ModelAdmin):
    pass
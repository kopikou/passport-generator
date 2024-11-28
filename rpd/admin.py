from django.contrib import admin

from rpd.models import ExceptionNames, AllowedNames, BaseDocuments, RPDFile


# Register your models here.
@admin.register(ExceptionNames)
class ExceptionNamesAdmin(admin.ModelAdmin):
    pass


@admin.register(AllowedNames)
class AllowedNamesAdmin(admin.ModelAdmin):
    pass


@admin.register(BaseDocuments)
class BaseDocumentsAdmin(admin.ModelAdmin):
    pass


@admin.register(RPDFile)
class RPDFileAdmin(admin.ModelAdmin):
    pass
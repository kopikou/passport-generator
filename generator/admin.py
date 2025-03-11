from django.contrib import admin

from generator.models import ScientificDataDefault, ScientificWorkType


# Register your models here.
@admin.register(ScientificDataDefault)
class ScientificDataDefaultAdmin(admin.ModelAdmin):
    pass

@admin.register(ScientificWorkType)
class ScientificWorkTypeAdmin(admin.ModelAdmin):
    pass
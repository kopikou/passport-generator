from django.contrib import admin

from ind_plan.models import Work


# Register your models here.
@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    class Meta:
        model = Work
        fields = "__all__"

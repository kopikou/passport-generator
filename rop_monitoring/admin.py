from django.contrib import admin

from rop_monitoring.models import Indicator, RopMonitoring, RopMonitoringScore


@admin.register(RopMonitoring)
class RopMonitoringAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


@admin.register(RopMonitoringScore)
class RopMonitoringScoreAdmin(admin.ModelAdmin):
    search_fields = ["rop_monitoring__name", "admission", "person", "indicator__name"]

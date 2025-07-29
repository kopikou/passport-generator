from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from rop_monitoring.models import Indicator, RopMonitoring, RopMonitoringScore, AdmissionKinds


class IndicatorForm(forms.ModelForm):
    admission_kinds = forms.MultipleChoiceField(
        choices=AdmissionKinds.choices,
        widget=FilteredSelectMultiple(
            "Типы ООП",
            is_stacked=False
        ),
    )

    def clean_admission_kinds(self):
        return [int(i) for i in self.cleaned_data['admission_kinds']]

    class Meta:
        model = Indicator
        fields = '__all__'


class AdmissionKindsListFilter(admin.SimpleListFilter):
    title = _('Типы ООП')
    parameter_name = 'admission_kinds'

    def lookups(self, request, model_admin):
        return [(choice.value, choice.label) for choice in AdmissionKinds]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(admission_kinds__contains=[int(self.value())])
        return queryset


@admin.register(RopMonitoring)
class RopMonitoringAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["id", "name", "description", "get_admission_kinds_display"]
    list_filter = (AdmissionKindsListFilter,)
    form = IndicatorForm


@admin.register(RopMonitoringScore)
class RopMonitoringScoreAdmin(admin.ModelAdmin):
    search_fields = ["rop_monitoring__name", "admission", "person", "indicator__name"]
    list_display = ["rop_monitoring", "admission", "person", "indicator", "score", "value"]

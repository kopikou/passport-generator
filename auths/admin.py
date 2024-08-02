from django.contrib import admin
from django.forms import ModelForm
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from app.utils import CheckboxSelectMultipleEx
from auths.models import UserProfile, Permissions

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    class Form(ModelForm):
        class Meta:
            model = UserProfile
            fields = "__all__"
            widgets = {
                'permissions': CheckboxSelectMultipleEx(choices=Permissions.choices)
            }

    form = Form
    search_fields = ['user__last_name', 'user__first_name']
    change_list_template = "loginas/change_list.html"
    list_display = ["user", "get_user__last_name", "get_user__first_name", "buttons", "mira_id", "is_student", "is_teacher", "bitrix_user_id"]
    list_filter = ["is_student", "is_teacher"]

    @admin.display(ordering='user__last_name', description='Фамилия')
    def get_user__last_name(self, obj):
        return obj.user.last_name

    @admin.display(ordering='user__first_name', description='Имя')
    def get_user__first_name(self, obj):
        return obj.user.first_name

    def buttons(self, obj):
        out = render_to_string('loginas/userprofile_loginas_button.html', {
            "object_id": obj.user.id
        })
        return mark_safe(out)

    buttons.short_description = 'Action'
    buttons.allow_tags = True
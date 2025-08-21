from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from arim.models import CatPerson
from auths.models import Permissions


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):

       mira_data = CatPerson.objects.get(id=user.esiauser.mira_id)

       if mira_data:
              name = mira_data.name.split(' ')

              user.userprofile.name = mira_data.name
              user.userprofile.middle_name = ' '.join(name[2:])
              user.userprofile.mira_id = mira_data.id

              if 'student' in user.esiauser.types:
                     user.is_student = True
              if 'employee' in user.esiauser.types:
                     user.is_teacher = True
                     user.userprofile.permissions = [Permissions.can_edit_rpd, Permissions.can_use_generator]

              user.userprofile.save()
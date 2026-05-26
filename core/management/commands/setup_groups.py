from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Crea grupos y asigna permisos para el sistema de autenticación"

    def handle(self, *args, **options):
        User = get_user_model()
        user_ct = ContentType.objects.get_for_model(User)

        perms_view_user = Permission.objects.get(
            codename="view_user", content_type=user_ct)
        perms_change_user = Permission.objects.get(
            codename="change_user", content_type=user_ct)

        group_viewers, _ = Group.objects.get_or_create(name="Viewers")
        group_viewers.permissions.add(perms_view_user)

        group_moderators, _ = Group.objects.get_or_create(name="Moderators")
        group_moderators.permissions.add(perms_view_user, perms_change_user)

        self.stdout.write(self.style.SUCCESS(
            "✓ Grupos creados: Viewers (auth.view_user), Moderators (auth.view_user + auth.change_user)"
        ))

        demo_user, created = User.objects.get_or_create(
            username="demo_user",
            defaults={"email": "demo@example.com"},
        )
        if created:
            demo_user.set_password("demo1234")
            demo_user.save()
            group_viewers.user_set.add(demo_user)
            self.stdout.write(self.style.SUCCESS(
                "✓ Usuario demo 'demo_user' creado (password: demo1234) en grupo Viewers"
            ))
        else:
            self.stdout.write("ℹ El usuario 'demo_user' ya existe")

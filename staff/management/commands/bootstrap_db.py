import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from staff.constants import SUPERUSER_STAFF_CODE
from staff.models import CoreUser, Role, Staff


class Command(BaseCommand):
    help = "Creating SuperUser Staff member"

    def add_arguments(self, parser):
        pass

    @transaction.atomic()
    def handle(self, *args, **options):

        self.create_roles()

        self.create_super_user()

    def create_roles(self):
        roles = ["SuperUser", "Junior", "Mid", "Senior", "Intern"]
        for role_title in roles:
            role = Role()
            role.title = role_title
            role.save()
            self.stdout.write(
                self.style.SUCCESS(f"Role created successfully! {str(role)}")
            )

    def create_super_user(self) -> Staff:
        core_user = self._django_user(
            username="SuperUser",
            password=None,
            email="superuser@localhost.com",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        su_role = Role.objects.get(slug="superuser")

        staff_member = self._create_staff_member(
            core_user=core_user,
            name="SuperUser",
            code=SUPERUSER_STAFF_CODE,
            role=su_role,
        )

        self.stdout.write(
            self.style.SUCCESS("SuperUser Staff Member successfully created!")
        )
        return staff_member

    @staticmethod
    def _django_user(
        username: str,
        password: [None, str],
        email: str,
        is_superuser: bool = False,
        is_active: bool = True,
        is_staff: bool = False,
    ) -> CoreUser:
        new_core_user = CoreUser()
        new_core_user.username = username

        if not password:
            password = "admin"  # nosec

        new_core_user.set_password(password)

        new_core_user.email = email

        new_core_user.is_active = is_active
        new_core_user.is_superuser = is_superuser
        new_core_user.is_staff = is_staff

        new_core_user.save()

        return new_core_user

    @staticmethod
    def _create_staff_member(
        core_user: CoreUser,
        name: str,
        code: str,
        role: Role,
        supervisor: CoreUser = None,
        joining_date: datetime.date = datetime.datetime.today().date(),
    ):
        new_staff = Staff()
        new_staff.id = core_user
        new_staff.name = name
        new_staff.code = code
        new_staff.role = role
        new_staff.supervisor = supervisor
        new_staff.joining_date = joining_date
        new_staff.save()

        return new_staff

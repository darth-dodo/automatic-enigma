import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from staff.constants import SUPERUSER_STAFF_CODE
from staff.models import CoreUser, Role, Staff

fake = Faker()


class Command(BaseCommand):
    help = "Creating SuperUser Staff member"

    def add_arguments(self, parser):
        pass

    @transaction.atomic()
    def handle(self, *args, **options):

        # self.create_roles()

        # self.create_super_user()

        self.create_staff()

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
        username: str = None,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        is_superuser: bool = False,
        is_active: bool = True,
        is_staff: bool = False,
    ) -> CoreUser:
        new_core_user = CoreUser()

        fake_first_name = fake.first_name()
        fake_last_name = fake.last_name()

        new_core_user.username = (
            username if username else f"{fake.first_name()}.{fake.last_name()}".lower()
        )
        new_core_user.first_name = first_name if first_name else fake_first_name
        new_core_user.last_name = last_name if last_name else fake_last_name

        if not password:
            password = "admin"  # nosec

        new_core_user.set_password(password)

        new_core_user.email = email if email else f"{new_core_user.username}@email.com"

        new_core_user.is_active = is_active
        new_core_user.is_superuser = is_superuser
        new_core_user.is_staff = is_staff

        new_core_user.save()

        return new_core_user

    def _create_staff_member(
        self,
        core_user: CoreUser,
        role: Role,
        name: str = None,
        code: str = None,
        supervisor: CoreUser = None,
        joining_date: datetime.date = datetime.datetime.today().date(),
    ):
        new_staff = Staff()
        new_staff.id = core_user
        new_staff.name = (
            name if name else f"{core_user.first_name} {core_user.last_name}"
        )
        new_staff.code = code if code else core_user.username[:5].upper()
        new_staff.role = role
        new_staff.supervisor = supervisor
        new_staff.joining_date = joining_date
        new_staff.save()

        self.style.SUCCESS(f"Staff created successfully! {str(new_staff)}")

        return new_staff

    def create_mid_level(self):
        mid_level = Role.objects.get(slug="mid")
        self._create_staff_by_level(mid_level)

    def create_senior_level(self):
        senior_level = Role.objects.get(slug="senior")
        self._create_staff_by_level(senior_level)

    def create_intern_level(self):
        intern_level = Role.objects.get(slug="intern")
        self._create_staff_by_level(intern_level)

    def _create_staff_by_level(self, role_level: Role):
        django_user = self._django_user()
        self._create_staff_member(core_user=django_user, role=role_level)

        self.stdout.write(
            self.style.SUCCESS(f"{role_level.title} level Staff successfully created!")
        )

    def create_staff(self):

        senior = 1
        mid = 3
        intern = 5

        for i in range(1, senior + 1):
            self.create_senior_level()

        for i in range(1, mid + 1):
            self.create_mid_level()

        for i in range(1, intern + 1):
            self.create_intern_level()


from django.contrib.auth.models import UserManager
from django.db.models import QuerySet
from django.db.models import Q


class CustomUserManager(UserManager):
    def get_queryset(self):
        return CustomUserQuerySet(self.model, using=self._db)

    def active_users(self):
        return self.get_queryset().active_users()

    def inactive_users(self):
        return self.get_queryset().inactive_users()

    def staff_users(self):
        return self.get_queryset().staff_users()


class CustomUserQuerySet(QuerySet):
    def active_users(self):
        return self.filter(Q(is_active=True))

    def inactive_users(self):
        return self.filter(Q(is_active=False))

    def staff_users(self):
        return self.filter(Q(is_staff=True))






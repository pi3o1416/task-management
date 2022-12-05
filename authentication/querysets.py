
from django.db.models import QuerySet
from django.db.models import Q


class CustomUserQuerySet(QuerySet):
    def active_users(self):
        return self.filter(Q(is_active=True))

    def inactive_users(self):
        return self.filter(Q(is_active=False))

    def staff_users(self):
        return self.filter(Q(is_staff=True))






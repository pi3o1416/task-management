
from django.db.models import QuerySet, Q


class EmailHistoryQuerySet(QuerySet):
    def success_emails(self):
        return self.filter(Q(email_status=self.model.EmailStatus.SUCCESS))

    def failed_emails(self):
        return self.filter(Q(email_status=self.model.EmailStatus.FAILURE))


























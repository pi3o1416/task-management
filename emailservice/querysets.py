
from django.db.models import QuerySet, Q


class EmailHistoryQuerySet(QuerySet):
    def success_emails(self):
        return self.filter(Q(email_status=self.model.EmailStatus.SUCCESS))

    def failed_emails(self):
        return self.filter(Q(email_status=self.model.EmailStatus.FAILURE))

    def activate_account_emails(self):
        #TODO: Move ACTIVE_ACCOUNT_EMAIL_SUBJECT to settings
        try:
            from authentication.services import ACTIVE_ACCOUNT_EMAIL_SUBJECT as subject
            return self.filter(Q(email_subject=subject))
        except:
            return self.none()

    def password_reset_emails(self):
        #TODO: Move PASSWORD_RESET_EMIAL_SUBJECT to settings
        try:
            from authentication.services import PASSWORD_RESET_EMIAL_SUBJECT as subject
            return self.filter(Q(email_subject=subject))
        except:
            return self.none()




























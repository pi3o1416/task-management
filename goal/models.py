
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

from department.models import Department
from services.exceptions import InvalidRequest

from .querysets import GoalQuerySet
from .validators import validate_completion, validate_year

# Create your models here.

class Goal(models.Model):
    class ReviewStatusChoices(models.TextChoices):
        ACCEPTED = "ACC", _("Accepted")
        PENDING = "Pen", _("Pending")


    class QuarterChoices(models.IntegerChoices):
        QUARTER1 = 1, _("Quarter 1")
        QUARTER2 = 2, _("Quarter 2")
        QUARTER3 = 3, _("Quarter 3")
        QUARTER4 = 4, _("Quarter 4")

    error_messages = {
        "CREATE": "Goal create failed.",
        "UPDATE": "Goal update failed.",
        "DELETE": "Goal delete failed.",
        "RETRIEVE": "Goal retrieve failed.",
        "PATCH": "Goal patch failed.",
    }

    department = models.ForeignKey(
        verbose_name=_("Department"),
        to=Department,
        on_delete=models.CASCADE,
        related_name='department_goals'
    )
    title = models.CharField(
        max_length=300,
        verbose_name=_("Quarter Goal Title"),
    )
    description = models.TextField(
        verbose_name=_("Goal Description"),
    )
    year = models.IntegerField(
        verbose_name=_("Goal Year"),
        validators=[validate_year],
    )
    quarter = models.IntegerField(
        verbose_name=_("Year Quarter"),
        choices=QuarterChoices.choices,
    )
    review_status = models.CharField(
        max_length=10,
        verbose_name=_("Goal Review Status"),
        choices=ReviewStatusChoices.choices,
        default=ReviewStatusChoices.PENDING,
    )
    review = models.TextField(
        verbose_name=_("Review under goal"),
        null=True,
        blank=True,
    )
    completion = models.IntegerField(
        verbose_name=_("Goal total completion on percentage"),
        validators=[validate_completion],
        default=0
    )
    objects = GoalQuerySet().as_manager()
    class Meta:
        permissions = (("can_add_review", _("Can Add Review")),
                       ("can_change_status", _("Can Change Status")))

    def __str__(self):
        return self.title

    def accept_goal(self):
        #TODO: Put operation on hold for undoing
        self.review_status = self.ReviewStatusChoices.ACCEPTED
        self.save()

    def set_status_pending(self):
        #TODO: Put operation on hold for undoing
        self.review_status = self.ReviewStatusChoices.PENDING
        self.save()

    def update_completion_percentage(self, percentage):
        self.completion = percentage
        self.save()

    def add_review(self, review):
        self.review = review
        self.save()

    def delete_review(self):
        self.review = None
        self.save()

    def safe_delete(self):
        try:
            self.delete()
        except Exception as exception:
            raise APIException({"detail": exception.args})

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
        try:
            goal = cls(
                **kwargs
            )
            if commit == True:
                goal.save()
            return goal
        except Exception as exception:
            raise InvalidRequest(
                detail={"detail": _(cls.error_messages["CREATE"] + exception.__str__())}
            )






















from django.db import models
from django.utils.translation import gettext_lazy as _

from department.models import Department
from .validators import validate_completion, validate_year

# Create your models here.

class Goal(models.Model):
    class ReviewStatusChoices(models.TextChoices):
        ACCEPTED = "ACC", _("Accepted")
        PENDING = "Pen", _("Pending")


    class QuarterChoices(models.TextChoices):
        QUARTER1 = "Q1", _("Quarter 1")
        QUARTER2 = "Q2", _("Quarter 2")
        QUARTER3 = "Q3", _("Quarter 3")
        QUARTER4 = "Q4", _("Quarter 4")


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
    quarter = models.CharField(
        max_length=10,
        verbose_name=_("Year Quarter"),
    )
    review_status = models.CharField(
        max_length=10,
        verbose_name=_("Goal Review Status"),
    )
    review = models.TextField(
        verbose_name=_("Review under goal")
    )
    completion = models.IntegerField(
        verbose_name=_("Goal total completion on percentage"),
        validators=[validate_completion]
    )
    class Meta:
        permissions = (("can_add_review", _("Can Add Review")),
                       ("can_change_status", _("Can Change Status")))

    def __str__(self):
        return self.title

















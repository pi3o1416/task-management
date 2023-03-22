
from django.db import models
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from department.models import Department, DepartmentMember
from services.mixins import ModelUpdateMixin
from services.exceptions import InvalidRequest
from .exceptions import ReviewCreateFailed, GoalDeleteFailed, GoalCreateFailed
from .querysets import GoalQuerySet
from .validators import validate_completion, validate_year


User = get_user_model()


class Goal(ModelUpdateMixin, models.Model):
    restricted_fields = ['pk', 'created_by', 'department']

    class ReviewStatusChoices(models.TextChoices):
        ACCEPTED = "ACC", _("Accepted")
        PENDING = "Pen", _("Pending")
        REJECTED = "REJ", _("Rejected")


    class QuarterChoices(models.IntegerChoices):
        QUARTER1 = 1, _("Quarter 1")
        QUARTER2 = 2, _("Quarter 2")
        QUARTER3 = 3, _("Quarter 3")
        QUARTER4 = 4, _("Quarter 4")

    created_by = models.ForeignKey(
        verbose_name=_("Created by"),
        to=User,
        on_delete=models.RESTRICT,
        related_name='created_goals'
    )
    department = models.ForeignKey(
        verbose_name=_("Department"),
        to=Department,
        on_delete=models.CASCADE,
        related_name='department_goals'
    )
    title = models.CharField(
        max_length=300,
        verbose_name=_("Title"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    year = models.IntegerField(
        verbose_name=_("Year"),
        validators=[validate_year],
    )
    quarter = models.IntegerField(
        verbose_name=_("Quarter"),
        choices=QuarterChoices.choices,
    )
    status = models.CharField(
        max_length=10,
        verbose_name=_("Status"),
        choices=ReviewStatusChoices.choices,
        default=ReviewStatusChoices.PENDING,
    )
    completion = models.IntegerField(
        verbose_name=_("Goal total completion on percentage"),
        validators=[validate_completion],
        default=0
    )
    objects = GoalQuerySet().as_manager()
    class Meta:
        permissions = (("can_change_status", _("Can Change Status")),
                       ("can_view_all_goals", _("Can View All Goals")),)

    def clean(self, update_fields=None):
        #Validate rejected goals can not be updated
        if update_fields != None and 'status' not in update_fields and self.status == self.ReviewStatusChoices.REJECTED:
            raise ValidationError("Rejecte goal can not be updated")
        #Validate completion should be 0 untill review status is not updated to accepted
        if self.status != self.ReviewStatusChoices.PENDING and self.completion != 0:
            raise ValidationError("Goal completion should be 0 when review status pending")
        #Validate created by user department and goal department need to be same
        if update_fields == None or 'department' in update_fields:
            breakpoint()
            member_pk = model_to_dict(self).get('created_by')
            member_department_pk = DepartmentMember.objects.member_department(member_pk=member_pk)
            goal_department_pk = model_to_dict(self).get('department')
            if goal_department_pk != member_department_pk:
                raise ValidationError("Goal department and created by user department did not match")

    def delete(self):
        if self.status != self.ReviewStatusChoices.PENDING:
            raise GoalDeleteFailed(detail="Goal can not be deleted once status change from pending.")
        return super().delete()

    def save(self, **kwargs):
        self.clean(**kwargs)
        return super(Goal, self).save(**kwargs)

    def accept_goal(self):
        if self.status != self.ReviewStatusChoices.ACCEPTED:
            self.update(status=self.ReviewStatusChoices.ACCEPTED)
            return True
        raise InvalidRequest("Goal status already set to accepted")

    def reject_goal(self):
        if self.status != self.ReviewStatusChoices.REJECTED:
            self.update(status=self.ReviewStatusChoices.REJECTED)
            return True
        raise InvalidRequest("Goal status already set to rejected")

    def update_completion_percentage(self, percentage):
        if self.completion != percentage:
            self.update(completion=percentage)
            return True
        raise InvalidRequest("Goal completion percentage already set to {}".format(percentage))

    def __str__(self):
        return self.title

    def get_edit_history(self):
        try:
            return self.edit_history
        except ObjectDoesNotExist:
            return None


    @classmethod
    def create_factory(cls, created_by, commit=True, **kwargs):
        try:
            required_fields = ['department', 'title', 'description', 'year', 'quarter']
            for field in required_fields:
                assert kwargs.get(field), "{} can not be null".format(field)
            goal = cls(created_by = created_by, **kwargs)
            if commit == True:
                goal.save()
            return goal
        except AssertionError as exception:
            raise GoalCreateFailed(detail="Goal create faield. " + exception.__str__())
        except IntegrityError as exception:
            raise GoalCreateFailed(detail="Goal create failed due to integrigy error")
        except Exception as exception:
            raise GoalCreateFailed(detail="Goal create faield. " + exception.__str__())


class GoalLastEdit(models.Model):
    goal = models.OneToOneField(
        to=Goal,
        on_delete=models.CASCADE,
        verbose_name=_("Goal"),
        related_name='edit_history'
    )
    edited_by = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='goal_edits',
        verbose_name=_("Edited by")
    )
    edited_at = models.DateTimeField(
        verbose_name=_("Edited at"),
        auto_now_add=True,
    )


class Review(models.Model):
    goal = models.ForeignKey(
        to=Goal,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_("Goal"),
    )
    review = models.TextField(
        verbose_name=_("Review"),
    )
    reviewed_by = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='added_reviews',
        verbose_name=_("Reviewed by")
    )
    reviewed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Reviewed at"),
    )

    def clean(self):
        #Validate only user with review add permission and
        #Goal department member with goal create permission can add review
        user = self.reviewed_by
        if not user.has_perm('review.add_review'):
            goal_department_pk = model_to_dict(self.goal).get('department')
            user_department_pk = model_to_dict(user.user_department).get('department')
            if not (user_department_pk == goal_department_pk and user.has_perm('goal.add_goal')):
                raise ValidationError(_("Reviewer does not have permission to add review."))
        #Validate review update is restricted
        if self.pk != None:
            raise ValidationError("Review update is restricted")

    def save(self, **kwargs):
        self.clean()
        return super(Review, self).save(**kwargs)

    @classmethod
    def create_factory(cls, reviewed_by, commit=True, **kwargs):
        try:
            assert kwargs.get('goal'), "Goal cannot be None"
            assert kwargs.get("review"), "Review text cannot be None"
            review = cls(
                reviewed_by=reviewed_by,
                **kwargs
            )
            if commit == True:
                review.save()
            return review
        except AssertionError as exception:
            raise ReviewCreateFailed(detail="Review create faield" + exception.__str__())
        except IntegrityError as exception:
            raise ReviewCreateFailed(detail="Review create failed due to integrigy error")
        except Exception as exception:
            raise ReviewCreateFailed(detail="Review creaate faield" + exception.__str__())


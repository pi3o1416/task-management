
from django.contrib.auth import get_user_model
from rest_framework import serializers

from department.models import Department
from department.serializers import DepartmentMinimalSerializer
from ..models import Team


User = get_user_model()


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['pk', 'title', 'description', 'department', 'team_lead']
        read_only_fields = ['pk', 'department']

    def create(self, department, commit=True):
        assert self.validated_data != None, "Validate serializer before create team instance"
        team_instance = Team.create_factory(**self.validated_data, department=department, commit=commit)
        return team_instance


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['pk', 'title', 'description', 'department', 'team_lead']
        read_only_fields = ['pk', 'department']

    def update(self):
        assert self.validated_data != None, "Validate serializer before update"
        assert self.instance != None, "Initialize serilaizer with team instance"
        assert type(self.instance) is Team, "Instance should be an instance of team"
        self.instance.update(**self.validated_data)


class TeamDetailSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    team_lead = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['pk', 'title', 'description', 'department', 'team_lead']

    def get_department(self, team):
        department_pk = team.department_id
        department = Department.objects.get_object_from_cache(pk=department_pk)
        serializer = DepartmentMinimalSerializer(instance=department)
        return serializer.data

    def get_team_lead(self, team):
        team_lead_pk = team.team_lead_id
        team_lead = User.objects.get_object_from_cache(pk=team_lead_pk)
        serializer = UserMinimalSerializer(instance=team_lead)
        return serializer.data


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [*User.CACHED_FIELDS]








from rest_framework import serializers

from ..models import Task, TaskTree


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['pk', 'created_by', 'title', 'description', 'created_at', 'last_date',
                  'approved_by_dept_head', 'status', 'priority', 'created_by_user_username',
                  'created_by_user_fullname']
        read_only_fields = ['pk', 'created_by', 'created_at', 'created_by_user_username',
                            'created_by_user_fullname', 'approved_by_dept_head', 'status']

    def create(self, commit=True):
        assert self.validated_data != None, "Validated serialzier before create object"
        task = Task(**self.validated_data)
        if commit == True:
            task.save()
        return task

#    def update(self, instance, commit = True):
#        assert self.validated_data != None, "Validate serializer before update"
#        assert type(instance) is Task, "Should be an instance of Task model"
#        instance.title = self.validated_data["title"]
#        instance.description = self.validated_data["description"]
#        instance.last_date = self.validated_data["last_date"]
#        instance.priority = self.validated_data["priority"]
#        if commit:
#            instance.save(update_fields=['title', 'description', 'status', 'last_date'])
#        return instance

# Generated by Django 4.1.3 on 2023-03-02 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('task', '0021_alter_task_description'),
        ('department', '0013_remove_departmentmember_member_full_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_tasks', to='department.department', verbose_name='Department')),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to_dept', to='task.task', verbose_name='Task')),
            ],
            options={
                'permissions': (('can_create_department_task', 'Can Create Department Task'), ('can_manage_departmnet_task', 'Can Manage Department Task')),
            },
        ),
    ]
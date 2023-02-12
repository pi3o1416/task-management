# Generated by Django 4.1.3 on 2023-02-08 10:38

from django.db import migrations, models
import project.validators


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_alter_project_project_manager_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='budget',
            field=models.DecimalField(decimal_places=10, max_digits=20, validators=[project.validators.validate_budget], verbose_name='Project Budget'),
        ),
    ]
# Generated by Django 5.1.4 on 2024-12-16 11:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_alter_order_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="robot_serial",
            new_name="serial",
        ),
        migrations.AddField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="is_handled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="order",
            name="is_waiting",
            field=models.BooleanField(default=False),
        ),
    ]
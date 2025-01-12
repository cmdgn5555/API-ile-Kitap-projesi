# Generated by Django 5.0.8 on 2025-01-03 11:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitaplar', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='yorum',
            name='yorum_sahibi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kullanici_yorumlari', to=settings.AUTH_USER_MODEL),
        ),
    ]
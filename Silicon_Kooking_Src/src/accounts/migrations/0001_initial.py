# Generated by Django 2.0.1 on 2018-03-10 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(db_column='recipe', on_delete=django.db.models.deletion.PROTECT, to='recipes.Recipe')),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorite',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, db_column='avatar', default='profile-img/default.jpg', upload_to='profile-img/')),
                ('user', models.ForeignKey(db_column='user', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profile_image',
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('recipe', 'user')},
        ),
    ]

# Generated by Django 2.0.1 on 2018-03-10 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100, null=True)),
            ],
            options={
                'db_table': 'cuisine',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CuisineRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(db_column='name', on_delete=django.db.models.deletion.PROTECT, to='recipes.Cuisine')),
            ],
            options={
                'db_table': 'cuisine_recipe',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=200, null=True)),
            ],
            options={
                'db_table': 'ingredient',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(db_column='ingredient', on_delete=django.db.models.deletion.PROTECT, to='recipes.Ingredient')),
            ],
            options={
                'db_table': 'ingredient_recipe',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MealType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(db_column='type', max_length=100, null=True)),
            ],
            options={
                'db_table': 'meal_type',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MealTypeRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'meal_type_recipe',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=200, null=True)),
                ('description', models.TextField(db_column='description', null=True)),
                ('static_image', models.ImageField(blank=True, db_column='static_image', default='images/default/default.jpg', upload_to='images')),
                ('web_image', models.CharField(blank=True, db_column='web_image', max_length=1000, null=True)),
                ('ingredients', models.TextField(db_column='ingredients', null=True)),
                ('ingredientList', models.TextField(db_column='ingredientList', null=True)),
                ('instructions', models.TextField(db_column='instructions', null=True)),
                ('cuisine', models.CharField(db_column='cuisine', max_length=1000, null=True)),
                ('type', models.CharField(db_column='type', max_length=1000, null=True)),
                ('author', models.CharField(db_column='author', max_length=200, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('tags', models.TextField(db_column='tags', null=True)),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'recipe',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RecipesRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=200)),
                ('updated', models.DateTimeField(db_column='updated')),
                ('timestamp', models.DateTimeField(db_column='timestamp')),
            ],
            options={
                'db_table': 'recipes_recipe',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SimilarIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=200, null=True)),
                ('similar', models.ForeignKey(db_column='similar', on_delete=django.db.models.deletion.PROTECT, to='recipes.Ingredient')),
            ],
            options={
                'db_table': 'similar_ingredient',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='mealtyperecipe',
            name='recipe',
            field=models.ForeignKey(db_column='recipe', on_delete=django.db.models.deletion.PROTECT, to='recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='mealtyperecipe',
            name='type',
            field=models.ForeignKey(db_column='type', on_delete=django.db.models.deletion.PROTECT, to='recipes.MealType'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(db_column='recipe', on_delete=django.db.models.deletion.PROTECT, to='recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='cuisinerecipe',
            name='recipe',
            field=models.ForeignKey(db_column='recipe', on_delete=django.db.models.deletion.PROTECT, to='recipes.Recipe'),
        ),
        migrations.AlterUniqueTogether(
            name='mealtyperecipe',
            unique_together={('recipe', 'type')},
        ),
        migrations.AlterUniqueTogether(
            name='ingredientrecipe',
            unique_together={('recipe', 'ingredient')},
        ),
        migrations.AlterUniqueTogether(
            name='cuisinerecipe',
            unique_together={('recipe', 'name')},
        ),
    ]

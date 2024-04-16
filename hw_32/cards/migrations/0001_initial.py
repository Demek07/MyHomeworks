# Generated by Django 4.2 on 2024-03-27 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(db_column='CardID', primary_key=True, serialize=False)),
                ('question', models.CharField(db_column='Question', max_length=255)),
                ('answer', models.TextField(db_column='Answer', max_length=5000)),
                ('upload_date', models.DateTimeField(auto_now_add=True, db_column='UploadDate')),
                ('views', models.IntegerField(db_column='Views', default=0)),
                ('adds', models.IntegerField(db_column='Favorites', default=0)),
            ],
            options={
                'verbose_name': 'Карточка',
                'verbose_name_plural': 'Карточки',
                'db_table': 'Cards',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(db_column='CategoryID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=100)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(db_column='TagID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=100)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'db_table': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='CardTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(db_column='CardID', on_delete=django.db.models.deletion.CASCADE, to='cards.card')),
                ('tag', models.ForeignKey(db_column='TagID', on_delete=django.db.models.deletion.CASCADE, to='cards.tag')),
            ],
            options={
                'verbose_name': 'Тег карточки',
                'verbose_name_plural': 'Теги карточек',
                'db_table': 'CardTags',
                'unique_together': {('card', 'tag')},
            },
        ),
        migrations.AddField(
            model_name='card',
            name='tags',
            field=models.ManyToManyField(db_column='Tags', related_name='cards', through='cards.CardTag', to='cards.tag'),
        ),
    ]
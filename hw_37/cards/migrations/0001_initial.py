# Generated by Django 5.0.6 on 2024-05-27 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(db_column='CardID', primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(db_column='Question', max_length=255, verbose_name='Вопрос')),
                ('answer', models.TextField(db_column='Answer', max_length=5000, verbose_name='Ответ')),
                ('upload_date', models.DateTimeField(auto_now_add=True, db_column='UploadDate', verbose_name='Дата загрузки')),
                ('views', models.IntegerField(db_column='Views', default=0, verbose_name='Просмотры')),
                ('adds', models.IntegerField(db_column='Favorites', default=0, verbose_name='В избранном')),
                ('status', models.BooleanField(choices=[(False, 'Не проверено'), (True, 'Проверено')], default=False, verbose_name='Проверено')),
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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Name', max_length=120, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(db_column='TagID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'db_table': 'Tags',
            },
        ),
    ]
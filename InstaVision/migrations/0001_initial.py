# Generated by Django 2.0.1 on 2018-09-09 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentsFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments_file_name', models.CharField(max_length=25)),
                ('file', models.FileField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ImagesFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images_file_name', models.CharField(max_length=25)),
                ('file', models.FileField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='InstaVisionModel',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('page_url', models.CharField(max_length=300)),
                ('max_posts', models.IntegerField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('comments_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaVision.CommentsFile')),
                ('images_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaVision.ImagesFile')),
            ],
        ),
        migrations.CreateModel(
            name='UserTokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='instavisionmodel',
            name='key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaVision.UserTokens'),
        ),
        migrations.AddField(
            model_name='imagesfile',
            name='key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaVision.UserTokens'),
        ),
        migrations.AddField(
            model_name='commentsfile',
            name='key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaVision.UserTokens'),
        ),
    ]

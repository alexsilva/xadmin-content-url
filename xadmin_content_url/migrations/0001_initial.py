# Generated by Django 3.2.16 on 2023-06-23 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='XdUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='XdContentUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xadmin_content_url.xdurl')),
            ],
        ),
        migrations.AddIndex(
            model_name='xdurl',
            index=models.Index(fields=['content_type', 'object_id'], name='xadmin_cont_content_eacc92_idx'),
        ),
        migrations.AddIndex(
            model_name='xdcontenturl',
            index=models.Index(fields=['content_type', 'object_id'], name='xadmin_cont_content_315308_idx'),
        ),
    ]

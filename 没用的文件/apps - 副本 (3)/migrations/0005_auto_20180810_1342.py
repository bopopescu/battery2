# Generated by Django 2.1 on 2018-08-10 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_remove_boxdevicetable_cellid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boxdevicetable',
            name='boxNum',
        ),
        migrations.RemoveField(
            model_name='boxdevicetable',
            name='chnNum',
        ),
        migrations.AddField(
            model_name='celldevicetable',
            name='boxID',
            field=models.ForeignKey(default=1000, on_delete=django.db.models.deletion.DO_NOTHING, to='apps.boxDeviceTable', verbose_name='boxID'),
            preserve_default=False,
        ),
    ]

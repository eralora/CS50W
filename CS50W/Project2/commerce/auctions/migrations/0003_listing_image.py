# Generated by Django 3.0.8 on 2020-09-09 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]

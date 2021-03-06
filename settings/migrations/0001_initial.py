# Generated by Django 2.2.5 on 2019-10-16 06:30

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
            name='SocialLinksmodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('social_value', models.CharField(default='0_socialvalue', max_length=200, unique=True)),
                ('url', models.TextField(max_length=5000)),
                ('iconclass', models.CharField(max_length=200)),
                ('field_type', models.CharField(default='text', max_length=200)),
                ('manager', models.CharField(default='social', max_length=200)),
                ('createat', models.DateTimeField(auto_now_add=True)),
                ('updateat', models.DateTimeField(auto_now_add=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SMTPdetailModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SMTP_EMAIL', models.EmailField(default='wwwsmtp@24livehost.com', max_length=200)),
                ('SMTPPASSWORD', models.TextField(default='cQI-&Np>?aF?V7#XJlGwQbl4kH)~o*Gfrz_V|Hy<FK$9YMNUXdF;!DHS!ix?R!3%fLQqY1Q%+4|W;HlbFHuBDNHcI$a&1B}QB6jAD{)d<I7x3}bWBiBR6}buOGR`wQ%XZfP*hPjMoLakd23lqMr2ttQe$;<D^6=oZ%Q^nPH%HiFL^O`dPa6_XE$Y5X)iWtL|Qj<IY?(vT1RAOO*T_ya!6x6', max_length=2000)),
                ('SMTPPORT', models.IntegerField(default=465)),
                ('SMTPUSERNAME', models.CharField(default='mail.24livehost.com', max_length=100)),
                ('SMTPTLS', models.BooleanField(default=False)),
                ('setting_checkbox', models.BooleanField(default=False)),
                ('createdat', models.DateTimeField(auto_now_add=True)),
                ('updatedat', models.DateTimeField(auto_now_add=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LogoFavIconsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=200, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('field_type', models.CharField(max_length=200)),
                ('manager', models.CharField(max_length=200)),
                ('favlogo_value', models.CharField(default='1_favlogo_value', max_length=200, unique=True)),
                ('config_value_file', models.FileField(upload_to='LogoFav/')),
                ('createdat', models.DateTimeField(auto_now_add=True)),
                ('updatedat', models.DateTimeField(auto_now_add=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AddGeneralsettingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('Constant_Slug', models.CharField(max_length=200)),
                ('field_type', models.CharField(default='text', max_length=200)),
                ('config_value_bool', models.BooleanField(null=True)),
                ('config_value_text', models.TextField(null=True)),
                ('createdat', models.DateTimeField(auto_now_add=True)),
                ('updatedat', models.DateTimeField(auto_now_add=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

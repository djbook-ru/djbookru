# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import src.utils.db.fields.country_field
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('active_icon', models.ImageField(help_text=b'https://mapicons.nicolasmollet.com/ #95ce4a', upload_to=b'uploads/Achievement/', verbose_name='active icon')),
                ('inactive_icon', models.ImageField(help_text=b'https://mapicons.nicolasmollet.com/ #d5d5d5', upload_to=b'uploads/Achievement/', verbose_name='inactive icon')),
            ],
            options={
                'verbose_name': 'achievement',
                'verbose_name_plural': 'achievements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300, verbose_name='title')),
                ('link', models.URLField(verbose_name='link', blank=True)),
                ('content', models.TextField(help_text='Use Markdown and HTML', verbose_name='content')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
            options={
                'verbose_name': 'announcement',
                'verbose_name_plural': 'announcements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent', models.DateTimeField()),
                ('confirmation_key', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'e-mail confirmation',
                'verbose_name_plural': 'e-mail confirmations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('biography', models.TextField(verbose_name='biography', blank=True)),
                ('homepage', models.URLField(verbose_name='homepage', blank=True)),
                ('is_valid_email', models.BooleanField(default=False, verbose_name='is valid email?')),
                ('signature', models.TextField(max_length=1024, verbose_name='forum signature', blank=True)),
                ('location', models.CharField(max_length=64, null=True, blank=True)),
                ('country', src.utils.db.fields.country_field.CountryField(blank=True, max_length=2, null=True, choices=[(b'AD', 'Andorra'), (b'AE', 'United Arab Emirates'), (b'AF', 'Afghanistan'), (b'AG', 'Antigua & Barbuda'), (b'AI', 'Anguilla'), (b'AL', 'Albania'), (b'AM', 'Armenia'), (b'AN', 'Netherlands Antilles'), (b'AO', 'Angola'), (b'AQ', 'Antarctica'), (b'AR', 'Argentina'), (b'AS', 'American Samoa'), (b'AT', 'Austria'), (b'AU', 'Australia'), (b'AW', 'Aruba'), (b'AZ', 'Azerbaijan'), (b'BA', 'Bosnia and Herzegovina'), (b'BB', 'Barbados'), (b'BD', 'Bangladesh'), (b'BE', 'Belgium'), (b'BF', 'Burkina Faso'), (b'BG', 'Bulgaria'), (b'BH', 'Bahrain'), (b'BI', 'Burundi'), (b'BJ', 'Benin'), (b'BM', 'Bermuda'), (b'BN', 'Brunei Darussalam'), (b'BO', 'Bolivia'), (b'BR', 'Brazil'), (b'BS', 'Bahama'), (b'BT', 'Bhutan'), (b'BV', 'Bouvet Island'), (b'BW', 'Botswana'), (b'BY', 'Belarus'), (b'BZ', 'Belize'), (b'CA', 'Canada'), (b'CC', 'Cocos (Keeling) Islands'), (b'CF', 'Central African Republic'), (b'CG', 'Congo'), (b'CH', 'Switzerland'), (b'CI', 'Ivory Coast'), (b'CK', 'Cook Islands'), (b'CL', 'Chile'), (b'CM', 'Cameroon'), (b'CN', 'China'), (b'CO', 'Colombia'), (b'CR', 'Costa Rica'), (b'CU', 'Cuba'), (b'CV', 'Cape Verde'), (b'CX', 'Christmas Island'), (b'CY', 'Cyprus'), (b'CZ', 'Czech Republic'), (b'DE', 'Germany'), (b'DJ', 'Djibouti'), (b'DK', 'Denmark'), (b'DM', 'Dominica'), (b'DO', 'Dominican Republic'), (b'DZ', 'Algeria'), (b'EC', 'Ecuador'), (b'EE', 'Estonia'), (b'EG', 'Egypt'), (b'EH', 'Western Sahara'), (b'ER', 'Eritrea'), (b'ES', 'Spain'), (b'ET', 'Ethiopia'), (b'FI', 'Finland'), (b'FJ', 'Fiji'), (b'FK', 'Falkland Islands (Malvinas)'), (b'FM', 'Micronesia'), (b'FO', 'Faroe Islands'), (b'FR', 'France'), (b'FX', 'France, Metropolitan'), (b'GA', 'Gabon'), (b'GB', 'United Kingdom (Great Britain)'), (b'GD', 'Grenada'), (b'GE', 'Georgia'), (b'GF', 'French Guiana'), (b'GH', 'Ghana'), (b'GI', 'Gibraltar'), (b'GL', 'Greenland'), (b'GM', 'Gambia'), (b'GN', 'Guinea'), (b'GP', 'Guadeloupe'), (b'GQ', 'Equatorial Guinea'), (b'GR', 'Greece'), (b'GS', 'South Georgia and the South Sandwich Islands'), (b'GT', 'Guatemala'), (b'GU', 'Guam'), (b'GW', 'Guinea-Bissau'), (b'GY', 'Guyana'), (b'HK', 'Hong Kong'), (b'HM', 'Heard & McDonald Islands'), (b'HN', 'Honduras'), (b'HR', 'Croatia'), (b'HT', 'Haiti'), (b'HU', 'Hungary'), (b'ID', 'Indonesia'), (b'IE', 'Ireland'), (b'IL', 'Israel'), (b'IN', 'India'), (b'IO', 'British Indian Ocean Territory'), (b'IQ', 'Iraq'), (b'IR', 'Islamic Republic of Iran'), (b'IS', 'Iceland'), (b'IT', 'Italy'), (b'JM', 'Jamaica'), (b'JO', 'Jordan'), (b'JP', 'Japan'), (b'KE', 'Kenya'), (b'KG', 'Kyrgyzstan'), (b'KH', 'Cambodia'), (b'KI', 'Kiribati'), (b'KM', 'Comoros'), (b'KN', 'St. Kitts and Nevis'), (b'KP', "Korea, Democratic People's Republic of"), (b'KR', 'Korea, Republic of'), (b'KW', 'Kuwait'), (b'KY', 'Cayman Islands'), (b'KZ', 'Kazakhstan'), (b'LA', "Lao People's Democratic Republic"), (b'LB', 'Lebanon'), (b'LC', 'Saint Lucia'), (b'LI', 'Liechtenstein'), (b'LK', 'Sri Lanka'), (b'LR', 'Liberia'), (b'LS', 'Lesotho'), (b'LT', 'Lithuania'), (b'LU', 'Luxembourg'), (b'LV', 'Latvia'), (b'LY', 'Libyan Arab Jamahiriya'), (b'MA', 'Morocco'), (b'MC', 'Monaco'), (b'MD', 'Moldova, Republic of'), (b'MG', 'Madagascar'), (b'MH', 'Marshall Islands'), (b'ML', 'Mali'), (b'MN', 'Mongolia'), (b'MM', 'Myanmar'), (b'MO', 'Macau'), (b'MP', 'Northern Mariana Islands'), (b'MQ', 'Martinique'), (b'MR', 'Mauritania'), (b'MS', 'Monserrat'), (b'MT', 'Malta'), (b'MU', 'Mauritius'), (b'MV', 'Maldives'), (b'MW', 'Malawi'), (b'MX', 'Mexico'), (b'MY', 'Malaysia'), (b'MZ', 'Mozambique'), (b'NA', 'Namibia'), (b'NC', 'New Caledonia'), (b'NE', 'Niger'), (b'NF', 'Norfolk Island'), (b'NG', 'Nigeria'), (b'NI', 'Nicaragua'), (b'NL', 'Netherlands'), (b'NO', 'Norway'), (b'NP', 'Nepal'), (b'NR', 'Nauru'), (b'NU', 'Niue'), (b'NZ', 'New Zealand'), (b'OM', 'Oman'), (b'PA', 'Panama'), (b'PE', 'Peru'), (b'PF', 'French Polynesia'), (b'PG', 'Papua New Guinea'), (b'PH', 'Philippines'), (b'PK', 'Pakistan'), (b'PL', 'Poland'), (b'PM', 'St. Pierre & Miquelon'), (b'PN', 'Pitcairn'), (b'PR', 'Puerto Rico'), (b'PT', 'Portugal'), (b'PW', 'Palau'), (b'PY', 'Paraguay'), (b'QA', 'Qatar'), (b'RE', 'Reunion'), (b'RO', 'Romania'), (b'RU', 'Russian Federation'), (b'RW', 'Rwanda'), (b'SA', 'Saudi Arabia'), (b'SB', 'Solomon Islands'), (b'SC', 'Seychelles'), (b'SD', 'Sudan'), (b'SE', 'Sweden'), (b'SG', 'Singapore'), (b'SH', 'St. Helena'), (b'SI', 'Slovenia'), (b'SJ', 'Svalbard & Jan Mayen Islands'), (b'SK', 'Slovakia'), (b'SL', 'Sierra Leone'), (b'SM', 'San Marino'), (b'SN', 'Senegal'), (b'SO', 'Somalia'), (b'SR', 'Suriname'), (b'ST', 'Sao Tome & Principe'), (b'SV', 'El Salvador'), (b'SY', 'Syrian Arab Republic'), (b'SZ', 'Swaziland'), (b'TC', 'Turks & Caicos Islands'), (b'TD', 'Chad'), (b'TF', 'French Southern Territories'), (b'TG', 'Togo'), (b'TH', 'Thailand'), (b'TJ', 'Tajikistan'), (b'TK', 'Tokelau'), (b'TM', 'Turkmenistan'), (b'TN', 'Tunisia'), (b'TO', 'Tonga'), (b'TP', 'East Timor'), (b'TR', 'Turkey'), (b'TT', 'Trinidad & Tobago'), (b'TV', 'Tuvalu'), (b'TW', 'Taiwan, Province of China'), (b'TZ', 'Tanzania, United Republic of'), (b'UA', 'Ukraine'), (b'UG', 'Uganda'), (b'UM', 'United States Minor Outlying Islands'), (b'US', 'United States of America'), (b'UY', 'Uruguay'), (b'UZ', 'Uzbekistan'), (b'VA', 'Vatican City State (Holy See)'), (b'VC', 'St. Vincent & the Grenadines'), (b'VE', 'Venezuela'), (b'VG', 'British Virgin Islands'), (b'VI', 'United States Virgin Islands'), (b'VN', 'Viet Nam'), (b'VU', 'Vanuatu'), (b'WF', 'Wallis & Futuna Islands'), (b'WS', 'Samoa'), (b'YE', 'Yemen'), (b'YT', 'Mayotte'), (b'YU', 'Yugoslavia'), (b'ZA', 'South Africa'), (b'ZM', 'Zambia'), (b'ZR', 'Zaire'), (b'ZW', 'Zimbabwe'), (b'ZZ', 'Unknown or unspecified country')])),
                ('lng', models.FloatField(null=True, verbose_name='longitude', blank=True)),
                ('lat', models.FloatField(null=True, verbose_name='latitude', blank=True)),
                ('last_comments_read', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last comments read')),
                ('last_doc_comments_read', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last doc. comments read')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(verbose_name='note', blank=True)),
                ('achievement', models.ForeignKey(verbose_name='achievement', to='accounts.Achievement')),
                ('user', models.ForeignKey(verbose_name='user', to='accounts.User')),
            ],
            options={
                'verbose_name': 'user achievement',
                'verbose_name_plural': 'user achievements',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='userachievement',
            unique_together=set([('user', 'achievement')]),
        ),
        migrations.AddField(
            model_name='user',
            name='achievements',
            field=models.ManyToManyField(to='accounts.Achievement', verbose_name='achievements', through='accounts.UserAchievement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailconfirmation',
            name='user',
            field=models.ForeignKey(to='accounts.User'),
            preserve_default=True,
        ),
    ]

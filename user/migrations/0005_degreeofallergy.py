# Generated by Django 3.1.5 on 2022-10-31 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20221008_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='DegreeOfAllergy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buckwheat', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='메밀')),
                ('wheat', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='밀')),
                ('Big_head', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='대두')),
                ('peanut', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='땅콩')),
                ('Walnut', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='호두')),
                ('pine_nut', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='잣')),
                ('peach', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='복숭아')),
                ('tomato', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='토마토')),
                ('milk', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='우유')),
                ('shrimp', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='새우')),
                ('Mackerel', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='고등어')),
                ('squid', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='오징어')),
                ('crab', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='게')),
                ('clam', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='조개')),
                ('Pork', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='돼지고기')),
                ('beef', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='쇠고기')),
                ('chicken', models.BooleanField(choices=[(0, 'None'), (1, 'Low'), (2, 'High')], default=0, verbose_name='닭고기')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='사용자')),
            ],
            options={
                'verbose_name': '사용자 알러지 정도',
                'verbose_name_plural': '사용자 알러지 정도',
                'db_table': 'user_degree_of_allergy',
            },
        ),
    ]
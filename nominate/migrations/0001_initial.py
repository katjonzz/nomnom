# Generated by Django 5.0 on 2023-12-13 00:36

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wsfs", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Election",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(max_length=40, unique=True)),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="NominatingMember",
            fields=[
                (
                    "nomnomuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("wsfs.nomnomuser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("ballot_position", models.SmallIntegerField()),
                ("fields", models.SmallIntegerField(default=1)),
                ("field_1_description", models.CharField(max_length=100)),
                ("field_2_description", models.CharField(max_length=100)),
                ("field_3_description", models.CharField(max_length=100)),
                (
                    "election",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="nominate.election",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="ElectionState",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("valid_from", models.DateTimeField(default=None, null=True)),
                ("valid_to", models.DateTimeField(default=None, null=True)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("pre_nomination", "Not Yet Nominating"),
                            ("nominating", "Nominating"),
                            ("voting", "Voting"),
                            ("closed", "Closed"),
                        ],
                        default="pre_nomination",
                        max_length=20,
                    ),
                ),
                (
                    "election",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="state_history",
                        to="nominate.election",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Finalist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField()),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="nominate.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Nomination",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("field_1", models.CharField(max_length=200)),
                ("field_2", models.CharField(max_length=200)),
                ("field_3", models.CharField(max_length=200)),
                ("nomination_date", models.DateTimeField(auto_now=True)),
                ("nomination_ip_address", models.CharField(max_length=64)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="nominate.category",
                    ),
                ),
                (
                    "nominator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="nominate.nominatingmember",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NominationPermission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nomination_pin", models.CharField(max_length=64)),
                (
                    "election",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="nominate.election",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="nominate.nominatingmember",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="nominatingmember",
            name="elections",
            field=models.ManyToManyField(
                through="nominate.NominationPermission",
                to="nominate.election",
                verbose_name="Participating Votes",
            ),
        ),
        migrations.CreateModel(
            name="VotingMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("member_id", models.CharField(max_length=100)),
                (
                    "elections",
                    models.ManyToManyField(
                        to="nominate.election", verbose_name="Participating Votes"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.PositiveSmallIntegerField()),
                (
                    "finalist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="nominate.finalist",
                    ),
                ),
                (
                    "membership",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="nominate.votingmember",
                    ),
                ),
            ],
        ),
    ]
# Generated by Django 3.1.2 on 2020-10-27 06:04

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                ("is_artist", models.BooleanField(default=False)),
                ("is_user", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="Single", max_length=250, verbose_name="Album Title"
                    ),
                ),
                (
                    "year",
                    models.PositiveIntegerField(
                        default=2020,
                        validators=[
                            django.core.validators.MinValueValidator(1857),
                            django.core.validators.MaxValueValidator(2020),
                        ],
                        verbose_name="Year of Release",
                    ),
                ),
                (
                    "cover_file",
                    models.ImageField(upload_to="", verbose_name="Album Cover"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Audio",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Audio Title")),
                ("duration", models.DurationField(verbose_name="Duration")),
                (
                    "times_played",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="No. of times played",
                    ),
                ),
                (
                    "audio_file",
                    models.FileField(upload_to="", verbose_name="Audio File"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Playlist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=100, verbose_name="Title of the playlist"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="PitchApp.user",
                    ),
                ),
                (
                    "artist_name",
                    models.CharField(max_length=250, verbose_name="Artist Name"),
                ),
                ("country", django_countries.fields.CountryField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name="NormalUser",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="PitchApp.user",
                    ),
                ),
                (
                    "account_type",
                    models.CharField(max_length=50, verbose_name="Type of Account"),
                ),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("age", models.PositiveIntegerField(verbose_name="Age")),
                ("card", models.CharField(max_length=19, verbose_name="Card Number")),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tag", models.CharField(max_length=12, verbose_name="Tag")),
                (
                    "audio_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="PitchApp.audio"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Song",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "album_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="PitchApp.album"
                    ),
                ),
                (
                    "audio_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="PitchApp.audio"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Podcast",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "audio_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="PitchApp.audio"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Features",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "audio_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="PitchApp.audio"
                    ),
                ),
                (
                    "playlist_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="PitchApp.playlist",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="audio",
            name="playlist_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="PitchApp.playlist"
            ),
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("due_date", models.DateField(verbose_name="Due Date")),
                (
                    "user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="PitchApp.normaluser",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="playlist",
            name="user_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="PitchApp.normaluser"
            ),
        ),
        migrations.CreateModel(
            name="Creates",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "playlist_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="PitchApp.playlist",
                    ),
                ),
                (
                    "user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="PitchApp.normaluser",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="album",
            name="artist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="PitchApp.artist",
                verbose_name="Name of the Artist",
            ),
        ),
    ]
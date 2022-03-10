# -*- coding: utf-8 -*-

import uuid
import pytz

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Manager class for User Model.
    """
    def create_user(self, name, password=None):
        """
        Create and return a `User` with an username and password.
        """
        if not name:
            raise ValueError('Users Must Have a name')

        user = self.model(
            name=name,
        )
        user.set_password(password)
        print(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    """
    The class representing the schema of the User table.
    :param name (Characters): Name of the user.
    :param password (Characters): Password of the user.
    :param is_staff (Number): 1 if the user has admin access else 0.
    :param is_superuser (Number): 1 if the user has admin access else 0.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    last_login = None

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Usage(models.Model):
    """
    The class representing the schema of the Usage table.
    :param user_id (ForeignKey): ID of user.
    :param usage_type_id (ForeignKey): ID of usage_type.
    :param usage_at (DateTime): Time at which a usage was created. [Default - current time]
    :param amount (Number): Current usage.
    """
    user_id = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    usage_type_id = models.ForeignKey(
        'UsageTypes',
        on_delete=models.RESTRICT,
    )
    usage_at = models.DateTimeField(datetime.now(tz=pytz.utc))
    amount = models.FloatField()


class UsageTypes(models.Model):
    """
    The class representing the schema of the Usage table.
    :param name (Characters): Name of UsageType resource example - Electricity.
    :param unit (Characters): Unit of UsageType resource example - kwh.
    :param factor (Number): Rate for the resource.
    """
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    factor = models.FloatField()




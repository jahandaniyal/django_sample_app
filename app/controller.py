# -*- coding: utf-8 -*-

"""Controller Functions for all database operations.
This module provides helper functions for the following operations:
    1. Creation
    2. Deletion
    3. Updation
    4. Deletion
The operations apply to the following models:
    1. User
    2. Usage
    3. UsageTypes
Todo:
    * Adding Logging
"""
import pytz

from datetime import datetime

from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

from app.models import User, UsageTypes, Usage


def create_user(data):
    """Create a new user and save it in the database.
        Args:
            data (dict): {'name': <string>, 'password': <string>}.
                input data required for User creation
        Returns (None):
            None.
    """
    user = User(name=data.get('name'))
    user.save()


def delete_all_usage_by_user_id(user_id=None):
    """Delete all Usages for a particular user from the database.
        Args:
            user_id (string): [Required].
        Returns (int):
            Number of records deleted.
    """
    queryset = Usage.objects.filter(user_id=user_id)
    count = queryset.count()
    queryset.delete()
    return count


def delete_usage(usage_id):
    """Delete a Usage from the database.
        Args:
            usage_id (int): [Required].
        Returns (None):
            None.
    """
    Usage.objects.get(pk=usage_id).delete()


def delete_usage_type(usage_type_id):
    """Delete a UsageType from the database.
        Args:
            usage_type_id (int): [Required].
        Returns (None):
            None.
    """
    UsageTypes.objects.get(pk=usage_type_id).delete()


def delete_user(user_id):
    """Delete a User from the database.
        Args:
            user_id (string): [Required].
        Returns (None):
            None.
    """
    User.objects.get(pk=user_id).delete()


def get_all_usage_types():
    """Get all UsageTypes from the database.
        Args:
            None.
        Returns (dict):
            Returns a dict containing list of UsageTypes data.
    """
    usage_types = UsageTypes.objects.all()
    usage_types_data = [{"id": usage.id, "name": usage.name, "unit": usage.unit, "factor": usage.factor} for usage in usage_types]
    return {'Usage Types': usage_types_data}


def get_all_users():
    """Get all Users from the database.
        Args:
            None.
        Returns (dict):
            Returns a dict containing list of Users.
    """
    users = User.objects.all()
    users_data = [{"id": user.id.hex, "name": user.name} for user in users]
    return {'users' : users_data}


def get_usage(usage_id=None):
    """Get Usage from the database.
        Args:
            usage_id (int): [Required].
        Returns (dict):
            Returns a Usage model containing one record.
    """
    usage_data = Usage.objects.get(pk=usage_id)
    return usage_data


def get_usages(user_id=None, *args, **kwargs):
    """Get Usage from the database.
        Args:
            user_id (string): [Required].
            *args (iterable): [Optional].
            **kwargs (dict): [Optional].
        Returns (dict):
            Returns a Usage model queryset containing one or more records.
    """
    orderby = ''.join(['-', kwargs.get('orderby', 'id')]) \
        if kwargs.get('order') == 'desc' \
        else kwargs.get('orderby', 'id')
    start_date = kwargs.get('start_date', datetime(1970, 1, 1, 0, 0))
    end_date = kwargs.get('end_date', datetime.now(tz=pytz.utc))

    Usage.objects.filter(user_id=user_id).order_by(orderby)
    usage_data = Usage.objects.filter(Q(user_id=user_id) & Q(usage_at__gte=start_date) & Q(usage_at__lte=end_date)).order_by(orderby)
    return usage_data


def get_usage_type_by_id(usage_type_id):
    """Get UsageType from the database.
        Args:
            usage_type_id (int): [Required].
        Returns (dict):
            Returns a UsageType model containing one record.
    """
    usage_type_data = UsageTypes.objects.get(pk=usage_type_id)
    return usage_type_data


def get_user_name_by_id(user_id):
    """Get User name from the database using user_id.
        Args:
            user_id (string): [Required].
        Returns (dict):
            Returns user name of the User matching user_id.
    """
    user = User.objects.get(pk=user_id)
    return user.name


def get_usage_type_by_name(usage_type_name):
    """Get UsageType from the database using usage_type_name.
        Args:
            usage_type_name (string): [Required].
        Returns (dict):
            Returns a UsageType model containing one record.
    """
    usage_type_data = UsageTypes.objects.get(name=usage_type_name)
    return usage_type_data


def get_user_id_by_name(name):
    """Get User ID from the database using name of the User.
        Args:
            name (string): [Required].
        Returns (dict):
            Returns User ID of the User matching username.
    """
    user = User.objects.get(name=name)
    return user.id


def update_user(request, data, user_id):
    """Update User in the database using User ID.
        Args:
            request (Request): [Required].
            data (dict): [Required].
            user_id (string): [Required].
        Returns (dict):
            Returns User name of the updated User.
    """
    if request.user.id.hex != user_id:
        raise PermissionDenied

    user = User.objects.get(pk=user_id)
    user.name = data.get('name')
    user.save()
    return user.name

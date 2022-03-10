# -*- coding: utf-8 -*-

from django.contrib.auth.password_validation import validate_password
from django.forms.models import model_to_dict
from rest_framework import serializers

from app.models import User, UsageTypes, Usage


class UserSerializer(serializers.ModelSerializer):
    """Allows serialisation and deserialisation of `User` model objects.
    Attributes:
        name (CharField): [Required, Write_only].
        password (CharField): [Required, Write_only].
    """
    name = serializers.CharField(write_only=True, required=True)

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'name')

    def create(self, validated_data):
        """
        Create and return a `User` with an username and password.
        """
        user = User.objects.create(
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        Update and return updated `User`.
        """
        instance.name = validated_data.get('name', instance.name)

        instance.save()

        return instance


class UsageTypesSerializer(serializers.ModelSerializer):
    """Allows serialisation and deserialisation of `UsageType` model objects.
    Attributes:
        name (CharField): [Required, Write_only].
        unit (CharField): [Required, Write_only].
        factor (DecimalField): [Required, Write_only, max_digits=10, decimal_places=5].
    """
    name = serializers.CharField(write_only=True, required=True)
    unit = serializers.CharField(write_only=True, required=True)
    factor = serializers.DecimalField(max_digits=10, decimal_places=5, write_only=True, required=True)

    class Meta:
        model = UsageTypes
        fields = ('id', 'name', 'unit', 'factor')

    def to_representation(self, instance):
        """Return a serialised dict containing `UsageType` data"""
        ret = super().to_representation(instance)
        ret['name'] = instance.name
        ret['unit'] = instance.unit
        ret['factor'] = instance.factor
        return ret

    def create(self, validated_data):
        """
        Create and return a `UsageType` with a name, unit and factor.
        """
        usage_type = UsageTypes.objects.create(
            name=validated_data['name'],
            unit=validated_data['unit'],
            factor=validated_data['factor']
        )

        usage_type.save()

        return usage_type


class UsageSerializer(serializers.ModelSerializer):
    """Allows serialisation and deserialisation of `UsageType` model objects.
    Attributes:
        user_id (SlugRelatedField):
        usage_type_id (SlugRelatedField):
        usage_at (DateTimeField): [Required, Write_only].
        amount (DecimalField): [Required, Write_only].
    """
    user_id = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id')
    usage_type_id = serializers.SlugRelatedField(queryset=UsageTypes.objects.all(), slug_field='id')
    usage_at = serializers.DateTimeField(write_only=True, required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=5, write_only=True, required=True)

    class Meta:
        model = Usage
        fields = ('user_id', 'usage_type_id', 'usage_at', 'amount')

    def to_representation(self, instance):
        """Return a serialised dict containing `Usage` data"""
        ret = super().to_representation(instance)
        ret['user'] = model_to_dict(instance.user_id, fields='name')
        ret['user']['id'] = instance.user_id.id
        ret['usage'] = model_to_dict(instance.usage_type_id)
        ret['usage']['usage_at'] = instance.usage_at
        ret['usage']['amount'] = instance.amount
        del (ret['user_id'])
        del (ret['usage_type_id'])
        return ret

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.usage_type_id = validated_data.get('usage_type_id', instance.usage_type_id)
        instance.usage_at = validated_data.get('usage_at', instance.usage_at)
        instance.amount = validated_data.get('amount', instance.amount)

        instance.save()

        return instance

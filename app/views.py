# -*- coding: utf-8 -*-

import json

from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated
)
from rest_framework.response import Response

from app.authentication import AuthorAndAllAdmins, IsAdminOrReadOnly
from app.controller import (
    delete_all_usage_by_user_id,
    delete_usage,
    delete_usage_type,
    delete_user,
    get_all_usage_types,
    get_all_users,
    get_usage,
    get_usages,
    get_usage_type_by_id,
    get_user_name_by_id,
    update_user
)
from app.models import User
from app.serializers import UserSerializer, UsageTypesSerializer, UsageSerializer
from app.utils import sanitize_json_input


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UsersAPIView(RetrieveAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = UserSerializer

    def get(self, request):
        users = get_all_users()
        return Response(users)


class UserAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AuthorAndAllAdmins)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, user_id):
        user_name = get_user_name_by_id(user_id)
        content = {'user is': user_name}
        return Response(content)

    @sanitize_json_input
    def put(self, request, *args, **kwargs):

        data = json.loads(self.request.body)
        uuid = kwargs.get('user_id')
        user_name = update_user(request, data, uuid)
        content = {'user {} has been updated'.format(self.request.user.name): user_name}
        return Response(content)

    def delete(self, request, *args, **kwargs):
        user_name = get_user_name_by_id(kwargs.get('user_id'))
        delete_user(kwargs.get('user_id'))
        content = 'User {} has been deleted'.format(user_name)
        return Response(content)


class UsageTypesAPIView(ListCreateAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = UsageTypesSerializer

    def get(self, request):
        usage_types = get_all_usage_types()
        return Response(usage_types)

    @sanitize_json_input
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UsageTypeAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = UsageTypesSerializer

    def get_object(self):
        usage_type_obj = get_usage_type_by_id(self.kwargs.get('usage_type_id'))
        return usage_type_obj

    @sanitize_json_input
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        usage_type = get_usage_type_by_id(kwargs.get('usage_type_id'))
        delete_usage_type(kwargs.get('usage_type_id'))
        content = 'Usage Type {} has been deleted'.format(usage_type.name)
        return Response(content)


class UsagesAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, AuthorAndAllAdmins)
    serializer_class = UsageSerializer

    def get_queryset(self):
        usage_obj = get_usages(self.kwargs.get('user_id'), **self.request.query_params.dict())
        return usage_obj

    @sanitize_json_input
    def post(self, request, *args, **kwargs):
        if 'user_id' in kwargs:
            request.data['user_id'] = kwargs['user_id']
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        count = delete_all_usage_by_user_id(kwargs.get('user_id'))
        content = 'Total of {} Usage has been deleted'.format(count)
        return Response(content)


class UsageAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AuthorAndAllAdmins)
    serializer_class = UsageSerializer

    def get_object(self):
        usage_obj = get_usage(usage_id=self.kwargs.get('usage_id'))
        if self.kwargs.get('user_id') == usage_obj.user_id.id.hex or self.request.user.is_superuser:
            return usage_obj
        raise PermissionDenied

    @sanitize_json_input
    def put(self, request, *args, **kwargs):

        usage_obj = get_usage(usage_id=self.kwargs.get('usage_id'))
        if self.kwargs.get('user_id') == usage_obj.user_id.id.hex or self.request.user.is_superuser:
            request.data['user_id'] = self.kwargs.get('user_id')
            request.data['usage_id'] = self.kwargs.get('usage_id')
            request.data['usage_type_id'] = usage_obj.usage_type_id.id

            return self.update(request, *args, **kwargs)
        raise PermissionDenied

    def delete(self, request, *args, **kwargs):
        usage_obj = get_usage(usage_id=self.kwargs.get('usage_id'))
        if self.kwargs.get('user_id') == usage_obj.user_id.id.hex or self.request.user.is_superuser:
            delete_usage(kwargs.get('usage_id'))
            content = 'Id {} Usage has been deleted'.format(kwargs.get('usage_id'))
            return Response(content)
        raise PermissionDenied

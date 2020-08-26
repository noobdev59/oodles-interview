from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FileUploadParser

from userauth.models import Profile
from utils.models import Address, Friend
from api.serializers import (ProfileModelSerializer, AddressModelSerializer,
                             FriendModelSerializer, CreateProfileModelSerializer, ListUserModelSerializer)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ProfileModelViewSet(ModelViewSet):
    """
        Profile ModelViewSet, allow for default CRUD operations
    """
    queryset = Profile.objects.none()
    serializer_class = ProfileModelSerializer
    parser_classes = [FileUploadParser, ]


class RegisterUser(APIView):
    queryset = Profile.objects.none()
    serializer_class = CreateProfileModelSerializer

    def post(self, request):
        user = Profile.objects.create(name=request.data.get('name'),
                                   username=request.data.get('username'),
                                   email=request.data.get('email'),
                                  password=make_password(request.data.get('password')),
                                  phone_number=request.data.get('phone_number'),
                                  gender=request.data.get('gender'),
                                  date_of_birth=request.data.get('date_of_birth'))
        data = ProfileModelSerializer(user, many=False)
        return Response(data.data, status=status.HTTP_201_CREATED)


class UpdateUserProfile(generics.UpdateAPIView):
    """
        Profile UpdateModelSerializer, allow for default CRUD operations
    """
    serializer_class = ProfileModelSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated, ]


class ListUsers(generics.ListAPIView):
    serializer_class = ListUserModelSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        gender = self.request.data.get('gender', None)
        permanent_address_city = self.request.data.get('permanent_address_city', None)

        if gender is not None and permanent_address_city is not None:
            return Profile.objects.filter(gender=gender, permanent_address__city=permanent_address_city)
        elif gender is not None and permanent_address_city is None:
            return Profile.objects.filter(gender=gender)
        elif gender is None and permanent_address_city is not None:
            return Profile.objects.filter(permanent_address__city=permanent_address_city)

        return Profile.objects.all()


class AddressModelViewSet(ModelViewSet):
    """
        Address ModelViewSet, allow for default CRUD operations
    """
    queryset = Address.objects.all()
    serializer_class = AddressModelSerializer
    permission_classes = [IsAuthenticated, ]


class FriendModelViewSet(ModelViewSet):
    """
        Friend ModelViewSet, allow for default CRUD operations
    """
    queryset = Address.objects.all()
    serializer_class = AddressModelSerializer
    permission_classes = [IsAuthenticated, ]


class Logout(APIView):
    """
        Logout user based on session and token authentication
    """

    def post(self, request):
        """
            Delete user session and token
        """
        logout(request.user)
        request.user.auth_token.delete()
        return Response({'success': 'You have been successfully logged out!'}, status=status.HTTP_200_OK)


class GetUserDetail(generics.RetrieveAPIView):
    serializer_class = ProfileModelSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated, ]


class AddFriend(APIView):
    """
        Add friend to current logged in user
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        """
            @username: string
            Remove frined from user's friend list by supplying the username.
        """
        username_of_friend_to_add = request.data.get('username')

        # Check if username exists then proceed otherwise return 400_BAD_REQUEST
        if username_of_friend_to_add:
            # check if username exists in the database, if not then return 400_BAD_REQUEST
            try:
                friend_to_add = Profile.objects.get(username=username_of_friend_to_add)
                friend_object, _ = Friend.objects.get_or_create(user=friend_to_add)
                request.user.friends.add(friend_object)
                user_details = ProfileModelSerializer(request.user, many=False)
                return Response(user_details.data, status=status.HTTP_201_CREATED)
            except Profile.DoesNotExist:
                return Response({'error': 'User with this username does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Username field is required to add friend'}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFriend(APIView):
    """
        Remove friend to current logged in user
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        """
            @username: string
            Remove frined from user's friend list by supplying the username.
        """
        username_of_friend_to_add = request.data.get('username')

        # Check if username exists then proceed otherwise return 400_BAD_REQUEST
        if username_of_friend_to_add:
            # check if username exists in the database, if not then return 400_BAD_REQUEST
            try:
                friend_to_add = Profile.objects.get(username=username_of_friend_to_add)
                friend_object, _ = Friend.objects.get_or_create(user=friend_to_add)
                request.user.friends.remove(friend_object)
                user_details = ProfileModelSerializer(request.user, many=False)
                return Response(user_details.data, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({'error': 'User with this username does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Username field is required to add friend'}, status=status.HTTP_400_BAD_REQUEST)


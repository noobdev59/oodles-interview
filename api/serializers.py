from rest_framework.serializers import ModelSerializer, SerializerMethodField

from utils.models import Address, Friend
from userauth.models import Profile


class CreateProfileModelSerializer(ModelSerializer):
    class Meta:
        model = Profile
        depth = 1
        fields = ('name', 'email', 'password', 'phone_number', 'gender', 'date_of_birth', 'username')


class ProfileModelSerializer(ModelSerializer):

    class Meta:
        model = Profile
        depth = 1
        fields = ('id', 'name', 'username', 'email', 'profile_picture', 'phone_number', 'gender', 'date_of_birth', 'is_admin', 'is_active', 'company_address', 'permanent_address', 'friends',)


class ListUserModelSerializer(ModelSerializer):
    profile_picture = SerializerMethodField()
    is_friend_with_me = SerializerMethodField()
    count_of_mutual_friends = SerializerMethodField()
    permanent_address_city = SerializerMethodField()

    def get_permanent_address_city(self, instance):
        if instance.permanent_address:
            return instance.permanent_address.city
        else:
            return None

    def get_count_of_mutual_friends(self, instance):
        user = None
        request = self.context.get('request')

        if request and hasattr(request, 'user'):
            user = request.user

            return user.friends.filter(id__in=list(instance.friends.values_list('id', flat=True))).count()


    def get_is_friend_with_me(self, instance):
        user = None
        request = self.context.get('request')

        if request and hasattr(request, 'user'):
            user = request.user

            friend, created = Friend.objects.get_or_create(user=instance)

            if created:
                return False

            if Profile.objects.filter(id=user.id, friend=friend).exists():
                return True
            else:
                return False
        else:
            return False

    def get_profile_picture(self, instance):
        if instance.profile_picture:
            return instance.profile_picture.url
        else:
            return ''

    class Meta:
        model = Profile
        fields = ('id', 'name', 'gender', 'profile_picture', 'permanent_address_city', 'is_friend_with_me', 'count_of_mutual_friends')


class AddressModelSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class FriendModelSerializer(ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'


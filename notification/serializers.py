from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['email','username','password']

    def validate(self,data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username','password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')


        if username and password:
            print(f'Username:{username} and Password:{password}')
            user = authenticate(username=username,password=password)

            print('User:',user)

            if not user:
                raise serializers.ValidationError('Username not found.')
        else:
            raise serializers.ValidationError('Please enter your username and password.')
        
        attrs['user'] = user
        return attrs
    

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threads
        fields = ['title']
        read_only_fields = ['author','created_at']



class ThreadSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadSubscription
        fields = ['threads']
        read_only_fields = ['author','subscribed_at']



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['message','event','status','is_read']
        read_only_fields = ['user','created_at']



class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['preference']
        read_only_fields = ['user']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['thread','text','user']
        read_only_fields = ['user','created_at','thread']
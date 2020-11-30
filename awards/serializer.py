from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)

class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=True)
    projects = serializers.SerializerMethodField('get_projects')
    user = UserSerializer()
    
    class Meta:
        model = Profile
        fields = ('id', 'user', 'job_title', 'location', 'bio', 'avatar', 'projects','whatsapp', 
                  'linkedin', 'github')
        
    def get_projects(self, username):
        user = get_object_or_404(User, username=username)
        return Project.objects.filter(user=user).count()
        
class ScreenshotSerializer(serializers.ModelSerializer):
    image_1 = serializers.ImageField(max_length=None, use_url=True)
    image_2 = serializers.ImageField(max_length=None, use_url=True)
    image_3 = serializers.ImageField(max_length=None, use_url=True)
    
    class Meta:
        model = Screenshot
        fields = ('image_1', 'image_2', 'image_3')
        
class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')
    screenshots = ScreenshotSerializer()
    
    class Meta:
        model = Project
        fields = ('id', 'image', 'screenshots', 'project_name',
                   'description', 'date', 'like')
        
    def get_image_url(self, obj):
        return obj.image.url
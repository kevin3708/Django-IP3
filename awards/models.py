from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
import uuid

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.profile.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    job_title = models.CharField(max_length=150, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(max_length=120, null=True)
    avatar = CloudinaryField('image')
   
    
    
    def __str__(self):
        return self.user.username
    
    def save_image(self):
        self.save()
        
    def delete_image(self):
        self.delete()
        
    def get_projects(self, username):
        user = get_object_or_404(User, username=username)
        return Project.objects.filter(user=user).count()
    
    @classmethod
    def update(cls, id, value):
        cls.objects.filter(id=id).update(avatar=value)
        
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
class Screenshot(models.Model):
    image_1 = CloudinaryField('image')  
    image_2 = CloudinaryField('image')
    image_3 = CloudinaryField('image') 
    
    
    
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    image = CloudinaryField('image')
    screenshots = models.ForeignKey(Screenshot, on_delete=models.CASCADE, related_name='project_images')
    project_name = models.CharField(max_length=120, null=True)
    description = models.TextField(max_length=1000, verbose_name='project Description', null=True)
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_profile')
    like = models.IntegerField(default=0)
    
    
    
    
    
    def __str__(self):
        return self.project_name
    
    def save_image(self):
        self.save()
        
    @classmethod
    def search_projects(cls,search_term):
        posts = Project.objects.filter(project_name__icontains=search_term)
        return posts
        
    def delete_image(self):
        self.delete()  
        
    def no_of_rating(self):
        ratings = Rating.objects.filter(project=self)
        return len(ratings)
    
    def ave_des(self):
        rate = Rating.objects.filter(project=self)
        ret = rate.aggregate(Avg('design'))
        design = ret['design__avg']
        return design
    
    def ave_use(self):
        rate = Rating.objects.filter(project=self)
        ret = rate.aggregate(Avg('usability'))
        usability = ret['usability__avg']
        return usability
    
    def ave_cont(self):
        rate = Rating.objects.filter(project=self)
        ret = rate.aggregate(Avg('content')) 
        content = ret['content__avg']
        return content
    
    def all_ave(self):
        total = 0
        a = Rating.objects.filter(project=self)
        ave = [a.aggregate(Avg('design'))['design__avg'], a.aggregate(Avg('usability'))['usability__avg'], a.aggregate(Avg('content'))['content__avg']]
        
        for items in ave:
            total = total + items
                    
        return total / len(ave)
            
        
    
    
class Rating(models.Model):
    design = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    usability = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    content = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='post_ratings')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rater_profile')
    
    def __str__(self):
        return self.project.project_name
    
    def design_rate(self):
        design = (self.design * 10)
        return design
    
    def usability_rate(self):
        usability = (self.usability * 10)
        return usability
    
    def content_rate(self):
        content = (self.content * 10)
        return content
            
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateTimeField()
    
    def add_project(sender,instance,*args,**kwargs):
        project = instance
        user = project.user
        followers = Follow.objects.all().filter(following=user)
        
        for follower in followers:
            stream = Stream(project=project, user=follower.follower, date=project.date, following=user)
            stream.save()
            
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='post_like')

class Comment(models.Model):
    comment = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='post_comment')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='commenter_profile')
            
post_save.connect(Stream.add_project, sender=Project)
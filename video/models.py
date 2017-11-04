from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
# Create your models here.

class Video(models.Model):

    name=models.TextField(max_length=2000, help_text="Enter video name")

    user=models.ForeignKey(User, related_name="videos", on_delete=models.CASCADE, help_text="a")

    created_date = models.DateTimeField(default=timezone.now)

    embed = models.TextField(max_length=2000, null=True, blank=True, help_text='Enter the ID of Video')

    thumbnail = models.TextField(max_length=1000, null=True, blank=True)

    json = models.TextField(max_length=5000000, null=True, blank=True)

    processed=models.CharField(max_length=3, null=True, blank=True)

    adult=models.CharField(max_length=1,null=True, blank=True)

    def get_absolute_url(self):
        return reverse('video-detail', args=[str(self.id)])

    def __str__(self):
        return "#%i: %s" % (self.id, self.name)

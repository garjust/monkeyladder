from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    about = models.CharField(max_length=500, null=True, blank=True)

    def name(self):
        full_name = self.user.get_full_name()
        if full_name:
            return full_name
        return self.user.username
    
    @models.permalink
    def get_absolute_url(self):
        return ('view_profile', (), {'user_id': self.user.id})

    def __unicode__(self):
        return "{}'s Profile".format(self.name())

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)
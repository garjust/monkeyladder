from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class DatedModel(models.Model):
    created = models.DateTimeField()
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_creator'
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(DatedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created']


class UpdatedModel(DatedModel):
    last_updated = models.DateTimeField()
    last_updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_last_updated_by'
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.last_updated = timezone.now()
        return super(UpdatedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        get_latest_by = 'last_updated'
        ordering = ['-last_updated']

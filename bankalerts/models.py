from django.db import models

class ParentModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-modified']


class BotChat(ParentModel):
    chat_id = models.CharField(default="", max_length=500, blank=True, null=True)
    email = models.CharField(default="", max_length=500, blank=True, null=True)
    email_pw = models.CharField(default="", max_length=500, blank=True, null=True)
    uid = models.CharField(default="", max_length=500, blank=True, null=True)
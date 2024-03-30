from django.db import models

from common.models import BaseModel


class Post(BaseModel):
    title = models.CharField(max_length=256)
    content = models.TextField()

    def __str__(self):
        return self.title

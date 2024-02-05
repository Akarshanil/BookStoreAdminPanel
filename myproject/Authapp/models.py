import uuid
from django.db import models
from django.utils import timezone

# Create your models here.


class Author(models.Model):
    author_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects=models.Manager()


    def __str__(self):
        return self.author_name

class Book(models.Model):
    book_name = models.CharField(max_length=200)
    author_name= models.ForeignKey(Author, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    book_id = models.CharField(max_length=20, unique=True,default='')

    objects=models.Manager()

    def save(self, *args, **kwargs):
        if not self.book_id:
            self.book_id = 'ab' + str(uuid.uuid4().hex)[:8]
        super().save(*args, **kwargs)


    def __str__(self):
        return self.book_name



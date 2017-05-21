from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

class User(models.Model):
    '''
        Model for user_blog
    '''

    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, unique=True, primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    pw_hash = models.CharField(max_length=100)
    created_at = models.DateField(default=timezone.now)


    def __str__(self):
        return '%s %s %s %s' % (self.name, self.user_name, self.email, self.pw_hash)

class Category(models.Model):
    '''
        Model for Category
    '''
    category_id = models.AutoField(serialize=False, primary_key=True)
    name = models.CharField(max_length=100, unique = True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Category, self).save(*args, **kwargs)





class Item(models.Model):
    '''
        Model for item
    '''
    item_id = models.AutoField(serialize=False, primary_key=True)
    title = models.CharField(max_length=100, unique= True)
    description = models.CharField(max_length=300)
    created_at = models.DateField(default=timezone.now)
    category_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    user_name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        super(Item, self).save(*args, **kwargs)





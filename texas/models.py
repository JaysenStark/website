from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
    	string = '%s %s' % (self.username, self.password)
    	return string
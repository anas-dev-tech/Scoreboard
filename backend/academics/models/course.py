from django.db import models
from .major import Major
from django.db.models.functions import Lower

class Course(models.Model):
    '''Model definition for Course.'''
    name = models.CharField(max_length=50)
    
    class Meta: 
        constraints = [ 
            models.UniqueConstraint(Lower("name"), name="unique_lower_name_course")
        ]
        
    def __str__(self):
        return self.name
    

from django.db import models

class User(models.Model):
    is_engineer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set', 
        related_query_name='user',
    )
    
    def __str__(self):
        return self.username
    
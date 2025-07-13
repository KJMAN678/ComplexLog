
from django.db import models


class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('poem', 'Poem'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

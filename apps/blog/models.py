from django.db import models
from django.utils import timezone

def blog_thumnail_directory(instance, filename):
    """
    Function to create a folder for each image of each
    blog post (if the post has images/thumnails)
    """
    return "blog/{0}/{1}".format(instance.title, filename)

# Create your models here.
class Post:

    class PostObjects(models.Manager):
        """
        Class to get only the 'published' posts in the FE
        """
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    status_options = (
        ("draft", "Draft")
        ("published", "Published")
    )
    
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=blog_thumnail_directory)

    keywords = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)

    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(auto_now=True)

    status = models.CharField(max_length=10, choices=status_options,default='draft')

    objects = models.Manager() # Default manager
    post_objects = PostObjects() # Custom manager

    class Meta:
        ordering = ("-published")

    def __str__(self):
        return self.title
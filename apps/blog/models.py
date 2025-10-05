import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
def blog_thumnail_directory(instance, filename):
    """
    Function to create a folder for each image of each
    blog post (if the post has images/thumbnails)
    """
    return "blog/{0}/{1}".format(instance.title, filename)

def categorty_thumbnail_directory(instance, filename):
    """
    Function to create a folder for each image of each
    catgeory (if the category has images/thumbnails)
    """
    return "blog{0}/{1}".format(instance.name, filename)

class Category(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, blank=True, null=True)
    
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=255, blank=True, null=True)   
    description = models.TextField()
    thumbnail = models.ImageField(upload_to=categorty_thumbnail_directory)
    slug = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Post(models.Model):

    class PostObjects(models.Manager):
        """
        Class to get only the 'published' posts in the FE
        """
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    status_options = (
        ("draft", "Draft"),
        ("published", "Published")
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=255)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=blog_thumnail_directory)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    keywords = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)

    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(auto_now=True)

    status = models.CharField(max_length=10, choices=status_options,default='draft')

    objects = models.Manager() # Default manager
    post_objects = PostObjects() # Custom manager

    class Meta:
        ordering = ("status", "-created_at")

    def __str__(self):
        return self.title
    
class Heading(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='headings')

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    level = models.IntegerField(
        choices=(
            (1, "H1"),
            (2, "H2"),
            (3, "H3"),
            (4, "H4"),
            (5, "H5"),
            (6, "H5"),
        )
    )
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.title) # title = "hola mundo y python" => después de slugify() title = "hola-mundo-y-python"
        super().save(*args, **kwargs)
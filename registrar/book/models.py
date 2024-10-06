from django.db import models 
from django.utils.html import format_html
from django.contrib.auth.models import User


BOOK_LEVEL_CHOICE = (
    ('B','Basic'),
    ('M','Medium'),
    ('A','Advance')
)
class Catagory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Catagory/หมวดหมู่'

class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    class Meta:
        verbose_name_plural = 'Author/ผู้แต่ง'

class Book(models.Model):
    code = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    catagory = models.ForeignKey(Catagory, null=True, blank=True, on_delete=models.CASCADE)
    author = models.ManyToManyField(Author, blank= True)
    level = models.CharField(max_length=5, null=True, blank=True, choices= BOOK_LEVEL_CHOICE)
    image = models.FileField(upload_to='upload', null=True, blank=True)
    published = models.BooleanField(default=False)
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

   #def show_image(self):
   #   return format_html('img src="%s" height="40px">'% self.image.url)
   #show_image.allow_tags =True

    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Book/หนังสือ'

class BookComment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)  
    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Book Comment/ความคิดเห็น'

    def __str__(self) -> str:
        return self.comment 
    


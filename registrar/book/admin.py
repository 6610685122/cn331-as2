from django.contrib import admin
from .models import Catagory, Author,Book,BookComment

# Register your models here.

class BookCommentStackedInLine(admin.StackedInline):
    model = BookComment

class BookTabularInline(admin.TabularInline):
    model = BookComment
    extra = 2

class BookAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'catagory','price','published' ]
    list_filter = ['published']
    search_fields = ['code', 'name']
    prepopulated_fields = {'slug' : ['name']}
    fieldsets = (
        (None,{'fields': ['code','slug','name','description' ,'price','level','published']}),
        ('YOOOO',{'fields':['catagory','author'], 'classes': ['collapse']}),
    )
    inlines =[BookTabularInline]


admin.site.register(Catagory)
admin.site.register(Author)
admin.site.register(Book, BookAdmin)


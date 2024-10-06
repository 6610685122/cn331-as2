from django.contrib import admin
from .models import Course, QuotaRequest

#admin.site.register(Course)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'semester', 'academic_year', 'seats', 'is_quota_open')

@admin.register(QuotaRequest)
class QuotaRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_approved')
    list_filter = ('course', 'is_approved')
    search_fields = ('user__username', 'course__name') 
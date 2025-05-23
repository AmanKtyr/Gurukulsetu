from django.contrib import admin
from .models import College, UserProfile

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'address', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'email', 'phone')
    ordering = ('-created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college')
    list_filter = ('college',)
    search_fields = ('user__username', 'user__email', 'college__name')
    raw_id_fields = ('user', 'college')

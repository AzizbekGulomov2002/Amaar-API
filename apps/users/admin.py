from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('phone_number', 'name')
    ordering = ('date_joined',)


# @admin.register(Company)
# class CompanyAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         RichTextField: {'widget': CKEditorWidget},
#     }
#     list_display = ('name', 'address', 'phone_number', 'email')  # Display fields in the list view

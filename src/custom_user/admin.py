from django.contrib import admin
from .models import User, PasswordReset

class UserAdmin(admin.ModelAdmin):
    list_display = ['username',
                    'email',
                    'account']
    class Meta:
        model = User
admin.site.register(User, UserAdmin)

class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ['email']

    class Meta:
        model = PasswordReset
admin.site.register(PasswordReset, PasswordResetAdmin)

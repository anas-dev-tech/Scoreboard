from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()


@admin.register(User)
class Admin(admin.ModelAdmin):
    '''Admin View for '''
    list_display =('email', 'name', 'role', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'date_joined', 'force_change_password', )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password') and form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
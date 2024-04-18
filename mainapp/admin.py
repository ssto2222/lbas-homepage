from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from mainapp.models.user_models import User
from mainapp.models.profile_models import Profile
from django.contrib.auth.models import Group
from mainapp.forms import UserCreationForm

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,]
    fieldsets = (
        (None,{
            'fields': (
                'email',
                'password',
            )
        }),
        (None,{
            'fields':(
                'is_active',
                'is_admin',
            )
        })
    )
    
    list_display = ('email', 'is_active')
    list_filter = ()
    ordering = ()
    filter_horizontal = ()
    
    add_fieldsets = (
        (None,{
            'fields':('email','password',),
        }),
    )
    
    add_form = UserCreationForm
    
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from manager_app.models import *


class SubNowAdmin(admin.ModelAdmin):
    list_display = ('user', 'sub', 'end', 'active',)
    ordering = ('-created',)

admin.site.register(SubNow, SubNowAdmin)


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'for_target', 'discont_value', 'active',)
    search_fields = ('name', 'code',)
    ordering = ('-created',)

admin.site.register(PromoCode, PromoCodeAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'period', 'period_value',)
    search_fields = ('name',)
    ordering = ('-created',)

admin.site.register(Subscription, SubscriptionAdmin)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'target', 'value', 'created',)
    search_fields = ('user', 'name',)
    ordering = ('-created',)

admin.site.register(History, HistoryAdmin)



class CustomUserAdmin(UserAdmin):
    list_display = ("user_id", "first_name", "last_name", "is_premium", "language_code", "is_superuser")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": (("first_name", "last_name",), 
        ("email", "user_id",), ("is_premium", "language_code",))}),
        (
            _("Permissions"),
            {
                "fields": (
                    ("is_active", "is_staff", "is_superuser",),
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'user_id')}
        ),
    )
    search_fields = ('user_id',)
    ordering = ('user_id',)


admin.site.register(User, CustomUserAdmin)

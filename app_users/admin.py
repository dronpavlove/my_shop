from django.contrib import admin
from .models import Profile, UserMessage
from django.utils.translation import gettext_lazy as _


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'data_of_birth', 'phone', 'purchases_count', 'full_sum_count', 'status']
    search_fields = ['user.username']  # критерии для поиска
    list_filter = ['city', 'status']

    def __str__(self):
        return _('user profile')
    pass


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'status']
    search_fields = ['name', 'email']
    list_filter = ['status']
    actions = ['mark_as_item_answered', 'mark_as_item_unanswered']

    def mark_as_item_answered(self, request, queryset):  # что делать при выборе действия
        queryset.update(status='y')

    def mark_as_item_unanswered(self, request, queryset):
        queryset.update(status='n')

    mark_as_item_answered.short_description = 'transfer to status "answered"'
    mark_as_item_unanswered.short_description = 'transfer to status "unanswered"'

    def __str__(self):
        return _('user message')
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserMessage, UserMessageAdmin)

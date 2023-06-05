from django.contrib import admin
from .models import Blog, UserProfile, Comment, Block


class Blocker(admin.TabularInline):
    fk_name = 'blocker'
    model = Block
    extra = 0

    def has_add_permission(self, request, obj):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class Commenting(admin.TabularInline):
    model = Comment
    list_display = ('content', 'created',)
    extra = 0

    def has_add_permission(self, request, obj):
        return True

    def has_view_permission(self, request, obj=None):
        return True


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', ]
    search_fields = ['title', 'content']
    list_filter = ['created', ]
    inlines = [Commenting, ]

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj and obj.user.user == request.user:
            return True
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = UserProfile.objects.filter(user=request.user).first()
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        readonly = ['user', ]
        if obj and obj.user.user != request.user:
            readonly += ("title", "file", "content", "created", "updated")
        return readonly

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        app_user = UserProfile.objects.filter(user=request.user).first()
        blocked_users = app_user.blocker.all().values_list('blocked', flat=True)
        return qs.exclude(user__in=blocked_users)


class UserAdmin(admin.ModelAdmin):
    inlines = [Blocker, ]
    readonly_fields = ['user', ]

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj and obj.user == request.user:
            return True

        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj and obj.user == request.user:
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj and obj.user == request.user:
            return True

        return False


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Blog, BlogAdmin)

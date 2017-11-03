from django.contrib import admin

from .models import WbUser, WeiboData


class ReadOnlyModelAdmin(admin.ModelAdmin):
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


class WbUserAdmin(ReadOnlyModelAdmin):
    list_display = ('uid', 'name', 'gender', 'location', 'description', 'register_time', 'verify_type',
                    'follows_num', 'fans_num', 'wb_num')
    search_fields = ['name', 'uid']
    list_per_page = 20


class WeiboDataAdmin(ReadOnlyModelAdmin):
    list_display = ('weibo_id', 'uid', 'create_time', 'weibo_cont', 'repost_num', 'comment_num', 'praise_num')
    search_fields = ['weibo_cont', 'weibo_id']
    list_per_page = 20


admin.site.register(WbUser, WbUserAdmin)
admin.site.register(WeiboData, WeiboDataAdmin)
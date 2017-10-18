from django.contrib import admin

from .models import Keywords, LoginInFo, Seeds, WbUser, WeiboData


class KeywordsAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'enable')
    search_fields = ['keyword']
    list_per_page = 20


class LoginInFoAdmin(admin.ModelAdmin):
    list_display = ('name', 'password', 'enable')
    search_fields = ['name', 'enable']
    list_per_page = 20


class SeedsAdmin(admin.ModelAdmin):
    list_display = (
        'uid', 'is_crawled', 'other_crawled', 'home_crawled')
    search_fields = ['uid']
    list_per_page = 20
    ordering = ['is_crawled']


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
    list_display = ('uid', 'name', 'gender', 'birthday', 'location', 'register_time', 'verify_type', 'follows_num',
                    'fans_num', 'wb_num', 'level', 'tags', 'contact_info', 'education_info', 'head_img', 'work_info',
                    'verify_info', 'description')
    search_fields = ['name', 'uid']
    list_per_page = 20


class WeiboDataAdmin(ReadOnlyModelAdmin):
    list_display = ('weibo_id', 'repost_num', 'comment_num', 'praise_num', 'uid', 'is_origin', 'device', 'weibo_url',
                    'create_time', 'weibo_cont', 'comment_crawled', 'repost_crawled')
    search_fields = ['weibo_cont', 'weibo_id']
    list_per_page = 20


admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(Seeds, SeedsAdmin)
admin.site.register(LoginInFo, LoginInFoAdmin)
admin.site.register(WbUser, WbUserAdmin)
admin.site.register(WeiboData, WeiboDataAdmin)
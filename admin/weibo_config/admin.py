from django.contrib import admin

from admin.admin_config import Keywords, LoginInFo, Seeds


# Register your models here.


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


class WbUserAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'gender', 'birthday', 'location', 'register_time', 'verify_type', 'follows_num',
                    'fans_num', 'wb_num', 'level', 'tags', 'contact_info', 'education_info', 'head_img', 'work_info',
                    'verify_info', 'description')  # list
    search_fields = ['name', 'uid']
    list_per_page = 20


class WeiboDataAdmin(admin.ModelAdmin):
    list_display = ('weibo_id', 'repost_num', 'comment_num', 'praise_num', 'uid', 'is_origin', 'device', 'weibo_url',
                    'create_time', 'weibo_cont', 'comment_crawled', 'repost_crawled')  # list
    search_fields = ['weibo_cont', 'weibo_id']
    list_per_page = 20


admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(Seeds, SeedsAdmin)
admin.site.register(LoginInFo, LoginInFoAdmin)
#admin.site.register(WbUser, WbUserAdmin)
#admin.site.register(WeiboData, WeiboDataAdmin)

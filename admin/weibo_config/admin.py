from django.contrib import admin

from .models import Keywords, LoginInFo, Seeds


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


admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(Seeds, SeedsAdmin)
admin.site.register(LoginInFo, LoginInFoAdmin)

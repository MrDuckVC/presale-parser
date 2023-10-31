from django.contrib import admin

from .models import Word, LastCheckedTender


class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'id_user')
    search_fields = ('word', 'id_user')


class LastCheckedTenderAdmin(admin.ModelAdmin):
    list_display = ('last_checked_tender', 'tender')
    search_fields = ('last_checked_tender', 'tender')


admin.site.register(Word, WordAdmin)
admin.site.register(LastCheckedTender, LastCheckedTenderAdmin)

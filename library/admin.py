from django.contrib import admin

from library.models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'birth_date', 'death_date')
    exclude = ('author_id',)
    search_fields = ['surname_russian', 'name_russian', 'patronymic_russian']

    def author_name(self, obj):
        return '%s %s %s' % (obj.surname_russian, obj.name_russian, obj.patronymic_russian)

    author_name.short_description = 'Author'
    author_name.admin_order_field = 'surname_russian'

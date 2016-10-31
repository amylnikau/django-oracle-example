from django.conf.urls import url

from library.alias.views import AliasCreateView, AliasesView
from library.author.views import AuthorCreateView, AuthorsView
from library.authors_works.views import WorkAuthorsView, WorkAuthorsCreateView
from library.publication.views import PublicationCreateView, \
    PublicationsView
from library.translations.views import TranslationsView, TranslationCreateView
from library.work.views import WorksView, WorkCreateView
from library.writings.views import WritingsView, WritingCreateView
from . import views

app_name = 'library'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^query$', views.query_view, name='query'),
    url(r'^trigger-switch$', views.trigger_switch, name='trigger-switch'),

    url(r'^authors$', AuthorsView.as_view(), name='authors'),
    url(r'^author/create$', AuthorCreateView.as_view(), name='author_create'),

    url(r'^work-authors$', WorkAuthorsView.as_view(), name='work-authors'),
    url(r'^work-author/create$', WorkAuthorsCreateView.as_view(), name='work-authors_create'),

    url(r'^aliases$', AliasesView.as_view(), name='aliases'),
    url(r'^alias/create$', AliasCreateView.as_view(), name='alias_create'),

    url(r'^publications$', PublicationsView.as_view(), name='publications'),
    url(r'^publications/create$', PublicationCreateView.as_view(), name='publication_create'),

    url(r'^works$', WorksView.as_view(), name='works'),
    url(r'^works/create$', WorkCreateView.as_view(), name='work_create'),

    url(r'^writings$', WritingsView.as_view(), name='writings'),
    url(r'^writings/create$', WritingCreateView.as_view(), name='writing_create'),

    url(r'^translations$', TranslationsView.as_view(), name='translations'),
    url(r'^translations/create$', TranslationCreateView.as_view(), name='translation_create'),
]

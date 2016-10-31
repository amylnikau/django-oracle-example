from django.contrib import messages
from django.db import DatabaseError
from django.db import connections
from django.db import transaction
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render

from library.forms import LibraryFormSetHelper

SELECT_TRANSLATE_AUTHOR_INFO = 'SELECT a.SURNAME_RUSSIAN,a.NAME_RUSSIAN,a.PATRONYMIC_RUSSIAN, w.WORK_TITLE, w.PUBLICATION_YEAR, wt.WORK_TITLE,wt.PUBLICATION_YEAR,t.TRANSLATION_TITLE FROM AUTHORS a JOIN AUTHORS_WORKS USING(AUTHOR_ID) JOIN WORKS w USING(WORK_ID) JOIN TRANSLATIONS t USING(WORK_ID) JOIN WORKS wt ON wt.WORK_ID = t.TRANSLATED_WORK_ID WHERE a.SURNAME_RUSSIAN=%s'
SELECT_AUTHORS_WITH_TWO_AND_MORE_ALIASES = 'SELECT a.SURNAME_RUSSIAN,a.NAME_RUSSIAN,a.PATRONYMIC_RUSSIAN,a.NAME_ORIGINAL,a.SURNAME_ORIGINAL,a.BIRTH_DATE,a.DEATH_DATE  FROM AUTHORS a WHERE (SELECT COUNT(DISTINCT aw.ALIAS_ID) FROM AUTHORS_WORKS aw WHERE a.AUTHOR_ID=aw.AUTHOR_ID)>1'
SELECT_WORK_COUNT_WITH_INFO = 'SELECT WORK_COUNT, a.SURNAME_RUSSIAN,a.NAME_RUSSIAN,a.PATRONYMIC_RUSSIAN,a.NAME_ORIGINAL,a.SURNAME_ORIGINAL,a.BIRTH_DATE,a.DEATH_DATE  FROM AUTHORS a JOIN (SELECT aw.AUTHOR_ID, COUNT(*) AS WORK_COUNT FROM AUTHORS_WORKS aw GROUP BY aw.AUTHOR_ID) USING(AUTHOR_ID) ORDER BY WORK_COUNT DESC'
FIRST_TRIGGER = 'alter trigger "ANDREW"."AUTHORS_WORKS_AI" {0}; alter trigger "ANDREW"."AUTHORS_WORKS_AIER" {0}; alter trigger "ANDREW"."AUTHORS_WORKS_BI" {0}'
SECOND_TRIGGER = 'alter trigger "ANDREW"."WORKS_AIU" {0}; alter trigger "ANDREW"."WORKS_AIUER" {0}; alter trigger "ANDREW"."WORKS_BIU" {0}'
THIRD_TRIGGER = 'alter trigger "ANDREW"."TRANSLATION_PUBLICATION_YEAR" {}'
TRIGGER_STATUS = 'SELECT STATUS FROM USER_TRIGGERS WHERE TRIGGER_NAME = %s'


def index(request):
    status = [False, False, False]
    with connections['oracle'].cursor() as cursor:
        for i, trigger_name in enumerate(['AUTHORS_WORKS_AI', 'WORKS_AIU', 'TRANSLATION_PUBLICATION_YEAR']):
            cursor.execute(TRIGGER_STATUS, [trigger_name])
            if cursor.fetchone()[0] == 'ENABLED':
                status[i] = True
    return render(request, 'library/index.html', {'trigger_status': status})


def trigger_switch(request):
    if request.method == 'POST':
        trigger = request.POST.get('trigger')
        value = 'enable' if request.POST.get('value') == 'true' else 'disable'
        if trigger in ('trigger1', 'trigger2', 'trigger3'):
            with connections['oracle'].cursor() as cursor:
                if trigger == 'trigger1':
                    for command in FIRST_TRIGGER.format(value).split(';'):
                        cursor.execute(command)
                elif trigger == 'trigger2':
                    for command in SECOND_TRIGGER.format(value).split(';'):
                        cursor.execute(command)
                else:
                    cursor.execute(THIRD_TRIGGER.format(value))
                transaction.commit()
                return JsonResponse({'message': 'Trigger successful %sd' % value})
        else:
            raise Http404()
    else:
        raise Http404()


def query_view(request):
    if request.method == 'GET':
        query_type = int(request.GET.get('query_type', 0))
        if query_type in (1, 2, 3):
            with connections['oracle'].cursor() as cursor:
                if query_type == 1:
                    surname = request.GET.get('surname')
                    cursor.execute(SELECT_TRANSLATE_AUTHOR_INFO, [surname])
                    result = ([col[0] for col in cursor.description],
                              cursor.fetchall())
                elif query_type == 2:
                    cursor.execute(SELECT_AUTHORS_WITH_TWO_AND_MORE_ALIASES)
                    result = ([col[0] for col in cursor.description],
                              cursor.fetchall())
                else:
                    cursor.execute(SELECT_WORK_COUNT_WITH_INFO)
                    result = ([col[0] for col in cursor.description],
                              cursor.fetchall())
                return render(request, 'library/query_result.html', {'result': result})
        else:
            raise Http404()
    else:
        raise Http404()


class ContextDataMixin(object):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['helper'] = LibraryFormSetHelper()
        data['model_name'] = self.model._meta.verbose_name
        data['model_name_plural'] = str(self.model._meta.verbose_name_plural)
        return data


class DatabaseErrorMessageMixin(object):
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except DatabaseError as e:
            messages.error(self.request, e, 'danger')
            return self.form_invalid(form)


class DatabaseErrorFormSetMessageMixin(object):
    def formset_valid(self, formset):
        try:
            return super().formset_valid(formset)
        except DatabaseError as e:
            messages.error(self.request, e, 'danger')
            return self.formset_invalid(formset)

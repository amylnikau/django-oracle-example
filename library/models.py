from django.db import models


class Alias(models.Model):
    alias_id = models.BigIntegerField(primary_key=True)
    russian_title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aliases'
        verbose_name_plural = 'aliases'

    def __str__(self):
        return self.russian_title


class Author(models.Model):
    author_id = models.BigIntegerField(primary_key=True)
    surname_russian = models.CharField(max_length=100)
    name_russian = models.CharField(max_length=100)
    patronymic_russian = models.CharField(max_length=100, blank=True, null=True)
    name_original = models.CharField(max_length=100, blank=True, null=True)
    surname_original = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authors'

    def __str__(self):
        return " ".join((self.surname_russian, self.name_russian, self.patronymic_russian))


class WorkAuthors(models.Model):
    author = models.ForeignKey(Author, models.CASCADE, null=False)
    work = models.ForeignKey('Work', models.CASCADE, null=False)
    alias = models.ForeignKey(Alias, models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = False
        unique_together = ('author', 'work', 'alias')
        db_table = 'authors_works'
        verbose_name = 'work-authors'
        verbose_name_plural = 'work-authors'


class Publication(models.Model):
    work = models.OneToOneField('Work', models.CASCADE, primary_key=True)
    journal_title = models.CharField(max_length=100)
    journal_issue = models.IntegerField()
    journal_volume = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'publications'


class Translation(models.Model):
    work = models.OneToOneField('Work', models.CASCADE, primary_key=True)
    translated_work = models.ForeignKey('Work', models.SET_NULL, related_name='translated_work', null=True)
    translation_title = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'translations'


class WorkType(models.Model):
    type_id = models.BigIntegerField(primary_key=True)
    type_title = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_types'

    def __str__(self):
        return self.type_title


class Work(models.Model):
    work_id = models.BigIntegerField(primary_key=True)
    type = models.ForeignKey(WorkType, models.DO_NOTHING)
    work_title = models.CharField(max_length=300)
    publication_year = models.IntegerField()
    authors = models.ManyToManyField(Author, through=WorkAuthors)

    class Meta:
        managed = False
        db_table = 'works'

    def __str__(self):
        return self.work_title


class Writing(models.Model):
    work = models.OneToOneField(Work, models.CASCADE, primary_key=True)
    collection_title = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'writings'

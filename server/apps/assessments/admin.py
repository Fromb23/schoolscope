# apps/academic/admin.py
from django.contrib import admin
from .models import AcademicYear, Term, Curriculum, Subject, Cohort, CohortSubject

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ['name', 'academic_year', 'sequence', 'start_date', 'end_date']
    list_filter = ['academic_year']

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ['name', 'curriculum_type', 'is_active']
    list_filter = ['curriculum_type', 'is_active']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'curriculum']
    list_filter = ['curriculum']
    search_fields = ['code', 'name']

@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'curriculum', 'academic_year']
    list_filter = ['curriculum', 'academic_year']

@admin.register(CohortSubject)
class CohortSubjectAdmin(admin.ModelAdmin):
    list_display = ['cohort', 'subject', 'is_compulsory']
    list_filter = ['cohort', 'is_compulsory']
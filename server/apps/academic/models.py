# ============================================================================
# apps/academic/models.py
# Academic structure: Years, Terms, Curricula, Subjects, Cohorts
# ============================================================================

from django.db import models
from django.core.exceptions import ValidationError


class CurriculumType(models.TextChoices):
    """Supported curriculum frameworks"""
    EIGHT_FOUR_FOUR = "8-4-4", "8-4-4"
    CBC = "CBC", "CBC"
    IGCSE = "IGCSE", "IGCSE"
    CUSTOM = "CUSTOM", "Custom"


class AcademicYear(models.Model):
    """Academic year container - temporal boundary"""
    name = models.CharField(max_length=50, unique=True)  # "2024", "2024-2025"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")


class Term(models.Model):
    """Term/Semester within an academic year"""
    academic_year = models.ForeignKey(
        AcademicYear, 
        on_delete=models.CASCADE,
        related_name='terms'
    )
    name = models.CharField(max_length=50)  # "Term 1", "Semester 1"
    sequence = models.PositiveSmallIntegerField()  # 1, 2, 3
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['academic_year', 'sequence']
        unique_together = [['academic_year', 'sequence']]
        verbose_name = "Term"
        verbose_name_plural = "Terms"
    
    def __str__(self):
        return f"{self.academic_year.name} - {self.name}"
    
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")


class Curriculum(models.Model):
    """Curriculum framework definition"""
    name = models.CharField(max_length=100)
    curriculum_type = models.CharField(
        max_length=20,
        choices=CurriculumType.choices
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Curriculum"
        verbose_name_plural = "Curricula"
    
    def __str__(self):
        return f"{self.name} ({self.get_curriculum_type_display()})"


class Subject(models.Model):
    """Subject/Course within a curriculum"""
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
        related_name='subjects'
    )
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['curriculum', 'code']]
        ordering = ['curriculum', 'name']
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Cohort(models.Model):
    """Student cohort - year group with curriculum"""
    name = models.CharField(max_length=100)  # "Form 3 2024", "Grade 10 2024"
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.PROTECT,
        related_name='cohorts'
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='cohorts'
    )
    level = models.CharField(max_length=50, blank=True)  # "Form 3", "Grade 10"
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['academic_year', 'name']]
        ordering = ['academic_year', 'level']
        verbose_name = "Cohort"
        verbose_name_plural = "Cohorts"
    
    def __str__(self):
        return self.name


class CohortSubject(models.Model):
    """Bridge: Which subjects this cohort actually takes"""
    cohort = models.ForeignKey(
        Cohort,
        on_delete=models.CASCADE,
        related_name='cohort_subjects'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='cohort_subjects'
    )
    is_compulsory = models.BooleanField(default=True)
    
    class Meta:
        unique_together = [['cohort', 'subject']]
        verbose_name = "Cohort Subject"
        verbose_name_plural = "Cohort Subjects"
    
    def __str__(self):
        return f"{self.cohort.name} - {self.subject.name}"


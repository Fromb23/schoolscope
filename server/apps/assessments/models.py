# ============================================================================
# apps/assessments/models.py
# Assessment and grading system
# ============================================================================

from django.db import models


class AssessmentType(models.TextChoices):
    """Types of assessments"""
    CAT = "CAT", "CAT"
    TEST = "TEST", "Test"
    MAIN_EXAM = "MAIN_EXAM", "Main Exam"
    MOCK = "MOCK", "Mock"
    PROJECT = "PROJECT", "Project"
    ASSIGNMENT = "ASSIGNMENT", "Assignment"
    PRACTICAL = "PRACTICAL", "Practical"
    COMPETENCY = "COMPETENCY", "Competency"


class EvaluationType(models.TextChoices):
    """Methods of evaluation"""
    NUMERIC = "NUMERIC", "Numeric"
    RUBRIC = "RUBRIC", "Rubric"
    DESCRIPTIVE = "DESCRIPTIVE", "Descriptive"
    COMPETENCY = "COMPETENCY", "Competency"


class RubricScale(models.Model):
    """Rubric scale definition (e.g., CBC 1-4 scale)"""
    curriculum = models.ForeignKey(
        'academic.Curriculum',
        on_delete=models.CASCADE,
        related_name='rubric_scales'
    )
    
    name = models.CharField(max_length=100)  # "CBC 4-Point Scale"
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Rubric Scale"
        verbose_name_plural = "Rubric Scales"
    
    def __str__(self):
        return f"{self.name} ({self.curriculum.name})"


class RubricLevel(models.Model):
    """Individual level within a rubric scale"""
    rubric_scale = models.ForeignKey(
        RubricScale,
        on_delete=models.CASCADE,
        related_name='levels'
    )
    
    code = models.CharField(max_length=10)  # "4", "EE", "A"
    label = models.CharField(max_length=100)  # "Exceeds Expectations"
    description = models.TextField(blank=True)
    numeric_value = models.FloatField(help_text="For conversion/calculation")
    sequence = models.PositiveSmallIntegerField(help_text="Display order")
    
    class Meta:
        unique_together = [['rubric_scale', 'code']]
        ordering = ['rubric_scale', '-sequence']
        verbose_name = "Rubric Level"
        verbose_name_plural = "Rubric Levels"
    
    def __str__(self):
        return f"{self.code} - {self.label}"


class Assessment(models.Model):
    """Dynamic assessment definition"""
    term = models.ForeignKey(
        'academic.Term',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='assessments',
        help_text="Null for year-round CBC assessments"
    )
    subject = models.ForeignKey(
        'academic.Subject',
        on_delete=models.CASCADE,
        related_name='assessments'
    )
    
    name = models.CharField(max_length=100)  # "CAT 1", "End Term Exam"
    assessment_type = models.CharField(
        max_length=20,
        choices=AssessmentType.choices
    )
    evaluation_type = models.CharField(
        max_length=20,
        choices=EvaluationType.choices,
        default=EvaluationType.NUMERIC
    )
    
    # For numeric assessments
    total_marks = models.FloatField(null=True, blank=True)
    
    # For rubric assessments
    rubric_scale = models.ForeignKey(
        RubricScale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assessments'
    )
    
    assessment_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    weight = models.FloatField(default=1.0, help_text="For final grade calculations")
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-assessment_date']
        indexes = [
            models.Index(fields=['term', 'subject']),
            models.Index(fields=['assessment_date']),
        ]
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"
    
    def __str__(self):
        term_str = self.term.name if self.term else "Year-round"
        return f"{self.name} - {self.subject.name} ({term_str})"


class AssessmentScore(models.Model):
    """Individual student assessment result"""
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    student = models.ForeignKey(
        'learners.Student',
        on_delete=models.CASCADE,
        related_name='assessment_scores'
    )
    
    # Numeric score
    score = models.FloatField(null=True, blank=True)
    
    # Rubric evaluation
    rubric_level = models.ForeignKey(
        RubricLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assessment_scores'
    )
    
    # Feedback
    comments = models.TextField(blank=True)
    
    # Metadata
    submitted_at = models.DateTimeField(null=True, blank=True)
    graded_at = models.DateTimeField(auto_now_add=True)
    graded_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = [['assessment', 'student']]
        indexes = [
            models.Index(fields=['assessment', 'student']),
        ]
        verbose_name = "Assessment Score"
        verbose_name_plural = "Assessment Scores"
    
    def __str__(self):
        return f"{self.student.admission_number} - {self.assessment.name}"


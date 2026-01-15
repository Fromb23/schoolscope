
# ============================================================================
# apps/cbc/models.py
# CBC-specific: Strands, Sub-Strands, Learning Outcomes, Evidence
# ============================================================================

from django.db import models


class Strand(models.Model):
    """CBC Strand - major content area within a subject"""
    curriculum = models.ForeignKey(
        'academic.Curriculum',
        on_delete=models.CASCADE,
        related_name='strands'
    )
    subject = models.ForeignKey(
        'academic.Subject',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='strands'
    )
    
    code = models.CharField(max_length=50)  # "ALG", "GEO"
    name = models.CharField(max_length=200)  # "Algebra", "Geometry"
    description = models.TextField(blank=True)
    sequence = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['curriculum', 'subject', 'sequence']
        verbose_name = "Strand"
        verbose_name_plural = "Strands"
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class SubStrand(models.Model):
    """CBC Sub-Strand - specific topic within a strand"""
    strand = models.ForeignKey(
        Strand,
        on_delete=models.CASCADE,
        related_name='sub_strands'
    )
    
    code = models.CharField(max_length=50)  # "ALG.1", "GEO.2"
    name = models.CharField(max_length=200)  # "Linear Equations"
    description = models.TextField(blank=True)
    sequence = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['strand', 'sequence']
        verbose_name = "Sub-Strand"
        verbose_name_plural = "Sub-Strands"
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class LearningOutcome(models.Model):
    """Competency or learning outcome - most granular level"""
    sub_strand = models.ForeignKey(
        SubStrand,
        on_delete=models.CASCADE,
        related_name='learning_outcomes'
    )
    
    code = models.CharField(max_length=50, unique=True)  # "MAT.10.ALG.1.1"
    description = models.TextField()
    level = models.CharField(max_length=50, blank=True)  # "Grade 10"
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sub_strand', 'code']
        verbose_name = "Learning Outcome"
        verbose_name_plural = "Learning Outcomes"
    
    def __str__(self):
        return f"{self.code} - {self.description[:50]}"


class EvidenceRecord(models.Model):
    """Evidence of competency achievement"""
    student = models.ForeignKey(
        'learners.Student',
        on_delete=models.CASCADE,
        related_name='evidence_records'
    )
    learning_outcome = models.ForeignKey(
        LearningOutcome,
        on_delete=models.CASCADE,
        related_name='evidence_records'
    )
    
    # Source of evidence
    source_type = models.CharField(max_length=50)  # "PROJECT", "ASSESSMENT", "OBSERVATION"
    source_id = models.IntegerField(null=True, blank=True)
    
    # Evaluation
    evaluation_type = models.CharField(
        max_length=20,
        choices=[
            ('NUMERIC', 'Numeric'),
            ('RUBRIC', 'Rubric'),
            ('DESCRIPTIVE', 'Descriptive'),
            ('COMPETENCY', 'Competency'),
        ]
    )
    numeric_score = models.FloatField(null=True, blank=True)
    rubric_level = models.ForeignKey(
        'assessments.RubricLevel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evidence_records'
    )
    narrative = models.TextField(blank=True)
    
    # Metadata
    observed_at = models.DateField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-observed_at']
        indexes = [
            models.Index(fields=['student', 'learning_outcome']),
        ]
        verbose_name = "Evidence Record"
        verbose_name_plural = "Evidence Records"
    
    def __str__(self):
        return f"{self.student.admission_number} - {self.learning_outcome.code}"


# ============================================================================
# apps/reporting/models.py
# Pre-computed aggregates for performance
# ============================================================================

from django.db import models


class AttendanceSummary(models.Model):
    """Pre-computed attendance statistics"""
    student = models.ForeignKey(
        'learners.Student',
        on_delete=models.CASCADE,
        related_name='attendance_summaries'
    )
    term = models.ForeignKey(
        'academic.Term',
        on_delete=models.CASCADE,
        related_name='attendance_summaries'
    )
    subject = models.ForeignKey(
        'academic.Subject',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='attendance_summaries'
    )
    
    total_sessions = models.IntegerField(default=0)
    present_count = models.IntegerField(default=0)
    absent_count = models.IntegerField(default=0)
    late_count = models.IntegerField(default=0)
    excused_count = models.IntegerField(default=0)
    
    attendance_percentage = models.FloatField(null=True, blank=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [['student', 'term', 'subject']]
        verbose_name = "Attendance Summary"
        verbose_name_plural = "Attendance Summaries"
    
    def __str__(self):
        subject_str = self.subject.name if self.subject else "All subjects"
        return f"{self.student.admission_number} - {self.term.name} - {subject_str}"


class GradeSummary(models.Model):
    """Pre-computed grade statistics per term"""
    student = models.ForeignKey(
        'learners.Student',
        on_delete=models.CASCADE,
        related_name='grade_summaries'
    )
    term = models.ForeignKey(
        'academic.Term',
        on_delete=models.CASCADE,
        related_name='grade_summaries'
    )
    subject = models.ForeignKey(
        'academic.Subject',
        on_delete=models.CASCADE,
        related_name='grade_summaries'
    )
    
    total_assessments = models.IntegerField(default=0)
    average_score = models.FloatField(null=True, blank=True)
    weighted_average = models.FloatField(null=True, blank=True)
    final_grade = models.CharField(max_length=10, blank=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [['student', 'term', 'subject']]
        verbose_name = "Grade Summary"
        verbose_name_plural = "Grade Summaries"
    
    def __str__(self):
        return f"{self.student.admission_number} - {self.term.name} - {self.subject.name}"
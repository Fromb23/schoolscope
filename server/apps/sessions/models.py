# ============================================================================
# apps/sessions/models.py
# Session and Attendance tracking
# ============================================================================

from django.db import models


class SessionType(models.TextChoices):
    """Types of learning sessions"""
    LESSON = "LESSON", "Lesson"
    PRACTICAL = "PRACTICAL", "Practical"
    PROJECT = "PROJECT", "Project"
    EXAM = "EXAM", "Exam"
    FIELD_TRIP = "FIELD_TRIP", "Field Trip"
    ASSEMBLY = "ASSEMBLY", "Assembly"
    OTHER = "OTHER", "Other"


class AttendanceStatus(models.TextChoices):
    """Student attendance states"""
    PRESENT = "PRESENT", "Present"
    ABSENT = "ABSENT", "Absent"
    LATE = "LATE", "Late"
    EXCUSED = "EXCUSED", "Excused"
    SICK = "SICK", "Sick"


class Session(models.Model):
    """Time-based learning interaction container"""
    term = models.ForeignKey(
        'academic.Term',
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    subject = models.ForeignKey(
        'academic.Subject',
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    
    session_type = models.CharField(
        max_length=20,
        choices=SessionType.choices
    )
    session_date = models.DateField()
    start_time = models.CharField(max_length=10, blank=True)  # "08:00"
    end_time = models.CharField(max_length=10, blank=True)    # "09:30"
    
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    venue = models.CharField(max_length=100, blank=True)
    
    # Project linkage (if this session is part of a project)
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions'
    )
    
    # Audit trail
    created_by = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-session_date', 'start_time']
        indexes = [
            models.Index(fields=['session_date']),
            models.Index(fields=['term', 'subject']),
        ]
        verbose_name = "Session"
        verbose_name_plural = "Sessions"
    
    def __str__(self):
        return f"{self.session_date} - {self.subject.name} ({self.get_session_type_display()})"


class AttendanceRecord(models.Model):
    """Per-session student attendance"""
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    student = models.ForeignKey(
        'learners.Student',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    
    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices
    )
    notes = models.TextField(blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    marked_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = [['session', 'student']]
        indexes = [
            models.Index(fields=['session', 'student']),
            models.Index(fields=['student', 'status']),
        ]
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"
    
    def __str__(self):
        return f"{self.student.admission_number} - {self.session.session_date} ({self.get_status_display()})"


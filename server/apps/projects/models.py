# ============================================================================
# apps/projects/models.py
# Project-based learning tracking
# ============================================================================

from django.db import models


class Project(models.Model):
    """Extended learning project spanning multiple sessions"""
    subject = models.ForeignKey(
        'academic.Subject',
        on_delete=models.CASCADE,
        related_name='projects'
    )
    term = models.ForeignKey(
        'academic.Term',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='projects',
        help_text="Null for cross-term projects"
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    # Evaluation details
    total_marks = models.FloatField(null=True, blank=True)
    evaluation_type = models.CharField(
        max_length=20,
        choices=[
            ('NUMERIC', 'Numeric'),
            ('RUBRIC', 'Rubric'),
            ('DESCRIPTIVE', 'Descriptive'),
        ],
        default='NUMERIC'
    )
    rubric_scale = models.ForeignKey(
        'assessments.RubricScale',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return f"{self.name} - {self.subject.name}"


class ProjectParticipation(models.Model):
    """Student participation and final project evaluation"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='participations'
    )
    student = models.ForeignKey(
        'learners.Student',
        on_delete=models.CASCADE,
        related_name='project_participations'
    )
    
    # Final score/evaluation
    final_score = models.FloatField(null=True, blank=True)
    rubric_level = models.ForeignKey(
        'assessments.RubricLevel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='project_participations'
    )
    comments = models.TextField(blank=True)
    
    # Status tracking
    submitted_at = models.DateTimeField(null=True, blank=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    evaluated_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = [['project', 'student']]
        verbose_name = "Project Participation"
        verbose_name_plural = "Project Participations"
    
    def __str__(self):
        return f"{self.student.admission_number} - {self.project.name}"


class ProjectMilestone(models.Model):
    """Checkpoints within a project"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='milestones'
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sequence = models.PositiveSmallIntegerField()
    due_date = models.DateField(null=True, blank=True)
    max_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['project', 'sequence']
        verbose_name = "Project Milestone"
        verbose_name_plural = "Project Milestones"
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"


class MilestoneScore(models.Model):
    """Student score on individual project milestone"""
    milestone = models.ForeignKey(
        ProjectMilestone,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    participation = models.ForeignKey(
        ProjectParticipation,
        on_delete=models.CASCADE,
        related_name='milestone_scores'
    )
    
    score = models.FloatField(null=True, blank=True)
    comments = models.TextField(blank=True)
    evaluated_at = models.DateTimeField(auto_now_add=True)
    evaluated_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = [['milestone', 'participation']]
        verbose_name = "Milestone Score"
        verbose_name_plural = "Milestone Scores"
    
    def __str__(self):
        return f"{self.participation.student.admission_number} - {self.milestone.name}"


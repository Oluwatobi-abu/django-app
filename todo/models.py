from django.db import models


class Priority(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'


class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'todos'

    def __str__(self):
        return self.title

    @property
    def priority_badge(self):
        colors = {
            'low': '#6ee7b7',
            'medium': '#fcd34d',
            'high': '#f87171',
        }
        return colors.get(self.priority, '#6ee7b7')

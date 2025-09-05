from django.db import models
from django.conf import settings


class Page(models.Model):
    """A note or page (like in Notion/Obsidian)."""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pages"
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)  # markdown or plain text
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="subpages"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Todo(models.Model):
    """Simple checklist item (can belong to a page)."""
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE,
        related_name="todos",
        blank=True, null=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="todos"
    )
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{'x' if self.completed else ' '}] {self.title}"


class Task(models.Model):
    """Advanced task tracker item (with status, priority, due date)."""
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    page = models.ForeignKey(
        Page, on_delete=models.CASCADE,
        related_name="tasks",
        blank=True, null=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="MEDIUM")
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

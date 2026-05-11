from django.db import models


class SearchLog(models.Model):
    game_name = models.CharField(max_length=100)
    tag_line = models.CharField(max_length=30)
    success = models.BooleanField(default=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.game_name}#{self.tag_line}"

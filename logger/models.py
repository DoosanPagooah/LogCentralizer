from django.db import models

class ServiceLog(models.Model):
    LEVEL_CHOICES = [
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]

    STRATEGY_CHOICES = [
        ('ROUND_ROBIN', 'Round Robin'),
        ('NASH_EQ', 'Nash Equilibrium'),
    ]
    strategy = models.CharField(max_length=20, choices=STRATEGY_CHOICES, default='ROUND_ROBIN')
    cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)  # FinOps tracking

    service_name = models.CharField(max_length=100)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='INFO')
    message = models.TextField()
    # JSONField is great for storing variable error metadata/tracebacks
    payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_name} - {self.level} - {self.created_at}"
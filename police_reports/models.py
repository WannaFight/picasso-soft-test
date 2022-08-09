from django.core import validators
from django.db import models


class Crime(models.Model):
    """Model to store data about registered crimes"""
    crime_id = models.PositiveIntegerField(
        help_text="Unique crime id", unique=True,
        validators=[validators.MinValueValidator(1)]
    )
    crime_type = models.CharField(
        blank=False, max_length=50, help_text="Original crime type name"
    )

    report_date = models.DateField(
        help_text="When victim has reported a crime"
    )
    call_date = models.DateField()
    offense_date = models.DateField(help_text="When the crime has occurred")
    call_time = models.CharField(max_length=5, help_text="Time of the call")
    call_date_time = models.DateTimeField()

    disposition = models.CharField(blank=False, max_length=15)

    address = models.CharField(max_length=100)
    address_type = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    agency_id = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(1)]
    )
    common_location = models.CharField(blank=False, null=True, max_length=100)

    class Meta:
        ordering = ('crime_id',)

    def __str__(self) -> str:
        return f"ID: {self.crime_id}, type: {self.crime_type}"

from django.db import models
from spinny import settings
from django.contrib.auth.models import User


class Box(models.Model):
    class Meta:
        db_table = 'boxes'

    length = models.FloatField(null=False)
    width = models.FloatField(null=False)
    height = models.FloatField(null=False)
    area = models.FloatField(null=False)

    volume = models.FloatField(null=False)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='updated_by' , on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InventoryConditions(models.Model):
    class Meta:
        db_table = 'inventory_condition'

    average_area = models.FloatField(null=False)
    average_volume = models.FloatField(null=False)
    total_boxes = models.IntegerField(null=False)


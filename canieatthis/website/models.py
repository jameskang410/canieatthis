from django.db import models

class FoodTable(models.Model):
    """
    Contains verified food and if they can be eaten
    """
    food = models.CharField(max_length=50, blank=True, null=True)
    can_eat = models.CharField(max_length=10, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    row_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'food_table'


    def __str__(self):
        return "%s - %s" % (self.food, self.can_eat)

class UserTable(models.Model):
    """
    Contains user-submitted food and if they can be eaten
    """
    food = models.CharField(max_length=50, blank=True, null=True)
    can_eat = models.CharField(max_length=10, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    row_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'user_table'

    def __str__(self):
        return "%s - %s" % (self.food, self.can_eat)
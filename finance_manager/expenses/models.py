from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    OPERATION_TYPE_CHOICES = [
        ('Дохід', 'Дохід'),
        ('Витрата', 'Витрата'),
    ]


    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=10, choices=OPERATION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.category.name} - {self.amount} - {self.date}"

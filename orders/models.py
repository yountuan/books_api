from django.conf import settings
from django.db import models
from books.models import Book


class Order(models.Model):
    STATUS_CHOICES = ((1, 'Sent'), (2, 'Delivered'), (3, 'Order received'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through='OrderItem')
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=3)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.user} - {self.books}: {self.status}'

    def save(self, *args, **kwargs):
        self.total_price = self.book.price * self.quantity
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)




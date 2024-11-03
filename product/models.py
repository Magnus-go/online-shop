from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    category_title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('category_title',)

    def __str__(self):
        return self.category_title


class Subcategory(models.Model):
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    category_title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('category_title',)

    def __str__(self):
        return f'{self.category_title} - {self.parent_category}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, related_name='products', null=True, blank=True
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    price = models.PositiveSmallIntegerField()
    descriptions = models.TextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.category}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments')
    comment_text = models.TextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.product} - {self.comment_text[:30]}'


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replies')
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comments_replies', blank=True, null=True)
    reply_text = models.TextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.reply_text[:30]}'

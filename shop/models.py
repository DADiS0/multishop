from django.db import models
from django.utils import timezone
from django.urls import reverse
import os

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

def product_image_path(instance, filename):
      # تنظيف اسم المنتج لإزالة الأحرف الخاصة
    name = instance.name
    filename = os.path.splitext(name)[0]  # إزالة الامتداد
    filename = filename.replace(' ', '_')  # استبدال المسافات بشواهد سفلية


    # إضافة الامتداد مرة أخرى
    ext = os.path.splitext(filename)[1]
    if not ext:
      ext = '.jpg'  # افتراض الامتداد إذا لم يكن موجودًا
    filename += ext

    categories=instance.ptype.categories
    
    ptype = instance.ptype
    brand = instance.brand
    # You might need to handle cases where ptype or brand is None
    now = timezone.now()
    date_str = now.strftime("%Y/%m/%d")  # Format the date using strftime
    return f'product_images/{categories.name}/{ptype.name}/{brand.name}/{date_str}/{filename}'

def ptype_image_path(instance, filename):
    categories=instance.categories
    filename =instance.name
    filename = filename.replace(' ', '_')

    ext = os.path.splitext(filename)[1]
    if not ext:
      ext = '.jpg'  # افتراض الامتداد إذا لم يكن موجودًا
    filename += ext
    # You might need to handle cases where ptype or brand is None
    now = timezone.now()
    date_str = now.strftime("%Y/%m/%d")  # Format the date using strftime
    return f'type_images/{categories.name}/{date_str}/{filename}'

def brand_image_path(instance, filename):
    filename =instance.name
    filename = filename.replace(' ', '_')

    ext = os.path.splitext(filename)[1]
    if not ext:
      ext = '.jpg'  # افتراض الامتداد إذا لم يكن موجودًا
    filename += ext
    # You might need to handle cases where ptype or brand is None
    now = timezone.now()
    date_str = now.strftime("%Y/%m/%d")  # Format the date using strftime
    return f'brand_images{date_str}/{filename}'

class Categories(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='categories_images/%Y/%m/%d', blank=True)
    def __str__(self):
        return self.name
    
class Ptype(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to=ptype_image_path)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='subcategory')
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to=brand_image_path)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer = models.IntegerField(choices=[
        (0, '0%'),
        (10, '10%'),
        (20, '20%'),
        (25, '25%'),
        (30, '30%'),
        (35, '35%'),
        (45, '45%'),
        (50, '50%'),
        (60, '60%'),
        (75, '75%'),
    ],default=0,blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, blank=True)

    def save(self, *args, **kwargs):
        discount_amount = (self.price * self.offer) / 100
        self.new_price = self.price - discount_amount
        super().save(*args, **kwargs)

    publish = models.DateTimeField(default=timezone.now)
    ptype = models.ForeignKey(Ptype, on_delete=models.CASCADE, related_name='types')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brands')
    img = models.ImageField(upload_to=product_image_path,max_length=3000)
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[
            #self.ptype.name,  # إذا كان ptype هو ForeignKey
            #self.brand.name,  # إذا كان brand هو ForeignKey
            self.slug,
        ])


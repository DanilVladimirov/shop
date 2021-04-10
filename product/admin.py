from django.contrib import admin
from product.models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(Categories)
admin.site.register(Attributes)
admin.site.register(ProductAttrs)
admin.site.register(Brand)
admin.site.register(KeyWords)

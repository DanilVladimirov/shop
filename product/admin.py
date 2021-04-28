from django.contrib import admin
from product.models import *
from product.tasks import stop_promotion
from shop.celery import app
# Register your models here.


class PromotionsAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.save(commit=False)
        if len(PromotionsTasks.objects.filter(promotion=obj)) == 0:
            task = stop_promotion.apply_async(args=(obj.id,), eta=obj.date_end)
            promotion_task = PromotionsTasks.objects.create(promotion=obj, task_id=task.task_id)
            promotion_task.save()
        else:
            promotion_task = PromotionsTasks.objects.get(promotion=obj)
            app.control.revoke(promotion_task.task_id, terminate=True, signal='SIGTERM')
            task = stop_promotion.apply_async(args=(obj.id,), eta=obj.date_end)
            promotion_task.task_id = task.task_id
            promotion_task.save()
        if obj.categories.all().exists():
            for category in obj.categories.all():
                products = Product.objects.filter(cid=category)
                for product in products:
                    product.old_price = product.price
                    product.price = product.price - (product.price * obj.discount_percentage)
                    product.save()
        if obj.products.all().exists():
            for product in obj.products.all():
                product.old_price = product.price
                product.price = product.price - (product.price * obj.discount_percentage)
                product.save()


admin.site.register(Product)
admin.site.register(Categories)
admin.site.register(Attributes)
admin.site.register(ProductAttrs)
admin.site.register(Brand)
admin.site.register(KeyWords)
admin.site.register(Promotions, PromotionsAdmin)
admin.site.register(PromotionsTasks)




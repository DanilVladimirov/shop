from django.contrib import admin
from product.models import *
from product.tasks import stop_promotion, start_promotion
from shop.celery import app
# Register your models here.


class PromotionsAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.save(commit=False)
        if len(PromotionsTasks.objects.filter(promotion=obj)) == 0:
            task_stop = stop_promotion.apply_async(args=(obj.id,), eta=obj.date_end)
            task_start = start_promotion.apply_async(args=(obj.id,), eta=obj.date_start)
            promotion_task_stop = PromotionsTasks.objects.create(promotion=obj,
                                                                 task_end_id=task_stop.task_id,
                                                                 task_start_id=task_start.task_id)
            promotion_task_stop.save()
        else:
            promotion_task_stop = PromotionsTasks.objects.get(promotion=obj)
            app.control.revoke(promotion_task_stop.task_end_id, terminate=True, signal='SIGTERM')
            app.control.revoke(promotion_task_stop.task_start_id, terminate=True, signal='SIGTERM')
            task_stop = stop_promotion.apply_async(args=(obj.id,), eta=obj.date_end)
            task_start = start_promotion.apply_async(args=(obj.id,), eta=obj.date_start)
            promotion_task_stop.task_end_id = task_stop.task_id
            promotion_task_stop.task_start_id = task_start.task_id
            promotion_task_stop.save()


admin.site.register(Product)
admin.site.register(Categories)
admin.site.register(Attributes)
admin.site.register(ProductAttrs)
admin.site.register(Brand)
admin.site.register(KeyWords)
admin.site.register(Promotions, PromotionsAdmin)
admin.site.register(PromotionsTasks)
admin.site.register(PresentationImages)
admin.site.register(CommentsProduct)
admin.site.register(CommentsReplies)
admin.site.register(Delivery)
admin.site.register(Order)
admin.site.register(Wishlist)

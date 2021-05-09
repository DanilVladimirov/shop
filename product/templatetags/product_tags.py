from django import template
from product.models import Product

register = template.Library()


@register.filter(name='get_value')
def get_value(product, attr_id):
    if product.attrs.filter(fkey_attr=attr_id).exists():
        value = product.attrs.get(fkey_attr=attr_id).value
    else:
        value = 'none'
    return value


@register.filter(name='is_product_compare', takes_context=True)
def is_product_compare(request, pid):
    cid = Product.objects.get(id=pid).cid.get().name
    compare_list = request.session.get('compare', {})
    if compare_list.get(cid):
        if pid in compare_list[cid]:
            return True
        else:
            return False
    else:
        return False

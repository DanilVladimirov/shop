from django import template

register = template.Library()


@register.filter(name='get_value')
def get_value(product, attr_id):
    if product.attrs.filter(fkey_attr=attr_id).exists():
        value = product.attrs.get(fkey_attr=attr_id).value
    else:
        value = 'none'
    return value




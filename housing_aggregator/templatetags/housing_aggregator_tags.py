from django import template


register = template.Library()

@register.simple_tag()
def menu_items():
    return ['Home', 'Rent', 'FAQs', 'About']

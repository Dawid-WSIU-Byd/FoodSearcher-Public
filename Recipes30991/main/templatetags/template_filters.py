from django import template
register = template.Library()


# Returns the key of an array value.
# {{ value|getKey:arg }}
@register.filter(name='get_key')
def get_key(value, arg):
    return value[arg]
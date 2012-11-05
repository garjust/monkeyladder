from django import template

register = template.Library()


@register.filter(is_safe=True)
def parameters(dictionary):
    return '&'.join(['%s=%s' % (key, dictionary[key]) for key in dictionary])

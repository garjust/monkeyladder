from django import template

register = template.Library()


@register.filter(is_safe=True)
def parameters(dictionary):
    """
    Returns the dictionaries key/values in an & separated string

    {'a': 1, 'b': 2, 'c': 3} => a=1&b=2&c=3

    Not that ordering is NOT guarenteed
    """
    return '&'.join(['%s=%s' % (key, dictionary[key]) for key in dictionary])

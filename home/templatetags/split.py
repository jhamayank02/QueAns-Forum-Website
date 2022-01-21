from django import template

register = template.Library()

# To split a string
@register.filter(name='split')
def split(value, key):
  """
    Returns the value turned into a list.
  """
  return value.split(key)
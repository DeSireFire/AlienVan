from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def size_cutover(b):
    #todo 使用hurry.filesize
    kb = b//1024
    return kb
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def startswith(value, arg):
    """Verifica se 'value' começa com 'arg'."""
    return value.startswith(arg)

@register.filter
def add_attr(field, attr):
    attrs = field.field.widget.attrs
    # Divide os atributos por vírgula
    attrs_list = attr.split(',')
    for attr in attrs_list:
        # Divide o atributo por '=' para obter o nome e o valor
        if '=' in attr:
            key, value = attr.split('=', 1)  # Divide em no máximo 2 partes
            attrs[key] = value.strip()  # Remove espaços em branco
    return field
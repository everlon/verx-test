from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(name='plot')
def plot(graph, width=None, height=None):
    size = ''

    if width and isinstance(width, int):
        size += f"width={width} "
    if height and isinstance(height, int):
        size += f"height={height} "

    return mark_safe(f'<img src="data:image/png;base64,{graph.decode("utf-8")}" {size}" /><br>')
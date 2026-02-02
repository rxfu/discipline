import json

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="format_values")
def format_values(value):
    data = (
        [
            format_html(
                "<li style='display:inline-block; padding-right: 20px'><strong>{}：</strong>{}</li>",
                key,
                val,
            )
            for key, val in value.items()
        ]
        if value is not None
        else "无"
    )

    return mark_safe("<ul style='list-style:none'>" + "".join(data) + "</ul>")


@register.filter(name="get_item")
def get_item(dictionary, key):
    if isinstance(dictionary, str):
        dictionary = json.dumps(dictionary)
    #
    if isinstance(dictionary, dict):
        return dictionary.get(key, "")
    else:
        return None

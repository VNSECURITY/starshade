from django import template
from django.template.base import TextNode
from django.utils import numberformat
from django.utils.safestring import mark_safe

from dashboard import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def clear_session_message(context):
    context.request.session['message'] = None

@register.filter(is_safe=True)
def currency(value,decimal=0):
    return numberformat.format(
        value,
        settings.DECIMAL_SEPARATOR,
        decimal,
        settings.NUMBER_GROUPING,
        settings.THOUSAND_SEPARATOR,
        force_grouping=True
    )
@register.tag
def date_format(parser, token):
    return TextNode(settings.DATE_FORMAT_JS)

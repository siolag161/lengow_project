
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from ..fields import (LengowStatus, MarketplaceStatus)

register = template.Library()


@register.filter
def lengow_display_status(value):
    return LengowStatus.labels.get(value, '')

@register.filter
def marketplace_display_status(value):
    return MarketplaceStatus.labels.get(value, '')


@register.filter
def default_string_value(value, default_val='NA'):
    if not value or value.strip() == '':
        return default_val
    return value

@register.filter
def display_currency_value(value, currency='EUR'):
    value = value or 0.0
    val = round(float(value), 2)
    return "%s%s %s" % (intcomma(int(val)), ("%0.2f" % val)[-3:], currency)


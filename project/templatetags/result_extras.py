from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def table_results(unit_list, results, candidate):
    ret_val = ''
    for i, result in enumerate(results):
        ret_val += '<td colspan="' + str(unit_list[i].get_colspan()) + '">'
        ret_val += str(result[candidate])
        ret_val += '</td>'
    return mark_safe(ret_val)


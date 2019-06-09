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


@register.simple_tag
def cand_res(results, candidate):
    ret_val = '['
    for result in results:
        ret_val = ret_val + str(result[candidate]) + ','
    ret_val = ret_val + ']'
    return mark_safe(ret_val)


@register.simple_tag
def pie_title(unit_list, i):
    return mark_safe(unit_list[i].name)


@register.simple_tag
def pie_data(result, candidates):
    ret_val = ''
    for candidate in candidates:
        ret_val += '{'
        ret_val += 'name:\'' + candidate.name + '\', '
        ret_val += 'y:' + str(result[candidate])
        ret_val += '},'
    return mark_safe(ret_val)

from django.template import Library
from django.utils.safestring import mark_safe
register=Library()

@register.simple_tag
def build_display_val(query,class_admin):
    ele=''
    if class_admin.list_display:
        for display in class_admin.list_display:
            filed=class_admin.model._meta.get_field(display)
            if filed.choices:
                print(display)
                td='<td>'+getattr(query,'get_%s_display'%display)()+'</td>'
            else:
                td='<td>%s</td>'%getattr(query,display)
            ele+=td
    else:
        ele='<td>%s</td>'%query
    return mark_safe(ele)

@register.simple_tag
def build_sort_url(forloop,order):
    if not order:
        url=forloop
    else:
        if forloop==abs(int(order)):
            if '-' in order:
                order=abs(int(order))
            else:
                order='-'+order
            url = order
        else:
            url=forloop
    return url
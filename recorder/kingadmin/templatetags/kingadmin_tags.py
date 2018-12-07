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

@register.simple_tag
def build_filter_val(class_admin,filters,filter_dict):

    clomun_filter=class_admin.model._meta.get_field(filters)
    if clomun_filter.get_internal_type()=='ForeignKey':
        if filter_dict:
            choices=filter_dict[filters]
        else:choices=''
        start_ele = '<select name="%s">'%filters
        for clomun in clomun_filter.get_choices():
            # print(type(choices), (clomun[0]))
            if choices==str(clomun[0]):
                if clomun[0]:
                    op='<option value=%s selected="selected">%s</option>'%(clomun[0],clomun[1])
                else : op='<option value= >%s</option>'%(clomun[1])

            else:
                op = '<option value=%s>%s</option>' % (clomun[0], clomun[1])
            start_ele+=op
        start_ele += '</select>'

        return mark_safe(start_ele)
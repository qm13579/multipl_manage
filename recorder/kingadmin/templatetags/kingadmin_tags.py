from django.template import Library
from django.utils.safestring import mark_safe
register=Library()

@register.simple_tag
def build_display_val(query,class_admin,app_name,table_name):
    ele=''
    count=0
    if class_admin.list_display:
        for display in class_admin.list_display:
            filed=class_admin.model._meta.get_field(display)
            if filed.choices:
                if count == 0:
                    count+=1
                    td = '<td><a href="/kingadmin/%s/%s%s/change">' +getattr(query, 'get_%s_display' % display)() + '</a></td>'%(app_name,table_name,query.id)
                else:
                    td='<td>'+getattr(query,'get_%s_display'%display)()+'</td>'
            else:
                if count == 0:
                    count+=1
                    td = '<td><a href="/kingadmin/%s/%s/%s/change">%s</a></td>' % (app_name,table_name,query.id,getattr(query, display))
                else:
                    td='<td>%s</td>'%getattr(query,display)
            ele+=td
    else:
        ele='<td><a href="/kingadmin/%s/%s/%s/change">%s</a></td>'%(app_name,table_name,query.id,query)
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

@register.simple_tag
def build_page(queryset):
    currrnt_page=queryset.number
    ele=''

    start_pag = currrnt_page - 3
    end_pag=currrnt_page+3
    if start_pag-3 < 0:start_pag=1
    if end_pag >queryset.paginator.num_pages+1:end_pag=queryset.paginator.num_pages+1

    for i in range(start_pag,end_pag):
        if i==currrnt_page:
            pag = '<li class="active"><a href="?page=%s">%s<span class="sr-only"></span></a></li>'%(i,i)
        else:
            pag = '<li class=""><a href="?page=%s">%s<span class="sr-only"></span></a></li>'%(i,i)
        ele+=pag

    return  mark_safe(ele)

@register.simple_tag
def build_delete(model_obj):
    ele='<ul>'
    tables=model_obj._meta.related_objects
    for table in tables:
        table_name=table.name
        lookup_key='%s_set'%table_name
        related_obj=getattr(model_obj,lookup_key).all()
        ele += '<li>%s<ul>'%table_name
        if table.get_internal_type() == 'ForeignKey':
            for i in related_obj:
                ele += '<li><a href="/kingadmin/%s/%s/%s/change">%s</a></li>'%( i._meta.app_label,
                                                            i._meta.model_name,
                                                            i.id,i)
        ele += '</ul></li>'
    ele += '</ul>'
    return mark_safe(ele)


@register.simple_tag
def build_webinfo(query):

    title=query.title
    keyword=';'.join([query.keyword_1,query.keyword_2,query.keyword_3,query.keyword_4,query.keyword_5])
    # keyword=';'
    url=query.url
    date=query.date
    td='<td><a href="%s">%s</a></td><td>%s</td><td>%s</td>'%(url,title,keyword,date)

    return mark_safe(td)
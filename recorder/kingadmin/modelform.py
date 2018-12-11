from django import forms

def create_model_from(class_admin):
    class Meta:
        model=class_admin.model
        fields='__all__'
        # exclude=['user']
    def __new__(cls,*args,**kwargs):
        # print('base_fields:',cls.base_fields)
        for filed_name in cls.base_fields:
            filed_obj=cls.base_fields[filed_name]
            filed_obj.widget.attrs.update({'class':'form-control'})
        return forms.ModelForm.__new__(cls)

    dynamic=type('DynamicModelFrom',(forms.ModelForm,),{'Meta':Meta,'__new__':__new__})

    return  dynamic
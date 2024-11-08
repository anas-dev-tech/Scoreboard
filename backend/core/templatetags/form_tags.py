from django import template 




register = template.Library()



@register.filter(name="get_form_field")
def get_form_field(form, field_name):
    return form[field_name]
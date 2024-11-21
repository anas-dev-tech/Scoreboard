from django import forms
from .models import GradeDetail, Grade, GradeType

from django.forms import modelformset_factory





# # widgets.py
# from django.forms.widgets import Widget
# from django.utils.html import format_html
# from django.forms.utils import flatatt

# class DisabledForeignKeyWidget(Widget):
#     def __init__(self, attrs=None, queryset=None):
#         self.queryset = queryset
#         super().__init__()

#     def render(self, name, value, attrs=None, renderer=None):
#         if value is None:
#             value = ''
#         final_attrs = self.build_attrs(attrs, extra_attrs={'name': name})
#         related_object = self.queryset.get(pk=value) if value else None
#         display_value = related_object.name if related_object else ''
#         return format_html('<input readonly type="text"{} value="{}">', flatatt(final_attrs), display_value)

#     def value_from_datadict(self, data, files, name):
#         return data.get(name, None)


    
class GradeDetailForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Type')
    max_score = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Max Score')

    class Meta:
        model = GradeDetail
        fields = ['score', 'max_score']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].initial = self.instance.type.name




GradeDetailFormSet = modelformset_factory(
                                GradeDetail,
                                form=GradeDetailForm,
                                edit_only=True,
                                extra=0,
                                can_delete=False,
                                can_order=False,
                                )


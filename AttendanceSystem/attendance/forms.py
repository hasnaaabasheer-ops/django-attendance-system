from django import forms
from .models import Attendance
from students.models import Student


class AttendanceFilterForm(forms.Form):

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
            }
        )
    )

    department = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        departments = Student.objects.values_list(
            'department',
            flat=True
        ).distinct().order_by('department')

        self.fields['department'].choices = [
            ('', 'All Departments')
        ] + [
            (dept, dept) for dept in departments
        ]


class AttendanceRecordForm(forms.ModelForm):

    class Meta:
        model = Attendance

        fields = [
            'status',
        ]

        widgets = {
            'status': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
        }
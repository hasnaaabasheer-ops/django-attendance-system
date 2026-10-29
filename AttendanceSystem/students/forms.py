from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    DEPARTMENT_CHOICES = [
        ('Management', 'Management'),
        ('Commerce', 'Commerce'),
        ('Computer Science', 'Computer Science'),
        ('Science', 'Science'),
        ('Arts', 'Arts'),
    ]

    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    class Meta:
        model = Student

        fields = [
            'name',
            'roll_number',
            'email',
            'phone',
            'department',
            'joining_date',
            'photo',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student name',
            }),

            'roll_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter roll number',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),

            'joining_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
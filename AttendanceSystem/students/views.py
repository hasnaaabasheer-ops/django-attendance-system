from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Student
from .forms import StudentForm


def student_list(request):
    students = Student.objects.all().order_by('roll_number')

    search = request.GET.get('search', '')
    department = request.GET.get('department', '')
    joining_date = request.GET.get('joining_date', '')

    if search:
        students = students.filter(
            name__icontains=search
        ) | students.filter(
            roll_number__icontains=search
        ) | students.filter(
            email__icontains=search
        )

    if department:
        students = students.filter(department=department)

    if joining_date:
        students = students.filter(joining_date=joining_date)

    departments = Student.objects.values_list(
        'department',
        flat=True
    ).distinct().order_by('department')

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'students/student_list.html', {
        'page_obj': page_obj,
        'departments': departments,
        'search': search,
        'selected_department': department,
        'selected_joining_date': joining_date,
    })


def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add Student',
    })


def student_edit(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Edit Student',
        'student': student,
    })


def student_delete(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    return render(request, 'students/student_confirm_delete.html', {
        'student': student,
    })
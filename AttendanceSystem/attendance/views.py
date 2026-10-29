from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q, Count
from .models import Attendance
from students.models import Student
from .forms import AttendanceFilterForm


def staff_required(view_func):
    return login_required(
        user_passes_test(lambda user: user.is_staff)(view_func)
    )

@login_required
def dashboard(request):

    today = timezone.localdate()

    total_students = Student.objects.count()

    present_today = Attendance.objects.filter(
        date=today,
        status='P'
    ).count()

    absent_today = Attendance.objects.filter(
        date=today,
        status='A'
    ).count()

    if total_students:
        attendance_rate = round(
            (present_today / total_students) * 100,
            1
        )
    else:
        attendance_rate = 0

    department_stats = Student.objects.values(
        'department'
    ).annotate(
        total=Count('id'),
        present_today=Count(
            'attendances',
            filter=Q(
                attendances__date=today,
                attendances__status='P'
            )
        )
    ).order_by('department')

    recent_records = Attendance.objects.select_related(
        'student'
    ).order_by('-created_at')[:10]

    return render(request, 'dashboard.html', {
        'today': today,
        'total_students': total_students,
        'present_today': present_today,
        'absent_today': absent_today,
        'attendance_rate': attendance_rate,
        'department_stats': department_stats,
        'recent_records': recent_records,
    })

@staff_required
def mark_attendance(request):

    if request.method == 'POST':

        date = request.POST.get('date')
        department = request.POST.get('department')

        students = Student.objects.all().order_by('roll_number')

        if department:
            students = students.filter(
                department=department
            )

        for student in students:

            status = request.POST.get(
                f'status_{student.id}',
                'A'
            )

            Attendance.objects.update_or_create(
                student=student,
                date=date,
                defaults={
                    'status': status
                }
            )

        return redirect('attendance_records')


    # Students shown when page is opened

    department = request.GET.get('department', '')

    students = Student.objects.all().order_by('roll_number')

    if department:
        students = students.filter(
            department=department
        )


    departments = Student.objects.values_list(
        'department',
        flat=True
    ).distinct().order_by('department')

    today = timezone.localdate()

    return render(request, 'attendance/mark_attendance.html', {
        'students': students,
        'departments': departments,
        'today': today,
        'selected_department': department,
    })


@login_required
def attendance_records(request):

    records = Attendance.objects.select_related(
        'student'
    ).order_by('-date', 'student__roll_number')

    student_name = request.GET.get('student', '')
    date = request.GET.get('date', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    department = request.GET.get('department', '')
    status = request.GET.get('status', '')

    if student_name:
        records = records.filter(
            Q(student__name__icontains=student_name) |
            Q(student__roll_number__icontains=student_name)
        )

    if date:
        records = records.filter(date=date)

    if start_date and end_date:
        records = records.filter(
            date__range=[start_date, end_date]
        )

    if department:
        records = records.filter(
            student__department=department
        )

    if status:
        records = records.filter(status=status)

    departments = Student.objects.values_list(
        'department',
        flat=True
    ).distinct().order_by('department')

    return render(request, 'attendance/attendance_records.html', {
        'records': records,
        'departments': departments,
        'student_name': student_name,
        'selected_date': date,
        'start_date': start_date,
        'end_date': end_date,
        'selected_department': department,
        'selected_status': status,
    })


@login_required
def student_history(request, id):

    student = Student.objects.get(id=id)

    records = Attendance.objects.filter(
        student=student
    ).order_by('-date')

    total_records = records.count()

    present_count = records.filter(
        status='P'
    ).count()

    absent_count = records.filter(
        status='A'
    ).count()

    if total_records:
        attendance_percentage = round(
            (present_count / total_records) * 100,
            1
        )
    else:
        attendance_percentage = 0

    return render(
        request,
        'attendance/student_history.html',
        {
            'student': student,
            'records': records,
            'total_records': total_records,
            'present_count': present_count,
            'absent_count': absent_count,
            'attendance_percentage': attendance_percentage,
        }
    )
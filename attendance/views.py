import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Teacher, Admin, Subject, Classroom, Attendance


@csrf_exempt
def login(request):
    data = json.loads(request.body)

    email = data["email"]
    password = data["password"]
    user_type = data["user_type"]

    if user_type == "student":
        user = Student.objects.filter(email=email, password=password).first()
    elif user_type == "teacher":
        user = Teacher.objects.filter(email=email, password=password).first()
    else:
        user = Admin.objects.filter(email=email, password=password).first()

    if user:
        return JsonResponse({
            "success": True,
            "user_id": user.id,
            "name": user.name,
            "user_type": user_type
        })

    return JsonResponse({
        "success": False,
        "message": "Invalid email or password"
    })


@csrf_exempt
def student_register(request):
    data = json.loads(request.body)

    Student.objects.create(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )

    return JsonResponse({"success": True})


@csrf_exempt
def students(request):

    if request.method == "POST":
        data = json.loads(request.body)
        Student.objects.create(
            name=data["name"],
            email=data["email"],
            password=data["password"]
        )
        return JsonResponse({"success": True, "message": "Student added"})

    if request.method == "PUT":
        data = json.loads(request.body)
        student = Student.objects.get(id=data["id"])
        student.name = data["name"]
        student.email = data["email"]

        if data.get("password"):
            student.password = data["password"]

        student.save()
        return JsonResponse({"success": True, "message": "Student updated"})

    if request.method == "DELETE":
        data = json.loads(request.body)
        Student.objects.get(id=data["id"]).delete()
        return JsonResponse({"success": True, "message": "Student deleted"})

    return JsonResponse([
        {"id": s.id, "name": s.name, "email": s.email}
        for s in Student.objects.all()
    ], safe=False)


@csrf_exempt
def teachers(request):

    if request.method == "POST":
        data = json.loads(request.body)
        Teacher.objects.create(
            name=data["name"],
            email=data["email"],
            phone=data.get("phone", ""),
            password=data["password"]
        )
        return JsonResponse({"success": True, "message": "Teacher added"})

    if request.method == "PUT":
        data = json.loads(request.body)
        teacher = Teacher.objects.get(id=data["id"])

        teacher.name = data["name"]
        teacher.email = data["email"]
        teacher.phone = data.get("phone", teacher.phone)

        if data.get("password"):
            teacher.password = data["password"]

        teacher.save()
        return JsonResponse({"success": True, "message": "Teacher updated"})

    if request.method == "DELETE":
        data = json.loads(request.body)
        Teacher.objects.get(id=data["id"]).delete()
        return JsonResponse({"success": True, "message": "Teacher deleted"})

    return JsonResponse([
        {
            "id": t.id,
            "name": t.name,
            "email": t.email,
            "phone": t.phone
        }
        for t in Teacher.objects.all()
    ], safe=False)


@csrf_exempt
def subjects(request):

    if request.method == "POST":
        data = json.loads(request.body)
        Subject.objects.create(name=data["name"])
        return JsonResponse({"success": True, "message": "Subject added"})

    if request.method == "PUT":
        data = json.loads(request.body)
        subject = Subject.objects.get(id=data["id"])
        subject.name = data["name"]
        subject.save()
        return JsonResponse({"success": True, "message": "Subject updated"})

    if request.method == "DELETE":
        data = json.loads(request.body)
        Subject.objects.get(id=data["id"]).delete()
        return JsonResponse({"success": True, "message": "Subject deleted"})

    return JsonResponse([
        {"id": s.id, "name": s.name}
        for s in Subject.objects.all()
    ], safe=False)


@csrf_exempt
def classrooms(request):

    if request.method == "POST":
        data = json.loads(request.body)
        Classroom.objects.create(name=data["name"])
        return JsonResponse({"success": True, "message": "Classroom added"})

    if request.method == "PUT":
        data = json.loads(request.body)
        classroom = Classroom.objects.get(id=data["id"])
        classroom.name = data["name"]
        classroom.save()
        return JsonResponse({"success": True, "message": "Classroom updated"})

    if request.method == "DELETE":
        data = json.loads(request.body)
        Classroom.objects.get(id=data["id"]).delete()
        return JsonResponse({"success": True, "message": "Classroom deleted"})

    return JsonResponse([
        {"id": c.id, "name": c.name}
        for c in Classroom.objects.all()
    ], safe=False)


@csrf_exempt
def attendance(request):

    if request.method == "POST":
        data = json.loads(request.body)

        Attendance.objects.create(
            teacher_id=data["teacher_id"],
            student_id=data["student_id"],
            subject_id=data["subject_id"],
            date=data["date"],
            present=data["present"]
        )

        return JsonResponse({"success": True})

    teacher = request.GET.get("teacher_id")
    student = request.GET.get("student_id")

    records = Attendance.objects.all()

    if teacher:
        records = records.filter(teacher_id=teacher)

    if student:
        records = records.filter(student_id=student)

    return JsonResponse([
        {
            "id": a.id,
            "student_id": a.student_id,
            "subject_id": a.subject_id,
            "date": a.date,
            "present": a.present
        }
        for a in records
    ], safe=False)

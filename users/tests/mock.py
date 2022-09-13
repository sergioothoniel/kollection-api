institution = {
    "name": "Institution Test",
    "address": "Address 1",
    "link":"instituition.com",
    "city": "City Test",
    "state": "MG",
    "phone":"123456789",
    "cep":"12345-123",
    "is_active": True,
}

superuser = {
    "username": "admin",
    "email":"admin@email.com",
    "first_name": "Super",
    "last_name": "User",
    "password": "1234",
}

manager = {
    "username": "manager",
    "email":"manager@email.com",
    "first_name": "Manager",
    "last_name": "Teste",
    "password": "1234",
    "is_superuser": True,
    "is_reviewer": True,
    "is_student": False,
}

reviewer_user = {
    "username": "reviewerUser",
    "email":"reviewer@email.com",
    "first_name": "Reviewer",
    "last_name": "Test",
    "password": "1234",
    "is_superuser": False,
    "is_reviewer": True,
    "is_student": False,
}

student = {
    "username": "student",
    "email":"student@email.com",
    "first_name": "Student",
    "last_name": "Test",
    "password": "1234",
    "is_superuser": False,
    "is_reviewer": False,
    "is_student": True,
}
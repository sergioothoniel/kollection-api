from model_bakery.recipe import Recipe
from users.models import User


admin = Recipe(
        User,
        username= "Admin",
        email= "admin@email.com",
        first_name= "Admin",
        last_name= "Teste",
        password= "1234",
        is_superuser= True,
        is_reviewer= True,
        is_student= False,
)

create_user = Recipe(
    User,
    username= "normal",
    email= "student@email.com",
    first_name= "User",
    last_name= "Test",
    password= "1234",
    degree="cursando",
    about="um curso ai"
    
)

reviewer = Recipe(
        User,
        username= "reviewerUser",
        email= "reviewer@email.com",
        first_name= "Reviewer",
        last_name= "Test",
        password= "1234",
        is_superuser= False,
        is_reviewer= True,
        is_student= False,
)
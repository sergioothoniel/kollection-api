from model_bakery.recipe import Recipe

from institutions.models import Institution, InstitutionInfo

institution_info_test = Recipe(
    InstitutionInfo,
    city="Curitiba",
    state="Paraná",
    link="https://kenzie.com.br/",
    phone="4199999999",
    cep="81400000",
)

institution_test = Recipe(
    Institution,
    name="Kenzie",
)

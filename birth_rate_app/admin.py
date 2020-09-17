from django.contrib import admin
from birth_rate_app.models import (
    Hospital,
    Birth,
)

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Birth)

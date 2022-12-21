from django.contrib import admin
from .models import User,Allergy,DegreeOfAllergy

# Register your models here.

class UserAllergyInline(admin.TabularInline):
    model = Allergy
    extra = 1

class UserAllergyLevelInline(admin.TabularInline):
    model = DegreeOfAllergy
    extra = 1

class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)

    inlines = [UserAllergyInline,UserAllergyLevelInline]

admin.site.register(User,UserAdmin)
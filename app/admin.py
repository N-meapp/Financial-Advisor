from django.contrib import admin
from .models import *

class LiabilityInline(admin.TabularInline):
    model = Liability
    extra = 2

class GoalsInline(admin.TabularInline):
    model = Financial_goals
    extra = 2

class FinancialStatementAdmin(admin.ModelAdmin):
    inlines = [LiabilityInline,GoalsInline]


admin.site.register(Customer)
admin.site.register(Finacial_statements,FinancialStatementAdmin)
admin.site.register(FinancialAdvice)


from django.contrib import admin
from .models import (Department, AccountManager, Customer, ProjectType,
                     Project, JobTitle, Employee, Skill, CommercialStatus,
                     AllocationType, ReccurringType, Allocation, AllocationDetail, BankHoliday)


admin.site.register(Department)
admin.site.register(AccountManager)
admin.site.register(Customer)
admin.site.register(ProjectType)
admin.site.register(Project)
admin.site.register(JobTitle)
admin.site.register(Employee)
admin.site.register(Skill)
admin.site.register(CommercialStatus)
admin.site.register(AllocationType)
admin.site.register(ReccurringType)
admin.site.register(Allocation)
admin.site.register(AllocationDetail)
admin.site.register(BankHoliday)
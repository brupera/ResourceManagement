from django.db import models
from django.urls import reverse
from django.core import validators
from django.contrib.auth.models import User
import calendar


class ResourceManagementAbstract(models.Model):
    """ Event abstract model """
    version = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MyProtectError(models.deletion.ProtectedError):

    def __init__(self, msg, protected_objects, **kwargs):
        self.kwargs = kwargs
        super().__init__(msg, protected_objects)


def MY_PROTECT(collector, field, sub_objs, using):
    kwargs = {
        'field': field,
        'sub_objs': sub_objs,
        'using': using
    }
    raise MyProtectError(
        "Cannot delete some instances of model '%s' because they are "
        "referenced through a protected foreign key: '%s.%s'" % (
            field.remote_field.model.__name__, sub_objs[0].__class__.__name__, field.name
        ),
        sub_objs, **kwargs
    )


class Department(ResourceManagementAbstract):
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.CharField(max_length=300, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_department')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_department')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('department-list')


class AccountManager(ResourceManagementAbstract):
    first_name = models.CharField("First name", max_length=100)
    last_name = models.CharField("Last name", max_length=100)
    email = models.EmailField(max_length=50, validators=[validators.EmailValidator(message="Invalid Email")])
    phone = models.CharField(max_length=20, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_account_manager')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_account_manager')

    def get_absolute_url(self):
        return reverse('accountmanager-list')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Customer(ResourceManagementAbstract):
    name = models.CharField(max_length=100)
    account_manager = models.ForeignKey(AccountManager, on_delete=MY_PROTECT)
    description = models.CharField(max_length=200, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_customer')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_customer')

    def get_absolute_url(self):
        return reverse('customer-list')

    def __str__(self):
        return self.name


class ProjectType(ResourceManagementAbstract):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_project_type')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_project_type')

    def get_absolute_url(self):
        return reverse('projecttype-list')

    def __str__(self):
        return self.name


class JobTitle(ResourceManagementAbstract):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_job_title')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_job_title')

    def get_absolute_url(self):
        return reverse('jobtitle-list')

    def __str__(self):
        return self.name


class Skill(ResourceManagementAbstract):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_skill')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_skill')

    def __str__(self):
        return self.name


class Employee(ResourceManagementAbstract):
    # https://www.letscodemore.com/blog/django-inline-formset-factory-with-examples/
    GENDER = (('male', 'MALE'), ('female', 'FEMALE'), ('other', 'OTHER'))
    LOCATION = (('india', 'India'), ('uk', 'UK'), ('other', 'OTHER'))
    emp_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_joining = models.DateField(null=False, blank=False)
    resignation_date = models.DateField(null=True, blank=True)
    last_date_of_working = models.DateField(null=True, blank=True)
    job_title = models.ForeignKey(JobTitle, null=True, blank=True, on_delete=MY_PROTECT)
    line_manager = models.ForeignKey('self', null=True, blank=True, on_delete=MY_PROTECT)
    email = models.EmailField(max_length=125, null=False)
    gender = models.CharField(choices=GENDER, max_length=10)
    location = models.CharField(choices=LOCATION, max_length=10)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    skills = models.ManyToManyField(Skill, null=True, blank=True)
    standard_hours = models.IntegerField(default=8)
    standard_charge_out_rate = models.DecimalField(blank=True, null=True, max_digits=20,  decimal_places=10)
    include_in_capacity = models.BooleanField(default=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_employee')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_employee')

    def get_absolute_url(self):

        return reverse('employee-list')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class CommercialStatus(ResourceManagementAbstract):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_commercial_status')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_commercial_status')

    def get_absolute_url(self):
        return reverse('commercialstatus-list')

    def __str__(self):
        return self.name


class Project(ResourceManagementAbstract):
    PHASE = (('initiation', 'Initiation'), ('planning', 'Planning'), ('execution', 'Execution'),
             ('monitoring & control', 'Monitoring & Control'), ('closure', 'Closure'))
    STATUS = (('in-flight', 'In-Flight'), ('on hold', 'On Hold'), ('completed', 'Completed'))
    PRIORITY = (('ciritical', 'Critical'), ('high', 'High'), ('medium', 'Medium'), ('low', 'Low'))
    HEALTH = (('red', 'Red'), ('amber', 'Amber'), ('green', 'Green'))

    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    customer = models.ForeignKey(Customer, null=True, on_delete=MY_PROTECT, related_name="account")
    project_type = models.ForeignKey(ProjectType, on_delete=MY_PROTECT)
    customer_delivery_lead = models.ForeignKey(Employee, on_delete=MY_PROTECT, null=True, related_name="cdl")
    service_delivery_manager = models.ForeignKey(Employee, on_delete=MY_PROTECT, null=True, related_name="sdm")
    commercial_status = models.ForeignKey(CommercialStatus, on_delete=MY_PROTECT, null=True, related_name="commercial")
    project_phase = models.CharField(choices=PHASE, max_length=20)
    project_status = models.CharField(choices=STATUS, max_length=10)
    priority = models.CharField(choices=PRIORITY, max_length=10)
    project_health = models.CharField(choices=HEALTH, max_length=10)
    objective_and_deliverables = models.CharField(max_length=200, null=True, blank=True)
    dependencies = models.CharField(max_length=200, null=True, blank=True)
    constraints = models.CharField(max_length=200, null=True, blank=True)
    assumptions = models.CharField(max_length=200, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_project')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_project')

    def get_absolute_url(self):
        return reverse('project-list')

    def __str__(self):
        return self.name


class AllocationType(ResourceManagementAbstract):
    name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=50)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_allocation_type')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_allocation_type')

    def get_absolute_url(self):
        return reverse('allocationtype-list')

    def __str__(self):
        return self.name


class BankHoliday(ResourceManagementAbstract):
    LOCATION = (('india', 'India'), ('uk', 'UK'), ('other', 'OTHER'))
    date = models.DateField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(choices=LOCATION, max_length=10)

    def __str__(self):
        return self.name


class ReccurringType(ResourceManagementAbstract):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Allocation(ResourceManagementAbstract):
    employee = models.ForeignKey(Employee, null=False, on_delete=MY_PROTECT, related_name='employee_allocation')
    project = models.ForeignKey(Project, null=False, on_delete=MY_PROTECT, related_name='employe_allocation_project')
    allocation_type = models.ForeignKey(AllocationType, null=False, on_delete=MY_PROTECT,
                                        related_name="employee_booking_type")
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    no_of_hours = models.IntegerField(default=8)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_allocation')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_allocation')

    def get_absolute_url(self):
        return reverse('allocation-list')

    def __str__(self):
        return '({}) Allocation for {} from {} to {} as {} for {} daily allocation hour(s) {}'.format(
            self.id,
            self.employee.first_name,
            self.start_date,
            self.end_date,
            self.allocation_type.name,
            self.project.name,
            self.no_of_hours)


class AllocationDetail(ResourceManagementAbstract):
    RECCURRING_TYPE = (('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'))
    allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE, related_name='allocation_detail_allocation')
    reccurring_type = models.CharField(choices=RECCURRING_TYPE, max_length=10)
    seperation_count = models.IntegerField(default=0, null=True)
    max_num_of_accurrences = models.IntegerField(default=0, null=True)
    day_of_week = models.IntegerField(default=0, null=True)
    week_of_month = models.IntegerField(default=0, null=True)
    day_of_month = models.IntegerField(default=0, null=True)
    month_of_year = models.IntegerField(default=0, null=True)

    def __str__(self):
        return '({}) Allocation for {} from {} to {} as {} for {} on {}'.format(
            self.allocation.id,
            self.allocation.employee.first_name,
            self.allocation.start_date,
            self.allocation.end_date,
            self.allocation.allocation_type.name,
            self.allocation.project.name,
            calendar.day_name[self.day_of_week])

from django.forms import ModelForm
from django import forms
from .models import (Department, AccountManager, Customer, ProjectType,
                     JobTitle, Employee, Skill, Project, CommercialStatus,
                     AllocationType, Allocation, AllocationDetail)
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.forms.models import inlineformset_factory


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        name = forms.CharField(required=True)
        discription = forms.CharField(required=False)

        labels = {
            'name': _('Name'),
            'description': _('Description')
        }
        help_text = {
            'name': _("Name"),
            "description": _("Description")
        }
        widgets = {
             'name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                            'placeholder': 'Enter department name'}),
             'description': forms.Textarea(attrs={'class': 'form-control form-control-user',
                                                  'placeholder': 'Enter event description'}),
        }
        error_messages = {
            'name': {
                'required': _('Please enter Department Name'),
            }
        }
        label_suffix = {
            'name': '*'
        }


class AccountManagerForm(ModelForm):

    class Meta:
        model = AccountManager
        fields = ['first_name', 'last_name', 'email', 'phone']
        first_name = forms.CharField(required=True)
        last_name = forms.CharField(required=True)
        email = forms.EmailField(required=True, validators=[validators.EmailValidator(message="Invalid Email")])
        phone = forms.CharField(required=False)
        labels = {
            'fisrt_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('EMail'),
            'phone': _('Phone')
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-user',
                                             'placeholder': 'Enter email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                            'placeholder': 'Enter phone number'}),
        }
        label_suffix = {
            'name': '*'
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'account_manager', 'description']
        name = forms.CharField()
        account_manager = forms.ModelChoiceField(queryset=AccountManager.objects.all())
        description = forms.CharField(required=False)

        labels = {
            'name': 'Customer Name',
            'account_manager': 'Account Manager',
            'description': 'Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                           'placeholder': 'Enter customer name'}),
            'account_manager': forms.Select(attrs={'class': 'form-control form-control-user',
                                                   'placeholder': 'Please select account manager'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-user',
                                                 'placeholder': 'Please enter description'}),
        }


class ProjectTypeForm(ModelForm):
    class Meta:
        model = ProjectType
        fields = ['name', 'description']
        name = forms.CharField(required=True)
        discription = forms.CharField(required=False)

        labels = {
            'name': _('Name'),
            'description': _('Description')
        }
        widgets = {
             'name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                            'placeholder': 'Please enter project type name'}),
             'description': forms.Textarea(attrs={'class': 'form-control form-control-user',
                                                  'placeholder': 'Please enter description'}),
        }
        label_suffix = {
            'name': '*'
        }


class JobTitleForm(ModelForm):
    class Meta:
        model = JobTitle
        fields = ['name', 'description']
        name = forms.CharField(required=True)
        discription = forms.CharField(required=False)

        labels = {
            'name': _('Name'),
            'description': _('Description')
        }
        help_text = {
            'name': _("Name"),
            "description": _("Description")
        }
        widgets = {
             'name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                            'placeholder': 'Please enter job titile'}),
             'description': forms.Textarea(attrs={'class': 'form-control form-control-user',
                                                  'placeholder': 'Please enter job description'}),
        }
        label_suffix = {
            'name': '*'
        }


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']
        name = forms.CharField(max_length=10)
        description = forms.CharField(max_length=100)
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        'description': forms.Textarea(attrs={'class': 'form-control form-control-user'}),
    }


class EmployeeForm(ModelForm):

    class Meta:
        LOCATION = (('india', 'India'), ('uk', 'UK'), ('other', 'OTHER'))
        model = Employee
        fields = ['emp_id',
                  'first_name',
                  'last_name',
                  'gender',
                  'date_of_joining',
                  'email',
                  'department',
                  'job_title',
                  'line_manager',
                  'skills',
                  'standard_hours',
                  'standard_charge_out_rate',
                  'resignation_date',
                  'last_date_of_working',
                  'location',
                  'include_in_capacity',
                  'is_active',
                  ]
        emp_id = forms.CharField(required=True, max_length=10)
        first_name = forms.CharField(required=True, max_length=100)
        last_name = forms.CharField(required=True, max_length=100)
        gender = forms.ChoiceField(choices=Employee.GENDER)
        date_of_joining = forms.DateField(required=True)
        resignation_date = forms.DateField()
        last_date_of_working = forms.DateField()
        job_title = forms.ModelChoiceField(required=True, queryset=JobTitle.objects.all())
        line_manager = forms.ModelChoiceField(required=False, queryset=Employee.objects.all())
        email = forms.EmailField(required=True, validators=[validators.EmailValidator(message="Invalid Email")])
        department = forms.ModelChoiceField(queryset=Department.objects.all())
        skills = forms.ModelMultipleChoiceField(required=True, queryset=Employee.objects.all())
        # location = forms.ModelMultipleChoiceField(queryset=LOCATION, required=True)
        is_active = forms.BooleanField(required=True)
        standard_hours = forms.IntegerField(required=True)
        standard_charge_out_rate = forms.DecimalField()
        include_in_capacity = forms.BooleanField(required=True)

        labels = {
            'emp_id': _('Employee ID'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'gender': _('Gender'),
            'date_of_joining': _('Date Of Joining'),
            'resignation_date': _('Resignation Date'),
            'last_date_of_working': _('Last Date Of working'),
            'designation': _('Designation'),
            'line_manager': _('Line Manager'),
            'email': _('Email'),
            'department': _('Department'),
            'skills': _('Skill(s)'),
            'active': 'Is Active?',
            'standard_hours': 'Standard working hours',
            'standard_charge_out_rate': 'Standard charge out rate',
            'include_in_capacity': 'Include in capacity planning?',
            'job_title': 'Job title',
        }
        widgets = {
            'emp_id': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                             'placeholder': 'Please enter employee number'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                 'placeholder': 'Please enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                'placeholder': 'Please enter last name'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-user'}),
            'resignation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-user'}),
            'last_date_of_working': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-user'}),
            'designation': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'line_manager': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-user',
                                             'placeholder': 'Please enter emial'}),
            'gender': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'department': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'location': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'skills': forms.CheckboxSelectMultiple(),
            'standard_hours':  forms.NumberInput(attrs={'class': 'form-control form-control-user',
                                                        'placeholder': 'Please enter standard working hours'}),
            'standard_charge_out_rate': forms.NumberInput(attrs={'class': 'form-control form-control-user',
                                                                 'placeholder':
                                                                     'Please enter standard charge out rate'}),
            'job_title': forms.Select(attrs={'class': 'form-control form-control-user'}),
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name',
                  'customer',
                  'project_type',
                  'start_date',
                  'end_date',
                  'commercial_status',
                  'project_phase',
                  'project_status',
                  'priority',
                  'project_health',
                  'customer_delivery_lead',
                  'service_delivery_manager',
                  'objective_and_deliverables',
                  'dependencies', 'constraints',
                  'assumptions',
                  ]
        name = forms.CharField(required=True, max_length=10)
        start_date = forms.DateField()
        end_date = forms.DateField()
        customer = forms.ModelChoiceField(required=True, queryset=Customer.objects.all())
        project_type = forms.ModelChoiceField(required=True, queryset=ProjectType.objects.all())
        customer_delivery_lead = forms.ModelChoiceField(required=True, queryset=Employee.objects.all())
        service_delivery_manager = forms.ModelChoiceField(required=True, queryset=Employee.objects.all())
        commercial_status = forms.ModelChoiceField(required=True, queryset=CommercialStatus.objects.all())

        labels = {
            'name': _('Project Name'),
            'start_date': _('Start Date'),
            'end_date': _('End Date'),
            'customer': _('Customer Name'),
            'project_type': _('Project Type'),
            'customer_delivery_lead': _('Customer Delivery Lead'),
            'service_delivery_manager': _('Service Delivery Manager'),
            'commercial_status': _('Commercial Status'),
            'objective_and_deliverables': 'Objective and deliverables',
            'dependencies': 'Dependencies',
            'constraints': 'Constraints',
            'assumptions': 'Assumptions',
            'project_phase': 'Project Phase',
            'project_status': 'Project Status',
            'priority': 'Priority',
            'project_health': 'Project Health',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-user',
                                           'placeholder': 'Please enter project name'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-user'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-user'}),
            'customer': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'project_type': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'customer_delivery_lead': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'service_delivery_manager': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'commercial_status': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'objective_and_deliverables': forms.Textarea(attrs={'class': 'form-control form-control-user',
                                                                'placeholder':
                                                                    'Please enter project objective and deliverables'}),
            'dependencies': forms.Textarea(attrs={'class': 'form-control form-control-user',
                                                  'placeholder': 'Please enter dependencies'}),
            'constraints': forms.Textarea(attrs={'class': 'form-control form-control-user',
                                                 'placeholder': 'Please enter constraints'}),
            'assumptions': forms.Textarea(attrs={'class': 'form-control form-control-user',
                                                 'placeholder': 'Please enter assumptions'}),
            'project_phase': forms.Select(attrs={'class': 'form-control form-control-user', }),
            'project_status': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'priority': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'project_health': forms.Select(attrs={'class': 'form-control form-control-user'}),
        }


class AllocationForm(ModelForm):
    days_of_week = forms.MultipleChoiceField(choices=(
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        return initial

    class Meta:
        model = Allocation
        fields = ['employee', 'project', 'allocation_type', 'start_date', 'end_date', 'no_of_hours', 'days_of_week']

        employee = forms.ModelChoiceField(required=True, queryset=Employee.objects.all())
        project = forms.ModelChoiceField(required=True, queryset=Project.objects.all())
        allocation_type = forms.ModelChoiceField(required=True, queryset=AllocationType.objects.all())
        start_date = forms.DateField()
        end_date = forms.DateField()
        no_of_hours = forms.NumberInput()

        labels = {
            'employee': _('Employee Name'),
            'project': _('Project Name'),
            'allocation_type': _('Allocation Type'),
            'start_date': _('Start Date'),
            'end_date': _('End Date'),
            'no_of_hours': _('Number of hours'),
            'days_of_week': _('Days of week'),
        }
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'project': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'allocation_type': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-user'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-user'}),
            'no_of_hours': forms.NumberInput(attrs={'class': 'form-control form-control-user'}),
            'days_of_week': forms.CheckboxSelectMultiple(),
        }


class AllocationFilterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].initial = '17/04/1981'
        self.fields['end_date'].initial = '17/04/1981'

    start_date = forms.DateField()
    end_date = forms.DateField()

    class Meta:
        model = Allocation
        fields = ['start_date', 'end_date']

        start_date = forms.DateField(required=True)
        end_date = forms.DateField(required=True)

        widgets = {
            'start_date': forms.DateInput(),
            'end_date': forms.DateInput()
        }


class WeeklyRecurrenceForm(ModelForm):
    days_of_week = forms.MultipleChoiceField(choices=(
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = AllocationDetail
        fields = ['days_of_week']

        labels = {
            'days_of_week': _('Day of week'),
        }
        widgets = {
            'days_of_week': forms.CheckboxSelectMultiple(),
        }


WeeklyRecurrenceFormSet = inlineformset_factory(Allocation, AllocationDetail, form=WeeklyRecurrenceForm,  extra=1)

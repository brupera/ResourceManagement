from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import (DepartmentForm, AccountManagerForm,
                    CustomerForm, ProjectTypeForm, JobTitleForm,
                    EmployeeForm, ProjectForm, AllocationForm)
from .models import (Department, AccountManager, Customer, ProjectType,
                     JobTitle, Employee, Project, AllocationType,
                     Allocation, AllocationDetail)
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from .utils import TimeLineCalendar
from django.utils.safestring import mark_safe
from rest_framework.views import APIView
from rest_framework.response import Response
from dateutil import parser


@login_required(login_url='login')
def home(request):
    return render(request, 'index.html')


def login(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        paassword = request.POST['paassword']

    user = authenticate(username=username, password=paassword)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('')
    return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    logout(request)


'''
DEPARTMENT VIEWS
'''


class DepartmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Department
    context_object_name = 'departments'
    queryset = Department.objects.all()
    template_name = 'department/department_list.html'
    paginate_by = 1
    permission_required = 'resource_management_app.view_department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get("datatables"):
            # Get the datatable parameters from the request
            draw = int(self.request.GET.get("draw", "1"))
            start = int(self.request.GET.get("start", "0"))
            length = int(self.request.GET.get("length", "10"))
            order_column_index = int(self.request.GET.get('order[0][column]', 0))
            order_direction = self.request.GET.get('order[0][dir]', 'asc')
            sv = self.request.GET.get("search[value]", None)

            # Determine the column to sort by
            columns = ['name', 'description']  # Replace with your column names
            order_column = columns[order_column_index]
            # replacing desc and asc befcause Django is accepting blank for assending order and - for decanding order
            order_direction = order_direction.replace('asc', '')
            order_direction = order_direction.replace('desc', '-')

            qs = self.get_queryset()
            if sv:
                qs = qs.filter(
                    Q(name__icontains=sv)
                    | Q(description__icontains=sv)
                )
            filtered_count = qs.count()
            qs = qs.order_by(f'{order_direction}{order_column}')
            qs = qs[start: start + length]

            return JsonResponse(
                {
                    "recordsTotal": self.get_queryset().count(),
                    "recordsFiltered": filtered_count,
                    "draw": draw,
                    "data": list(qs.values()),
                },
                safe=False,
            )
        return super().render_to_response(context, **response_kwargs)


class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Department
    template_name = 'department/department_add_or_update.html'
    redirect_field_name = 'department/department_list.html'
    form_class = DepartmentForm
    permission_required = 'resource_management_app.add_department'

    def form_valid(self, form):
        form.instance.version = 1
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department/department_add_or_update.html'
    permission_required = 'resource_management_app.change_department'
    redirect_field_name = 'department/department_list.html'

    # template_name_suffix = '_update_form'
    def form_valid(self, form):
        form.instance.version = form.instance.version + 1
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Department
    context_object_name = 'department'
    template_name = 'department/department_delete.html'
    success_url = '/department/'
    permission_required = 'resource_management_app.delete_department'

    def form_valid(self, form):
        messages.success(self.request, "The Department was deleted successfully.")
        return super(DepartmentDeleteView, self).form_valid(form)


'''
CUSTOMER VIEWS
'''


class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Customer
    context_object_name = 'customers'
    queryset = Customer.objects.all()
    template_name = 'customer/customer_list.html'
    # paginate_by = 1
    permission_required = 'resource_management_app.view_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get("datatables"):
            draw = int(self.request.GET.get("draw", "1"))
            start = int(self.request.GET.get("start", "0"))
            length = int(self.request.GET.get("length", "10"))
            order_column_index = int(self.request.GET.get('order[0][column]', 0))
            order_direction = self.request.GET.get('order[0][dir]', 'asc')
            sv = self.request.GET.get("search[value]", None)

            # Determine the column to sort by
            columns = ['name', 'description', 'account_manager__first_name']  # Replace with your column names
            order_column = columns[order_column_index]
            # replacing desc and asc befcause Django is accepting blank for assending order and - for decanding order
            order_direction = order_direction.replace('asc', '')
            order_direction = order_direction.replace('desc', '-')

            qs = self.get_queryset().order_by("name")
            if sv:
                qs = qs.filter(
                    Q(name__icontains=sv)
                    | Q(description__icontains=sv)
                    | Q(account_manager__first_name__icontains=sv)
                )
            filtered_count = qs.count()
            qs = qs.order_by(f'{order_direction}{order_column}')
            qs = qs[start: start + length]

            return JsonResponse(
                {
                    "recordsTotal": self.get_queryset().count(),
                    "recordsFiltered": filtered_count,
                    "draw": draw,
                    "data": list(qs.values('id', 'name', 'description', 'account_manager__first_name')),
                },
                safe=False,
            )
        return super().render_to_response(context, **response_kwargs)


class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Customer
    template_name = 'customer/customer_add_or_update.html'
    redirect_field_name = 'customer/customer_list.html'
    form_class = CustomerForm
    permission_required = 'resource_management_app.add_customer'

    def form_valid(self, form):
        form.instance.version = 1
        form.instance.updated_by = self.request.user
        form.instance.created_by = self.request.user

        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_add_or_update.html'
    permission_required = 'resource_management_app.change_customer'
    redirect_field_name = 'customer/customer_list.html'

    def form_valid(self, form):
        form.instance.version += 1
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'customer/customer_delete.html'
    success_url = '/customer/'
    permission_required = 'resource_management_app.delete_customer'

    def form_valid(self, form):
        messages.success(self.request, "The Customer was deleted successfully.")
        return super(CustomerDeleteView, self).form_valid(form)


'''
ACCOUNT MANAGER VIEWS
'''


class AccountManagerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AccountManager
    context_object_name = 'accountmanagers'
    queryset = AccountManager.objects.all()
    template_name = 'accountmanager/accountmanager_list.html'
    # paginate_by = 1
    permission_required = 'resource_management_app.view_accountmanager'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get("datatables"):
            draw = int(self.request.GET.get("draw", "1"))
            start = int(self.request.GET.get("start", "0"))
            length = int(self.request.GET.get("length", "10"))
            order_column_index = int(self.request.GET.get('order[0][column]', 0))
            order_direction = self.request.GET.get('order[0][dir]', 'asc')
            sv = self.request.GET.get("search[value]", None)

            # Determine the column to sort by
            columns = ['first_name', 'last_name', 'email', 'phone']  # Replace with your column names
            order_column = columns[order_column_index]
            # replacing desc and asc befcause Django is accepting blank for assending order and - for decanding order
            order_direction = order_direction.replace('asc', '')
            order_direction = order_direction.replace('desc', '-')

            qs = self.get_queryset().order_by("first_name")
            if sv:
                qs = qs.filter(
                    Q(first_name__icontains=sv)
                    | Q(last_name__icontains=sv)
                    | Q(email__icontains=sv)
                    | Q(phone__icontains=sv)
                )
            filtered_count = qs.count()
            qs = qs.order_by(f'{order_direction}{order_column}')
            qs = qs[start: start + length]

            return JsonResponse(
                {
                    "recordsTotal": self.get_queryset().count(),
                    "recordsFiltered": filtered_count,
                    "draw": draw,
                    "data": list(qs.values('id', 'first_name', 'last_name', 'email', 'phone')),
                },
                safe=False,
            )
        return super().render_to_response(context, **response_kwargs)


class AccountManagerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = AccountManager
    template_name = 'accountmanager/accountmanager_add_or_update.html'
    redirect_field_name = 'accountmanager/accountmanager_list.html'
    form_class = AccountManagerForm
    permission_required = 'resource_management_app.add_accountmanager'

    def form_valid(self, form):
        form.instance.version = 1
        form.instance.updated_by = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AccountManagerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = AccountManager
    form_class = AccountManagerForm
    template_name = 'accountmanager/accountmanager_add_or_update.html'
    permission_required = 'resource_management_app.change_accountmanager'
    redirect_field_name = 'accountmanager/accountmanager_list.html'

    def form_valid(self, form):
        form.instance.version += 1
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class AccountManagerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = AccountManager
    context_object_name = 'accountmanager'
    template_name = 'accountmanager/accountmanager_delete.html'
    success_url = '/accountmanager/'
    permission_required = 'resource_management_app.delete_accountmanager'

    def form_valid(self, form):
        messages.success(self.request, "The Account Manaager was deleted successfully.")
        return super(AccountManagerDeleteView, self).form_valid(form)


'''
PROJECT TYPE VIEWS
'''


class ProjectTypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ProjectType
    context_object_name = 'projecttypes'
    queryset = ProjectType.objects.all()
    template_name = 'projecttype/projecttype_list.html'
    permission_required = 'resource_management_app.view_projecttype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get("datatables"):
            draw = int(self.request.GET.get("draw", "1"))
            start = int(self.request.GET.get("start", "0"))
            length = int(self.request.GET.get("length", "10"))
            order_column_index = int(self.request.GET.get('order[0][column]', 0))
            order_direction = self.request.GET.get('order[0][dir]', 'asc')
            sv = self.request.GET.get("search[value]", None)

            # Determine the column to sort by
            columns = ['name', 'description']  # Replace with your column names
            order_column = columns[order_column_index]
            # replacing desc and asc befcause Django is accepting blank for assending order and - for decanding order
            order_direction = order_direction.replace('asc', '')
            order_direction = order_direction.replace('desc', '-')

            qs = self.get_queryset().order_by("name")
            if sv:
                qs = qs.filter(
                    Q(name__icontains=sv)
                    | Q(description__icontains=sv)
                )
            filtered_count = qs.count()
            qs = qs.order_by(f'{order_direction}{order_column}')
            qs = qs[start: start + length]

            return JsonResponse(
                {
                    "recordsTotal": self.get_queryset().count(),
                    "recordsFiltered": filtered_count,
                    "draw": draw,
                    "data": list(qs.values('id', 'name', 'description')),
                },
                safe=False,
            )
        return super().render_to_response(context, **response_kwargs)


class ProjectTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProjectType
    template_name = 'projecttype/projecttype_add_or_update.html'
    redirect_field_name = 'projecttype/projecttype_list.html'
    form_class = ProjectTypeForm
    permission_required = 'resource_management_app.add_projecttype'

    def form_valid(self, form):
        form.instance.version = 1
        form.instance.updated_by = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProjectTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProjectType
    form_class = ProjectTypeForm
    template_name = 'projecttype/projecttype_add_or_update.html'
    permission_required = 'resource_management_app.change_projecttype'
    redirect_field_name = 'projecttype/projecttype_list.html'

    def form_valid(self, form):
        form.instance.version += 1
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ProjectTypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProjectType
    context_object_name = 'projecttype'
    template_name = 'projecttype/projecttype_delete.html'
    success_url = '/projecttype/'
    permission_required = 'resource_management_app.delete_projecttype'

    def form_valid(self, form):
        messages.success(self.request, "The Project Type was deleted successfully.")
        return super(ProjectTypeDeleteView, self).form_valid(form)


'''
JOB TITLE VIEWS
'''


class JobTitleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = JobTitle
    context_object_name = 'jobtitles'
    queryset = JobTitle.objects.all()
    template_name = 'jobtitle/jobtitle_list.html'
    permission_required = 'resource_management_app.view_jobtitle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get("datatables"):
            draw = int(self.request.GET.get("draw", "1"))
            start = int(self.request.GET.get("start", "0"))
            length = int(self.request.GET.get("length", "10"))
            order_column_index = int(self.request.GET.get('order[0][column]', 0))
            order_direction = self.request.GET.get('order[0][dir]', 'asc')
            sv = self.request.GET.get("search[value]", None)

            # Determine the column to sort by
            columns = ['name', 'description']  # Replace with your column names
            order_column = columns[order_column_index]
            # replacing desc and asc befcause Django is accepting blank for assending order and - for decanding order
            order_direction = order_direction.replace('asc', '')
            order_direction = order_direction.replace('desc', '-')

            qs = self.get_queryset().order_by("name")
            if sv:
                qs = qs.filter(
                    Q(name__icontains=sv)
                    | Q(description__icontains=sv)
                )
            filtered_count = qs.count()
            qs = qs.order_by(f'{order_direction}{order_column}')
            qs = qs[start: start + length]

            return JsonResponse(
                {
                    "recordsTotal": self.get_queryset().count(),
                    "recordsFiltered": filtered_count,
                    "draw": draw,
                    "data": list(qs.values('id', 'name', 'description')),
                },
                safe=False,
            )
        return super().render_to_response(context, **response_kwargs)


class JobTitleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = JobTitle
    template_name = 'jobtitle/jobtitle_add_or_update.html'
    redirect_field_name = 'jobtitle/jobtitle_list.html'
    form_class = JobTitleForm
    permission_required = 'resource_management_app.add_jobtitle'

    def form_valid(self, form):
        form.instance.version = 1
        form.instance.updated_by = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class JobTitleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = JobTitle
    form_class = JobTitleForm
    template_name = 'jobtitle/jobtitle_add_or_update.html'
    permission_required = 'resource_management_app.change_jobtitle'
    redirect_field_name = 'jobtitle/jobtitle_list.html'

    def form_valid(self, form):
        form.instance.version += 1
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class JobTitleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = JobTitle
    context_object_name = 'jobtitle'
    template_name = 'jobtitle/jobtitle_delete.html'
    success_url = '/jobtitle/'
    permission_required = 'resource_management_app.delete_jobtitle'

    def form_valid(self, form):
        messages.success(self.request, "The Job Title was deleted successfully.")
        return super(DesignationDeleteView, self).form_valid(form)


'''
EMPLOYEE VIEWS
'''


class EmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Employee
    context_object_name = 'employees'
    queryset = Employee.objects.all()
    template_name = 'employee/employee_list.html'
    permission_required = 'resource_management_app.view_employee'

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get("datatables"):
            draw = int(self.request.GET.get("draw", "1"))
            start = int(self.request.GET.get("start", "0"))
            length = int(self.request.GET.get("length", "10"))
            order_column_index = int(self.request.GET.get('order[0][column]', 0))
            order_direction = self.request.GET.get('order[0][dir]', 'asc')
            sv = self.request.GET.get("search[value]", None)

            # Determine the column to sort by
            columns = ['emp_id','first_name', 'last_name', 'job_title__name', 'line_manager__first_name',
                       'skills__name']  # Replace with your column names
            order_column = columns[order_column_index]
            # replacing desc and asc befcause Django is accepting blank for assending order and - for decanding order
            order_direction = order_direction.replace('asc', '')
            order_direction = order_direction.replace('desc', '-')

            qs = self.get_queryset().order_by("first_name")
            if sv:
                qs = qs.filter(
                    Q(first_name__icontains=sv)
                    | Q(last_name__icontains=sv)
                    | Q(job_title__name__contains=sv)
                    | Q(line_manager__first_name__contains=sv)
                    | Q(skills__name__contains=sv)
                )
            filtered_count = qs.count()
            qs = qs.order_by(f'{order_direction}{order_column}').distinct()
            qs = qs[start: start + length]

            return JsonResponse(
                {
                    "recordsTotal": self.get_queryset().count(),
                    "recordsFiltered": filtered_count,
                    "draw": draw,
                    "data": list([
                        {'id': e.id,
                         'emp_id': e.emp_id,
                         'first_name': e.first_name,
                         'last_name': e.last_name,
                         'job_title__name': e.job_title.name,
                         'line_manager__first_name': e.line_manager.first_name,
                         'skills__name': [s.name for s in e.skills.all().distinct()]}
                        for e in qs.prefetch_related('skills')
                    ])

                },
                safe=False,
            )
        return super().render_to_response(context, **response_kwargs)


class EmployeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Employee
    template_name = 'employee/employee_add_or_update.html'
    redirect_field_name = 'employee/employee_list.html'
    form_class = EmployeeForm
    permission_required = 'resource_management_app.add_employee'

    def form_valid(self, form):
        form.instance.version = 1
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class EmployeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_add_or_update.html'
    permission_required = 'resource_management_app.change_employee'
    redirect_field_name = 'employee/employee_list.html'

    def form_valid(self, form):
        form.instance.version += 1
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class EmployeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employee/employee_delete.html'
    success_url = '/employee/'
    permission_required = 'resource_management_app.delete_employee'

    def form_valid(self, form):
        messages.success(self.request, "The Employee was deleted successfully.")
        return super(EmployeeDeleteView, self).form_valid(form)


'''
PROJECT VIEWS
'''


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    queryset = Project.objects.all()
    template_name = 'project/project_list.html'
    permission_required = 'resource_management_app.view_project'

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get("datatables"):
            draw = int(self.request.GET.get("draw", "1"))
            start = int(self.request.GET.get("start", "0"))
            length = int(self.request.GET.get("length", "10"))
            order_column_index = int(self.request.GET.get('order[0][column]', 0))
            order_direction = self.request.GET.get('order[0][dir]', 'asc')
            sv = self.request.GET.get("search[value]", None)

            # Determine the column to sort by
            columns = ['name', 'start_date', 'end_date', 'customer__name', 'project_type__name',
                       'customer_delivery_lead__first_name', 'service_delivery_manager__first_name']
            order_column = columns[order_column_index]
            # replacing desc and asc befcause Django is accepting blank for assending order and - for decanding order
            order_direction = order_direction.replace('asc', '')
            order_direction = order_direction.replace('desc', '-')

            qs = self.get_queryset().order_by("name")
            if sv:
                qs = qs.filter(
                    Q(name__icontains=sv)
                    | Q(start_date__icontains=sv)
                    | Q(start_date__icontains=sv)
                    | Q(end_date__icontains=sv)
                    | Q(customer__name__icontains=sv)
                    | Q(project_type__name__icontains=sv)
                    | Q(customer_delivery_lead__first_name__icontains=sv)
                    | Q(service_delivery_manager__first_name__icontains=sv)
                )
            filtered_count = qs.count()
            qs = qs.order_by(f'{order_direction}{order_column}')
            qs = qs[start: start + length]

            return JsonResponse(
                {
                    "recordsTotal": self.get_queryset().count(),
                    "recordsFiltered": filtered_count,
                    "draw": draw,
                    "data": list(qs.values('id', 'name', 'start_date', 'end_date',
                                           'customer__name', 'project_type__name',
                                           'customer_delivery_lead__first_name',
                                           'service_delivery_manager__first_name'))

                },
                safe=False,
            )
        return super().render_to_response(context, **response_kwargs)


class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'project/project_add_or_update.html'
    redirect_field_name = 'project/project_list.html'
    form_class = ProjectForm
    permission_required = 'resource_management_app.add_project'

    def form_valid(self, form):
        form.instance.version = 1
        form.instance.updated_by = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_add_or_update.html'
    permission_required = 'resource_management_app.change_project'
    redirect_field_name = 'project/project_list.html'

    def form_valid(self, form):
        form.instance.version += 1
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Project
    context_object_name = 'project'
    template_name = 'project/project_delete.html'
    success_url = '/project/'
    permission_required = 'resource_management_app.delete_project'

    def form_valid(self, form):
        messages.success(self.request, "The Project was deleted successfully.")
        return super(ProjectDeleteView, self).form_valid(form)


'''
EMPLOYEE ALLOCATION
'''


class AllocationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Allocation
    context_object_name = 'allocation'
    queryset = Allocation.objects.all()
    template_name = 'allocation/allocation_list.html'
    permission_required = 'resource_management_app.view_allocation'

    def get_context_data(self, **kwargs):
        context = super(AllocationListView, self).get_context_data(**kwargs)
        context = {"allocation_types": AllocationType.objects.all()}
        return context


class CapacityView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Allocation
    context_object_name = 'allocation'
    queryset = Allocation.objects.all()
    template_name = 'allocation/capacity_view.html'
    permission_required = 'resource_management_app.view_allocation'

    def get_context_data(self, **kwargs):
        context = super(CapacityView, self).get_context_data(**kwargs)
        return context


class AllocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Allocation
    template_name = 'allocation/allocation_add_or_update.html'
    redirect_field_name = 'allocation/allocation_list.html'
    form_class = AllocationForm
    permission_required = 'resource_management_app.add_allocation'

    def get_context_data(self, **kwargs):
        context = super(AllocationCreateView, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():

            form.instance.updated_by = self.request.user
            form.instance.created_by = self.request.user
            allocation = form.save()

            for day in form.cleaned_data['days_of_week']:
                print(day)
                detail = AllocationDetail()

                detail.allocation = allocation
                detail.day_of_week = day
                detail.reccurring_type = 'weekly'
                detail.max_num_of_accurrences = (allocation.end_date - allocation.start_date).days
                detail.version += 1
                detail.is_deleted = 0
                detail.created_at = self.request.user
                detail.updated_at = self.request.user

                detail.save()

            return redirect('allocation-list')
            # return self.form_valid(form, allocation_daily_recurrence_formset, allocation_weekly_recurrence_formset)
        else:
            return self.form_invalid(form)


class AllocationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Allocation
    form_class = AllocationForm
    template_name = 'allocation/allocation_add_or_update.html'
    permission_required = 'resource_management_app.change_allocation'
    redirect_field_name = 'allocation/allocation_list.html'

    def get_initial(self):
        initial = super(AllocationUpdateView, self).get_initial()
        initial['days_of_week'] = self.getAllocatedDays(self.object)
        return initial

    def getAllocatedDays(self, allocation):
        items = []
        allocation_details = AllocationDetail.objects.filter(allocation=allocation)
        for item in allocation_details:
            items.append(item.day_of_week)

        return items

    def form_valid(self, form):
        form.instance.version += 1
        form.instance.updated_by = self.request.user

        if form.is_valid():
            allocation = form.save()

            AllocationDetail.objects.filter(allocation=allocation).delete()

            for day in form.cleaned_data['days_of_week']:
                print(day)
                detail = AllocationDetail()

                detail.allocation = allocation
                detail.day_of_week = day
                detail.reccurring_type = 'weekly'
                detail.max_num_of_accurrences = (allocation.end_date - allocation.start_date).days
                detail.version += 1
                detail.is_deleted = 0
                detail.created_at = self.request.user
                detail.updated_at = self.request.user
                detail.save()

        return super().form_valid(form)

class AllocationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Allocation
    context_object_name = 'allocation'
    template_name = 'allocation/allocation_delete.html'
    success_url = '/allocation/'
    permission_required = 'resource_management_app.delete_allocation'

    def form_valid(self, form):
        messages.success(self.request, "The Allocation was deleted successfully.")
        return super(AllocationDeleteView, self).form_valid(form)

class AllocationListViewAPI(APIView):

    def get(self, request):
        start_date = parser.parse(self.request.GET.get("start_date")).date()
        end_date = parser.parse(self.request.GET.get("end_date")).date()

        cal = TimeLineCalendar(start_date, end_date)

        html_cal = cal.gettimelinecalendar()
        context = {"calendar": mark_safe(html_cal)}

        return Response(context)


class CapacityViewAPI(APIView):

    def get(self, request):
        start_date = parser.parse(self.request.GET.get("start_date")).date()
        end_date = parser.parse(self.request.GET.get("end_date")).date()

        cal = TimeLineCalendar(start_date, end_date)
        html_cal = cal.capacitycalendar()
        context = {"calendar": mark_safe(html_cal)}

        return Response(context)

from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index.html', views.home, name='index'),
    path('', views.home, name='index'),
    # path('department/new', views.createDepartment, name='new_department'),
    path('department/', views.DepartmentListView.as_view(), name="department-list"),
    path('department/create', views.DepartmentCreateView.as_view(), name="department-create"),
    path('department/update/<int:pk>', views.DepartmentUpdateView.as_view(), name="department-update"),
    path('department/delete/<int:pk>', views.DepartmentDeleteView.as_view(), name="department-delete"),

    path('customer/', views.CustomerListView.as_view(), name="customer-list"),
    path('customer/create/', views.CustomerCreateView.as_view(), name="customer-create"),
    path('customer/update/<int:pk>', views.CustomerUpdateView.as_view(), name="customer-update"),
    path('customer/delete/<int:pk>', views.CustomerDeleteView.as_view(), name="customer-delete"),

    path('accountmanager/', views.AccountManagerListView.as_view(), name="accountmanager-list"),
    path('accountmanager/create', views.AccountManagerCreateView.as_view(), name="accountmanager-create"),
    path('accountmanager/update/<int:pk>', views.AccountManagerUpdateView.as_view(), name="accountmanager-update"),
    path('accountmanager/delete/<int:pk>', views.AccountManagerDeleteView.as_view(), name="accountmanager-delete"),

    path('projecttype/', views.ProjectTypeListView.as_view(), name="projecttype-list"),
    path('projecttype/create', views.ProjectTypeCreateView.as_view(), name="projecttype-create"),
    path('projecttype/update/<int:pk>', views.ProjectTypeUpdateView.as_view(), name="projecttype-update"),
    path('projecttype/delete/<int:pk>', views.ProjectTypeDeleteView.as_view(), name="projecttype-delete"),

    path('jobtitle/', views.JobTitleListView.as_view(), name="jobtitle-list"),
    path('jobtitle/create', views.JobTitleCreateView.as_view(), name="jobtitle-create"),
    path('jobtitle/update/<int:pk>', views.JobTitleUpdateView.as_view(), name="jobtitle-update"),
    path('jobtitle/delete/<int:pk>', views.JobTitleDeleteView.as_view(), name="jobtitle-delete"),

    path('employee/', views.EmployeeListView.as_view(), name="employee-list"),
    path('employee/create', views.EmployeeCreateView.as_view(), name="employee-create"),
    path('employee/update/<int:pk>', views.EmployeeUpdateView.as_view(), name="employee-update"),
    path('employee/delete/<int:pk>', views.EmployeeDeleteView.as_view(), name="employee-delete"),

    path('project/', views.ProjectListView.as_view(), name="project-list"),
    path('project/create', views.ProjectCreateView.as_view(), name="project-create"),
    path('project/update/<int:pk>', views.ProjectUpdateView.as_view(), name="project-update"),
    path('project/delete/<int:pk>', views.ProjectDeleteView.as_view(), name="project-delete"),

    path('allocation/', views.AllocationListView.as_view(), name="allocation-list"),
    path('allocation/capacity', views.CapacityView.as_view(), name="capacity-view"),
    path('allocation/create', views.AllocationCreateView.as_view(), name="allocation-create"),
    path('allocation/update/<int:pk>', views.AllocationUpdateView.as_view(), name="allocation-update"),
    path('allocation/delete/<int:pk>', views.AllocationDeleteView.as_view(), name="allocation-delete"),

    path('', views.home, name='index'),
    path('accounts/logout/', views.logout, name='logout'),

    path('api/allocations/', views.AllocationListViewAPI.as_view()),
    path('api/allocations/capacity', views.CapacityViewAPI.as_view()),
]

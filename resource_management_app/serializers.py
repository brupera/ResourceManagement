from rest_framework import serializers
from .models import Employee, Allocation, AllocationDetail, Skill


class AllocationDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AllocationDetail
        fields = ['day_of_week',
                  'seperation_count',
                  'reccurring_type',
                  'max_num_of_accurrences',
                  'week_of_month',
                  'day_of_month',
                  'month_of_year',
                  ]
        depth = 1


class AllocationSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    project = serializers.CharField(source='project.name')
    allocation_type = serializers.CharField(source='allocation_type.name')
    allocation_type_color_code = serializers.CharField(source='allocation_type.color_code')

    class Meta:
        model = Allocation
        fields = ['start_date',
                  'end_date',
                  'no_of_hours',
                  'project',
                  'allocation_type',
                  'allocation_type_color_code',
                  'details']
        depth = 1

    def get_details(self, allocation):
        return AllocationDetailSerializer(AllocationDetail.objects.filter(allocation=allocation), many=True).data


class EmployeeSerializer(serializers.ModelSerializer):
    allocations = serializers.SerializerMethodField()
    job_title = serializers.CharField(source='job_title.name')
    line_manager = serializers.CharField(source='line_manager.first_name')
    skills = serializers.ListField(source='skills.name')

    class Meta:
        model = Employee
        fields = ['emp_id',
                  'first_name',
                  'last_name',
                  'date_of_joining',
                  'job_title',
                  'resignation_date',
                  'last_date_of_working',
                  'line_manager',
                  'skills',
                  'allocations']
        depth = 3

    def get_allocations(self, employee):
        return AllocationSerializer(Allocation.objects.filter(employee=employee), many=True).data


class AllocationGridSerializer(serializers.Serializer):
    id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    date_of_joining = serializers.CharField()
    job_title = serializers.CharField()
    resignation_date = serializers.CharField()
    last_date_of_working = serializers.CharField()
    series = serializers.ListField()

    def to_representation(self, instance):
        # Customize the serialization process
        # Create a dictionary representing the custom JSON structure
        allocations = Allocation.objects.filter(employee=instance)
        allocated_days = []
        for allocation in allocations:
            days = AllocationDetail.objects.filter(allocation=allocation)
            for day in days:
                print(day)
                allocated_days.append({'name': allocation.project.name,
                                       'allocation_type': allocation.allocation_type.name,
                                       'color': allocation.allocation_type.color_code,
                                       'start': allocation.start_date,
                                       'end': allocation.end_date,
                                       'day_of_week': day.day_of_week})

        custom_data = {
            'id': instance.emp_id,
            'name': instance.first_name,
            'last_name': instance.last_name,
            'date_of_joining': instance.date_of_joining,
            'job_title': instance.job_title.name,
            'resignation_date': instance.resignation_date,
            'last_date_of_working': instance.last_date_of_working,
            'series': allocated_days
            # Customize more fields as needed
        }
        return custom_data

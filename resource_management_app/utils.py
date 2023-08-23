from datetime import datetime, timedelta
from .models import Allocation, AllocationDetail, Employee, Project
from django.db.models import Q


class TimeLineCalendar:
    class Booking:
        allocation_id = 0
        project = ''
        allocation_type = ''
        day_of_week = 0
        start_date = datetime.now()
        end_date = datetime.now()
        no_of_hours = 0
        color_code = ''

    def __init__(self, start_date=None, end_date=None):
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def get_month_header(start_date, end_date):
        delta = timedelta(days=1)
        month_td = ''
        current_month = start_date.strftime("%b")
        month_col_span = 0

        while start_date <= end_date:
            if current_month == start_date.strftime("%b"):
                month_col_span += 1
            else:
                month_td += '<th colspan="{}" scope="row" style="text-align: center;vertical-align: middle;">{}</th>'\
                    .format(month_col_span, current_month + "/" + start_date.strftime('%y'))
                current_month = start_date.strftime("%b")
                month_col_span = 1

            start_date += delta

        # loop ends once look reaches end_date hence not getting opportunity to add last month name. Due to that
        # added this manual entry in tail end of the loop
        month_td += '<th colspan="{}" scope="row" style="text-align: center;vertical-align: middle;">{}</th>'.format(
            month_col_span, current_month + "/" + start_date.strftime('%y'))

        return month_td

    @staticmethod
    def get_week_header(start_date, end_date):
        delta = timedelta(days=1)
        week_td = ''
        current_week = start_date.strftime("%W")
        week_col_span = 0

        while start_date <= end_date:
            if current_week == start_date.strftime("%W"):
                week_col_span += 1
            else:
                wc_date = start_date - delta * 2
                week_commencing = wc_date - timedelta(days=wc_date.weekday() % 7)

                week_td += '<th colspan="{}" class="week-commencing">{}</th>'.format(
                    week_col_span, week_commencing.strftime("%d-%m"))
                current_week = start_date.strftime("%W")
                week_col_span = 1

            start_date += delta

        wc_date = start_date - delta * 2
        week_commencing = wc_date - timedelta(days=wc_date.weekday() % 7)
        # loop ends once look reaches end_date hence not getting opportunity to add last month name. Due to that
        # added this manual entry in tail end of the loop
        week_td += '<th colspan="{}" class="week-commencing">{}</th>'.format(
            week_col_span, week_commencing.strftime("%d-%m"))

        return week_td

    @staticmethod
    def get_week_header_v2(start_date, end_date):
        delta = timedelta(days=1)
        week_td = ''
        current_week = start_date.strftime("%W")

        while start_date < end_date:
            if current_week != start_date.strftime("%W"):
                wc_date = start_date - delta * 2
                week_commencing = wc_date - timedelta(days=wc_date.weekday() % 7)

                week_td += '<th>{}</th>'.format(
                    week_commencing.strftime("%d-%m"))
                current_week = start_date.strftime("%W")
            start_date += delta

        wc_date = start_date - delta * 2
        week_commencing = wc_date - timedelta(days=wc_date.weekday() % 7)
        # loop ends once look reaches end_date hence not getting opportunity to add last month name. Due to that
        # added this manual entry in tail end of the loop
        week_td += '<th>{}</th>'.format(
            week_commencing.strftime("%d-%m"))

        return week_td

    @staticmethod
    def get_date_range_header(start_date, end_date):
        delta = timedelta(days=1)
        date_td = ''

        while start_date <= end_date:
            date_td += '<th class="weekday">{}</th>'.format(
                start_date.strftime("%a")[0])
            start_date += delta

        return date_td

    @staticmethod
    def is_weekend(date_to_check):
        if date_to_check.strftime("%a") == "Sat" or \
                date_to_check.strftime("%a") == "Sun":
            return True
        else:
            return False

    @staticmethod
    def get_week_commencing_date(date_to_check):
        delta = timedelta(days=1)
        wc_date = date_to_check - delta * 2
        return wc_date - timedelta(days=wc_date.weekday() % 7)


    def is_bank_holiday(self, date_to_check):
        bank_holidays = self.get_bank_holidays()

        if date_to_check.strftime("%d-%m-%Y") in bank_holidays:
            return True
        else:
            return False

    @staticmethod
    def get_bank_holidays():
        # TODO: Replace constant values with database
        bank_holidays = {}

        bank_holidays['21-04-2023'] = 'Eid-ul-Fitr'
        bank_holidays['15-08-2023'] = 'Independence Day'
        bank_holidays['30-08-2023'] = 'Rakshabandhan'
        bank_holidays['24-10-2023'] = 'Dusshera'
        bank_holidays['13-11-2023'] = 'New Year'
        bank_holidays['14-11-2023'] = 'Bhai Duj'
        bank_holidays['25-12-2023'] = 'Christmas'
        bank_holidays['15-01-2024'] = 'Vasi Uttrayan'
        bank_holidays['26-01-2024'] = 'Republic Day'
        bank_holidays['25-03-2024'] = 'Dhuleti'

        return bank_holidays

    def get_employee_allocation_detail(self, start_date, end_date, employee):

        query = Q(Q(employee=employee) & Q(end_date__gte=start_date) & Q(start_date__lte=end_date))

        allocations = Allocation.objects.filter(query)

        bookings = []
        for allocation in allocations:
            for detail in AllocationDetail.objects.filter(allocation=allocation):
                b = self.Booking()
                b.allocation_id = allocation.id
                b.project = allocation.project.name
                b.allocation_type = allocation.allocation_type.name
                b.day_of_week = detail.day_of_week
                b.start_date = allocation.start_date
                b.end_date = allocation.end_date
                b.no_of_hours = allocation.no_of_hours
                b.color_code = allocation.allocation_type.color_code
                bookings.append(b)

        return bookings

    def get_blank_tds(self, start_date, end_date):
        delta = timedelta(days=1)
        tr = ''
        while start_date <= end_date:
            if self.is_weekend(start_date):
                tr += '<td class="weekend"></td>'
            elif self.is_bank_holiday(start_date):
                tr += '<td class="bank-holiday"></td>'
            else:
                tr += '<td class="un-allocated-td"></td>'

            start_date += delta
        return tr

    def get_employee_allocation_tr(self, start_date, end_date, allocation):
        delta = timedelta(days=1)
        timeline_tr = ''
        total_allocation_hours = 0
        total_hours_between_dates = 0

        allocation_detail = AllocationDetail.objects.filter(allocation=allocation)

        while start_date <= end_date:
            allocation_data = ''

            for detail in allocation_detail:
                if start_date.weekday() == detail.day_of_week and \
                        start_date >= allocation.start_date and \
                        start_date <= allocation.end_date:

                    class_name = ''
                    if self.is_bank_holiday(start_date):
                        class_name = 'bank-holiday'

                    allocation_data = '<td bgcolor="{}" class="allocation-td {}" onclick="allocation_edit({})" ></td>'\
                        .format(allocation.allocation_type.color_code, class_name, allocation.id)

                    total_allocation_hours += allocation.no_of_hours
                    break
                else:
                    if self.is_weekend(start_date):
                        allocation_data = '<td class="weekend"></td>'
                    elif self.is_bank_holiday(start_date):
                        allocation_data = '<td class="bank-holiday"></td>'
                    else:
                        allocation_data = '<td class="un-allocated-td"></td>'

            if not self.is_weekend(start_date):
                total_hours_between_dates += 8

            timeline_tr += allocation_data
            start_date += delta

        return timeline_tr

    def gettimelinecalendar(self):

        empty_tds = self.get_blank_tds(self.start_date, self.end_date)

        cal = '<table id="timeline-calendar-table" class="table">'

        cal += '<thead >'

        cal += '<tr scope="row">'
        # Creating space for Name, Job Title, Date Of Joining, Skills, Date, etc... columns
        # cal += '<th></th><th></th>'
        cal += '<th rowspan="2" style="vertical-align: middle; background: gray; color: white;" >{}</th>'\
            .format('Name')
        cal += '<th rowspan="2" style="vertical-align: middle;  background: gray; color: white;">{}</th>'\
            .format('Job Title')
        cal += self.get_week_header(self.start_date, self.end_date)
        cal += '</tr>'

        cal += '<tr >'
        cal += self.get_date_range_header(self.start_date, self.end_date)
        cal += '</tr>'

        cal += '</thead>'

        cal += '<tbody>'

        timeline_tr = ''
        row_span = 0

        days_difference = (self.end_date-self.start_date)
        row_span = days_difference.days + 3

        flex_squad = '<tr>'
        flex_squad += '<td class="project-detail" colspan="{}">{}</td>'.format(row_span, 'Flex Suad')
        flex_squad += '</tr>'
        # Fetch employees who are not allocated in selected time frame and add them in the Flex Squad project
        emps = [allocation.employee.id for allocation in Allocation.objects.filter(start_date__lte=self.end_date,
                                                                                   end_date__gte=self.start_date)]

        for emp in Employee.objects.all().exclude(id__in=emps):
            flex_squad += '<tr>'
            flex_squad += '<th style="white-space: nowrap;" >{}</th>'.format(emp.first_name)
            flex_squad += '<th style="white-space: nowrap;">{}</th>'.format(emp.job_title.name)
            flex_squad += empty_tds
            flex_squad += '</tr>'

        cal += flex_squad

        for project in Project.objects.filter(start_date__lte=self.end_date, end_date__gte=self.start_date)\
                .order_by('name'):
            timeline_tr = '<tr>'
            timeline_tr += '<td class="project-detail" colspan="{}">{}- Project Type:{}, Start date:{}, ' \
                           'End date:{}, Commercial Status: {}</td>'.format(
                            row_span, project.name, project.project_type.name,
                            project.start_date, project.end_date, project.commercial_status)

            timeline_tr += '</tr>'

            for allocation in Allocation.objects.filter(project=project, start_date__lte=self.end_date,
                                                        end_date__gte=self.start_date).order_by('employee__first_name'):
                timeline_tr += '<tr>'
                timeline_tr += "<th style='white-space: nowrap;' >{}</th>".format(allocation.employee.first_name)
                timeline_tr += "<th style='white-space: nowrap;'>{}</th>".format(allocation.employee.job_title.name)
                timeline_tr += self.get_employee_allocation_tr(self.start_date, self.end_date, allocation)
                timeline_tr += '</tr>'

            cal += timeline_tr

        cal += '</tbody>'
        cal += '</table>'

        return cal


    def capacitycalendar(self):

        cal = '<table id="capacity-calendar" class="table">'
        cal += '<thead>'

        cal += '<tr>'
        cal += '<th>{}</th>' \
            .format('Name')
        cal += '<th>{}</th>' \
            .format('Job Title')
        cal += '<th>{}</th>' \
            .format('Skills')
        cal += self.get_week_header_v2(self.get_week_commencing_date(self.start_date), self.get_week_commencing_date(self.end_date))
        cal += '</tr>'
        cal += '</thead>'

        cal += '<tbody>'

        delta = timedelta(days=1)
        start_date = self.get_week_commencing_date(self.start_date)
        end_date = self.get_week_commencing_date(self.end_date)

        for employee in Employee.objects.all():

            allocation_detail = self.get_employee_allocation_detail(self.get_week_commencing_date(self.start_date),
                                                                    self.get_week_commencing_date(self.end_date),
                                                                    employee)
            total_allocation_hours = 0
            employee_tr = '<tr>'
            employee_tr += '<td style="white-space: nowrap;">{}</td>'.format(employee.first_name)
            employee_tr += '<td style="white-space: nowrap;">{}</td>'.format(employee.job_title.name)
            employee_tr += '<td style="white-space: nowrap;">{}</td>'.format(','.join([s.name for s in employee.skills.all()]))

            start_date = self.get_week_commencing_date(self.start_date)
            end_date = self.get_week_commencing_date(self.end_date)
            current_week = self.start_date.strftime("%W")
            while start_date <= end_date:

                for detail in allocation_detail:
                    if start_date.weekday() == detail.day_of_week and \
                            start_date >= detail.start_date and \
                            start_date <= detail.end_date:

                        total_allocation_hours += detail.no_of_hours

                if start_date.strftime("%a") == 'Sun':
                    allocation_percentage = (total_allocation_hours / 40)

                    # progressbar = '<div class ="progress" style="height: 20px;">'
                    # progressbar += '<div class ="progress-bar"'
                    # progressbar += ' role="progressbar" aria-valuenow="{}" aria-valuemin="0" aria-valuemax="100"'.format(total_allocation_hours)
                    # progressbar += ' style="width: {:.0%}" >'.format(allocation_percentage)
                    # progressbar += '{:.0%}</div>'.format(allocation_percentage)
                    # progressbar += '</div>'

                    current_week = start_date.strftime("%W")

                    # employee_tr += "<td>{}</td>".format(progressbar)
                    employee_tr += "<td style=background:{};color:white;text-align:right>{} %</td>".format(self.get_heatmap_color(allocation_percentage*100), allocation_percentage*100)
                    total_allocation_hours = 0

                start_date += delta

            employee_tr += "</tr>"
            cal += employee_tr

        cal += '</tbody>'
        cal += '</table>'

        return cal

    @staticmethod
    def get_heatmap_color(value):
        heatmap_color = ''

        if value>=0 and value<=10:
            heatmap_color='#cc0000'
        elif value>=11 and value<=20:
            heatmap_color='#ff0000'
        elif value>=21 and value<=30:
            heatmap_color = '#ff6600'
        elif value>=31 and value<=40:
            heatmap_color = '#ff9900'
        elif value>=41 and value<=50:
            heatmap_color = '#ffc000'
        elif value>=51 and value<=60:
            heatmap_color = '#ffd966'
        elif value>=61 and value<=70:
            heatmap_color = '#ffe699'
        elif value>=71 and value<=80:
            heatmap_color = '#c6e0b4'
        elif value>=81 and value<=90:
            heatmap_color = '#a9d08e'
        elif value>=91 and value<=100:
            heatmap_color = '#339966'
        elif value>100:
            heatmap_color = '#1654b0'

        return heatmap_color
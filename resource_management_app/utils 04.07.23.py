from datetime import datetime, timedelta
from calendar import HTMLCalendar, calendar
from .models import Allocation, AllocationDetail, Employee
from django.db.models import Q

class TimeLineCalendar():

	class booking():
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

	def get_month_header(self, start_date, end_date):
		delta = timedelta(days=1)
		month_td = ''
		current_month = start_date.strftime("%B")
		month_col_span = 0

		while (start_date <= end_date):
			if current_month == start_date.strftime("%B"):
				month_col_span += 1
			else:
				month_td += '<th colspan="{}" scope="row" style="text-align: center;vertical-align: middle;">{}</th>'.format(month_col_span, current_month + "/" + start_date.strftime('%Y'))
				current_month = start_date.strftime("%B")
				month_col_span = 1

			start_date += delta


		# loop ends once look reache end_date hence not getting opporunity to add last month name. Due to that
		# added this manual entry in tail end of the loop
		month_td += '<th colspan="{}" scope="row" style="text-align: center;vertical-align: middle;">{}</th>'.format(
			month_col_span, current_month + "/" + start_date.strftime('%Y'))

		return month_td

	def get_date_range_header(self, start_date, end_date):
		delta = timedelta(days=1)
		date_td = ''

		while (start_date <= (end_date )):
			date_td += '<th scope="row" style="text-align: center;vertical-align: middle;">{}<br>{}</th>'.format(start_date.strftime("%d"), start_date.strftime("%a")[0])
			start_date += delta

		return date_td

	def is_weekend(self, date_to_check):
		if date_to_check.strftime("%a") == "Sat" or \
				date_to_check.strftime("%a") == "Sun":
			return True
		else:
			return False

	def is_bank_holiday(self, date_to_check):
		bank_holidays = self.get_bank_holidays()

		if date_to_check.strftime("%d-%m-%Y") in bank_holidays:
			return True
		else:
			return False
	def get_bank_holidays(self):
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

		# query = Q(Q(employee=employee) &
		# 		 Q(Q(start_date__gte=start_date) & Q(start_date__lte=end_date)))
		query = Q(Q(employee=employee) & Q(end_date__gte=start_date) & Q(start_date__lte=end_date))

		allocations = Allocation.objects.filter(query)

		bookings = []
		for allocation in allocations:
			for detail in AllocationDetail.objects.filter(allocation=allocation):
				b = self.booking()
				b.allocation_id = allocation.id
				b.project = allocation.project.name
				b.allocation_type = allocation.allocation_type.name
				b.day_of_week = detail.day_of_week
				b.start_date = datetime.combine(allocation.start_date, datetime.min.time())
				b.end_date = datetime.combine(allocation.end_date, datetime.min.time())
				b.no_of_hours = allocation.no_of_hours
				b.color_code = allocation.allocation_type.color_code
				bookings.append(b)

		return bookings

	def get_blank_tds(self, start_date, end_date):
		delta = timedelta(days=1)
		tr = ''
		while (start_date <= end_date):
			if self.is_weekend(start_date):
				tr += '<td class="weekend"></td>'
			elif self.is_bank_holiday(start_date):
				tr += '<td class="bank-holiday"></td>'
			else:
				tr += '<td ></td>'

			start_date += delta
		return tr

	def get_employee_allocation_by_project_tr(self, start_date, end_date, project, allocations):
		delta = timedelta(days=1)
		timeline_tr = ''
		allocation_data = ''
		total_allocation_hours = 0
		total_hours_between_dates = 0

		while (start_date <= end_date ):
			allocation_data = ''
			for allocation in allocations:
				if start_date.weekday() == allocation.day_of_week and \
						start_date>=allocation.start_date and \
						start_date <=allocation.end_date and \
						allocation.project == project:

					cell_color_code = allocation.color_code
					class_name = ''
					if self.is_bank_holiday(start_date):
						# cell_color_code = '#d917ec'
						class_name = 'bank-holiday'

					allocation_data = '<td bgcolor="{}" class="allocation-td {}" onclick="allocation_edit({})" ></td>'.format(allocation.color_code, class_name,
																						   allocation.allocation_id)

					total_allocation_hours += allocation.no_of_hours
					break
				else:
					if self.is_weekend(start_date):
						allocation_data = '<td class="weekend"></td>'
					elif self.is_bank_holiday(start_date):
						allocation_data = '<td class="bank-holiday"></td>'
					else:
						allocation_data = '<td ></td>'

			if not self.is_weekend(start_date):
				total_hours_between_dates += 8

			timeline_tr += allocation_data
			start_date += delta


		return timeline_tr, ((total_allocation_hours / total_hours_between_dates) * 100)

	def get_employee_allocation_timeline_tr(self, start_date, end_date, allocations):

		delta = timedelta(days=1)
		timeline_tr = ''
		allocation_data = ''
		total_allocation_hours = 0
		total_hours_between_dates = 0

		while (start_date <= end_date ):
			allocation_data = '<td></td>'
			for allocation in allocations:
				if start_date.weekday() == allocation.day_of_week and \
						start_date>=allocation.start_date and \
						start_date <=allocation.end_date:
					allocation_data = '<td bgcolor="{}">' \
									  '<a href="/allocation/update/{}">{}</a></td>'.format(allocation.color_code, allocation.allocation_id, allocation.project)
					total_allocation_hours += allocation.no_of_hours
					break
				else:
					if start_date.strftime("%a") == "Sat" or \
							start_date.strftime("%a") == "Sun":
						allocation_data = '<td bgcolor="#f1f1f1"></td>'
					else:
						allocation_data = '<td></td>'

			if not start_date.strftime("%a") == "Sat" and \
					not start_date.strftime("%a") == "Sun":
				total_hours_between_dates += 8

			if start_date.strftime("%a") == "Sat" or \
					start_date.strftime("%a") == "Sun":
				allocation_data = '<td bgcolor="#f1f1f1"></td>'

			timeline_tr += allocation_data
			start_date += delta

		return timeline_tr, ((total_allocation_hours / total_hours_between_dates) * 100)

	def get_employee_allocation_tr(self, start_date, end_date, employee):

		allocation_detail = self.get_employee_allocation_detail(start_date, end_date, employee)

		# Creating distanct project dictionary
		allocated_projects = {}
		for allocation in allocation_detail:
			if not allocation.project in allocated_projects:
				allocated_projects[allocation.project] = ''

		per_allocation = {}
		for project in allocated_projects:
			allocated_projects[project], per_allocation[project] = self.get_employee_allocation_by_project_tr(
				start_date, end_date, project, allocation_detail)

		timeline_tr = ''
		emp_id = employee.emp_id
		for key in allocated_projects:
			#timeline_tr = ''
			timeline_tr += '<tr>'


			timeline_tr += '<th class="text-nowrap" style="position: sticky; left: 0;" rowspan="{}">{}</th>'.format(row_span, employee.first_name)
			timeline_tr += '<th class="text-nowrap" rowspan="{}">{}</th>'.format(row_span,employee.job_title.name)

			timeline_tr += '<th class="text-nowrap" >{0:.2f}%</th>'.format(per_allocation[key])
			timeline_tr += '<th class="text-nowrap" >{}</th>{}'.format(key, allocated_projects[key])
			timeline_tr += '</tr>'

			row_span -=1

		return timeline_tr

	# def get_employee_allocation_tr(self, start_date, end_date, employee):
	#
	# 	allocation_detail = self.get_employee_allocation_detail(start_date, end_date, employee)
	#
	# 	allocation_tr, per_allocation = self.get_employee_allocation_timeline_tr(start_date, end_date, allocation_detail)
	#
	# 	timeline_tr = ''
	# 	timeline_tr += '<tr>'
	# 	timeline_tr += '<th class="text-nowrap" style="position: sticky; left: 0; ">{}</th>'.format(employee.first_name)
	# 	timeline_tr += '<th class="text-nowrap">{}</th>'.format(employee.job_title.name)
	# 	timeline_tr += '<th class="text-nowrap">{0:.2f}%</th>'.format(per_allocation)
	# 	timeline_tr += allocation_tr
	# 	timeline_tr += '</tr>'
	#
	#
	# 	return timeline_tr

	def gettimelinecalendar(self):

		employees_info_td = ''
		empty_tds = self.get_blank_tds(self.start_date, self.end_date)

		cal = '<table id="allocation_timeline" class="table">'

		cal += '<thead class="thead-dark">'

		cal += '<tr scope="row">'
		# Creating space for Name, Job Title, Date Of Joining, Skills, Date, etc... columns
		cal += '<th></th><th></th><th></th><th></th>'
		cal += self.get_month_header(self.start_date, self.end_date)
		cal += '</tr>'


		cal += '<tr scope="row">'
		cal += '<th scope="row" style="position: sticky; left: 0; ">{}</th>'.format('Name')
		cal += '<th scope="row">{}</th>'.format('Job Title')
		cal += '<th scope="row">{}</th>'.format('Allocation')
		cal += '<th scope="row">{}</th>'.format('Project')
		cal += self.get_date_range_header(self.start_date, self.end_date)
		cal += '</tr>'

		cal += '</thead>'

		cal += '<tbody>'

		for employee in Employee.objects.all():
			
			allocation_detail = self.get_employee_allocation_detail(self.start_date, self.end_date, employee)

			allocated_projects = {}
			for allocation in allocation_detail:
				if not allocation.project in allocated_projects:
					allocated_projects[allocation.project] = ''

			timeline_tr = ''
			employe_info_tds_created = False
			row_span = len(allocated_projects)
			for project in allocated_projects:

				timeline_tr += '<tr>'

				if not employe_info_tds_created:
					timeline_tr += '<th class="text-nowrap" style="position: sticky; left: 0; vertical-align: middle;" rowspan="{}">{}</th>'.format(
						row_span, employee.first_name)
					timeline_tr += '<th class="text-nowrap" style="vertical-align: middle;" rowspan="{}">{}</th>'.format(row_span, employee.job_title.name)
					employe_info_tds_created = True

				allocated_tds, allocation_percentage = self.get_employee_allocation_by_project_tr(
					self.start_date, self.end_date, project, allocation_detail)
				timeline_tr += '<th class="text-nowrap" >{0:.2f}%</th>'.format(allocation_percentage)
				timeline_tr += '<th class="text-nowrap" >{}</th>{}'.format(project, allocated_tds)

				timeline_tr += '</tr>'

			if len(allocated_projects) == 0:
				timeline_tr = '<tr>'
				timeline_tr += '<th class="text-nowrap" style="position: sticky; left: 0; vertical-align: middle;">{}</th>'.format(
					employee.first_name)
				timeline_tr += '<th class="text-nowrap" style="vertical-align: middle;" >{}</th>'.format(
					employee.job_title.name)
				timeline_tr += '<th class="text-nowrap" >{0:.2f}%</th>'.format(0)
				timeline_tr += '<th class="text-nowrap" >{}</th>{}'.format('N/A', empty_tds )

			cal += timeline_tr


		cal += '</tbody>'
		cal += '</table>'

		return cal

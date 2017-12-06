from django.db import models

class Subject(models.Model):
	#sub_id=models.AutoField()
	sub_code=models.IntegerField(primary_key=True)
	sub_name=models.CharField(max_length=200)
	semester_name=models.ForeignKey('Semester',on_delete=models.CASCADE,db_column='semester_name')

	def __str__(self):
		return str(self.sub_code)+'-'+self.sub_name

class Semester(models.Model):
	semester_name=models.CharField(max_length=200)

	def __str__(self):
		return str(self.semester_name)

class Subject_Scheme(models.Model):
	# subject=models.OneToOneField(
	# 		Subject,
	# 		on_delete=models.CASCADE,
	# 		primary_key=True,
	# 	)
	sub_code=models.ForeignKey('Subject',on_delete=models.CASCADE,db_column='sub_code')
	sub_load=models.IntegerField()
	sub_theory_class=models.IntegerField()
	sub_tutorial_class=models.IntegerField()
	sub_practical_class=models.IntegerField()

	def __str__(self):
		return self.sub_code+'-'+self.sub_name

# class Subject_Scheme(models.Model):
# 	sub_code=models.ForeignKey('Subject')
# 	sub_load=models.IntegerField()
# 	sub_theory_class=models.IntegerField()
# 	sub_tutorial_class=models.IntegerField()
# 	sub_practical_class=models.IntegerField()

# 	def __str__(self):
# 		return self.sub_code+'-'+self.sub_name

class Faculty(models.Model):
	faculty_id=models.AutoField(primary_key=True)
	faculty_name=models.CharField(max_length=200)
	position=models.IntegerField()
	work_load=models.IntegerField()

	def __str__(self):
		return self.faculty_id+'-'+self.faculty_name

class Faculty_subject(models.Model):
	faculty_id=models.ForeignKey('Faculty',on_delete=models.CASCADE)
	sub_code=models.ForeignKey('Subject',on_delete=models.CASCADE,db_column='sub_code')

	def __str__(self):
		return self.sub_code+'-'+self.faculty_id

class Days(models.Model):
	day_id=models.AutoField(primary_key=True)
	day_name=models.CharField(max_length=200)

	def __str__(self):
		return self.day_id+'-'+self.day_name

class Timeslot(models.Model):
	timeslot_id=models.AutoField(primary_key=True)
	timeslot=models.CharField(max_length=200)

	def __str__(self):
		return self.timeslot_id+'-'+self.timeslot

class Timeslot_day(models.Model):
	day_id=models.ForeignKey('Days',on_delete=models.CASCADE)
	timeslot_id=models.ForeignKey('Timeslot',on_delete=models.CASCADE)
	faculty_subject_table_id=models.ForeignKey('Faculty_subject',on_delete=models.CASCADE)
	semester=models.IntegerField()

	def __str__(self):
		return self.day_id+'-'+self.timeslot_id

class Timetable_master(models.Model):
	semester=models.IntegerField()
	timeslot_day_table_id=models.ForeignKey('Timeslot_day',on_delete=models.CASCADE)

	def __str__(self):
		return self.semester+'-'+self.timeslot_day_table_id

class Semester_day_table(models.Model):
	semester_name=models.ForeignKey('Semester',on_delete=models.CASCADE,db_column='semester_name')
	number_day=models.IntegerField()

	def __str__(self):
		return self.semester_name

class Semester_timeslot_table(models.Model):
	semester_name=models.ForeignKey('Semester',on_delete=models.CASCADE,db_column='semester_name')	
	number_timeslot=models.IntegerField()


	def __str__(self):
		return self.number_timeslot
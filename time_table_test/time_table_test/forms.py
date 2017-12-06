from django import forms
from .models import Subject,Faculty

class SubjectForm(forms.ModelForm):
	class Meta:
		model=Subject
		fields=['sub_code','sub_name','semester_name']

class FacultyForm(forms.ModelForm):
	class Meta:
		model=Faculty
		fields=['faculty_id','faculty_name','position','work_load']
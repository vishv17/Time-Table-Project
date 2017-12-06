from django.shortcuts import render,redirect
from .forms import SubjectForm,FacultyForm
from django.views import generic
from django.views.generic import View
from django import views
from . import time_table_models
from .models import Subject,Subject_Scheme,Faculty,Faculty_subject,Days,Timeslot,Timeslot_day,Timetable_master
from rest_framework import serializers
from time_table_models import TimeTableTestDays,TimeTableTestFaculty,TimeTableTestSubject,TimeTableTestFacultySubject,TimeTableTestSubjectScheme,TimeTableTestTimeslot,TimeTableTestTimeslotDay,TimeTableTestTimetableMaster,TimeTableTestSemester
import MySQLdb,json,operator
from playhouse.shortcuts import model_to_dict,dict_to_model
from collections import OrderedDict
from operator import itemgetter
from peewee import *
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt

class Subject(View):
	form=SubjectForm
	template_name='timetable/subject.html'

	def get(self,request):
		form=self.form(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form=self.form(request.POST)
		if form.is_valid():
			subject=form.save(commit=True)
			form=SubjectForm()
			return render(request,self.template_name,{'form':form})
		self.form=SubjectForm()
		return render(request,self.template_name,{'form':form})

class Faculty(View):
	form=FacultyForm
	template_name='timetable/Faculty.html'

	def get(self,request):
		form=self.form(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form=self.form(request.POST)
		if form.is_valid():
			faculty=form.save(commit=True)
			form=FacultyForm()
			return render(request,self.template_name,{'form':form})
		self.form=FacultyForm()
		return render(request,self.template_name,{'form':form})


def dashboard(request):
	# db=MySQLDatabase('time_table_test',user='root',password='',host='localhost')
	# db.connect()
	# count=TimeTableTestSemester.select().count()
	# if count>0:		
	return render(request, "timetable/dashboard.html",{'form':""})


def timetable(request):
	return render(request, "timetable/timetable.html",{'form':""})

@csrf_exempt
def add_semester(request):
	#if request.method=='POST':
		# print(request.body)
		# if 'application/json' in request.META['CONTENT_TYPE']:	
		# 	datas=json.loads((request.body).decode('utf-8'))
			#print(datas)
		# semester = request.POST['class_name'];
	info=json.loads((request.body).decode('utf-8'))
	semester=info['class_name']

	# return HttpResponse({'status':datas}, content_type="application/json")
	#json_encode=json.loads(request.body)
	#semester=json_encode['class_name']
	#request_status=3
	#semester=request.POST.get('class_name')
	db=MySQLDatabase('time_table_test',user='root',password='',host='localhost')
	db.connect()

	temp=TimeTableTestSemester.select().where(TimeTableTestSemester.semester_name==semester).count()
	if temp>0:
		return JsonResponse({'status':'unsuccess'})
	else:
		temp=TimeTableTestSemester(TimeTableTestSemester.semester_name==semester)
		temp.save()
		return JsonResponse({'status':'success'})
	# try:
	# 	with db.atomic():
	# 		obj=TimeTableTestSemester.get(TimeTableTestSemester.semester_name==semester)
	# 		return JsonResponse({'status':'unsuccess'})
	# except peewee.IntegrityError:
	# 	temp=TimeTableTestSemester.create(TimeTableTestSemester.semester_name=semester)
	# 	return JsonResponse({'status':'success'})
	#semester,temp=TimeTableTestSemester.get_or_create(semester_name=semester)
	#new_temp=temp.save()

	# if semester:
	# 	return JsonResponse({'status':'success'})
	# 	# return render(request, "timetable/dashboard.html",{'status':'success'})
	# 	#return HttpResponse({'status':'success'},content_type="application/json")
	# else:
	# 	return JsonResponse({'status':'unsuccess'})
		# return render(request, "timetable/dashboard.html",{'status':'unsuccess'})
		#return HttpResponse({'status':'unsuccess'}, content_type="application/json")
	# else:
	# 	return HttpResponse({'status':'0'}, content_type="application/json")


def before_timetable_subject(request):
	db=MySQLDatabase('time_table_test',user='root',password='',host='localhost')
	db.connect()
	temp_dict={}
	# var=TimeTableTestSubject.select(TimeTableTestSubject.semester).distinct()
	var=TimeTableTestSemester.select()
	list4=[]
	list3=[]
	#list1=[]
	#list2=[]
	for x in var:
		temp_dict2={}
		subjects=TimeTableTestSubject.select().where(TimeTableTestSubject.semester_name==x.semester_name)
		list1=[]
		list2=[]
		temp_dict={}
		for sub in subjects:
			fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub_code)
			for f in fac_sub:
				list1.append({'id':f.faculty_id.faculty,'postion':f.faculty_id.position,'name':str(f.faculty_id.faculty_name),'work_load':f.faculty_id.work_load})
			#print(list1)
			#list1=[int(x) for x in list1]
			#list1.sort(key=lambda tup:tup[1],reverse=True)
			# i=0
			# xtra=['id','position','name','work_load']
			# for l in list1:
			# 	temp_dict2[i]={
			# 			'id':l[0],
			# 			'position':l[1],
			# 			'name':l[2],
			# 			'work_load':l[3]
			# 		}
			# 	i=i+1
			# i=0
			#print(list1)
			sub_info=TimeTableTestSubjectScheme.select().where(TimeTableTestSubjectScheme.sub_code==sub.sub_code).get()
			
			list2.append({'name':sub.sub_name,'sub_load':sub_info.sub_load,'sub_code':sub.sub_code,'faculties':list1})
			
			# temp_dict[str(sub.sub_name)]={
			# 						'subject_load':int(str(sub_info.sub_load)),
			# 						'practical_load':int(str(sub_info.sub_practical_class)),
			# 						'theory_load':int(str(sub_info.sub_theory_class)),
			# 						'tutorial_load':int(str(sub_info.sub_tutorial_class)),
			# 						'faculty':list1
			# 							}
			#print(sub_info.sub_code.sub_name)
			#print(list1)
			list1=[]
		list3.append({'subjects':list2,'name':str(x.semester_name)})


		#list4.append(list3)
	if len(list3)>0:		
		temp_dict={'classes':list3}
	else:
		temp_dict={'classes':[]}
	return HttpResponse(json.dumps(temp_dict), content_type="application/json")


def timetable_generation(request):
	db=MySQLDatabase('time_table_test',user='root',password='',host='localhost')
	db.connect()
	days=TimeTableTestDays.select()
	time_slots=TimeTableTestTimeslot.select()
	subjects=TimeTableTestSubject.select().where(TimeTableTestSubject.semester_name==7)
	faculties=TimeTableTestFaculty.select()
	subject_count={}
	faculty_count={}
	timeslot_list=[]
	subject_list=[]
	for sub in subjects:
		subject_count[str(sub.sub_name)]=0
		subject_list.append(str(sub.sub_name))

	for fac in faculties:
		faculty_count[str(fac.faculty_name)]=0

	for t in time_slots:
		timeslot_list.append(int(t.timeslot_id))

	list1=[]
	temp_dict={}
	for sub in subjects:
		fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub_code)
		for f in fac_sub:
			list1.append((f.faculty_id.faculty,f.faculty_id.position,f.faculty_id.faculty_name,f.faculty_id.work_load))
		#print(list1)
		#list1=[int(x) for x in list1]
		list1.sort(key=lambda tup:tup[1],reverse=True)
		#print(list1)
		sub_info=TimeTableTestSubjectScheme.select().where(TimeTableTestSubjectScheme.sub_code==sub.sub_code).get()
		temp_dict[str(sub.sub_name)]={
								'subject_load':int(str(sub_info.sub_load)),
								'practical_load':int(str(sub_info.sub_practical_class)),
								'theory_load':int(str(sub_info.sub_theory_class)),
								'tutorial_load':int(str(sub_info.sub_tutorial_class)),
								'faculty':list1
									}
		#print(sub_info.sub_code.sub_name)
		#print(list1)
		list1=[]
	for sub in subjects:
		info=temp_dict[str(sub.sub_name)]
		faculties=info['faculty']
		new_temp_dict={}
		i=0
		for fac in faculties:
			new_temp_dict[i]={
				'id':fac[0],
				'position':fac[1],
				'name':fac[2],
				'work_load':fac[3]
			}
			i+=1
		info['faculty']=new_temp_dict


	days_dict={}
	temp_list=[]
	inner_flag=0
	testing=0
	if testing==0:
		for d in days:
			listx=[]
			# days_list=days_dict.keys()
			# last_day=days_list.pop()
			timeslot_dict={}
			subjects=TimeTableTestSubject.select()
			faculties=TimeTableTestFaculty.select()

			for sub in subjects:
				subject_count[str(sub.sub_name)]=0
				#subject_list.append(str(sub.sub_name))

			for fac in faculties:
				faculty_count[str(fac.faculty_name)]=0

			for x in timeslot_list:
				sub=random.choice(subject_list)
				if len(timeslot_dict)>0:
					timeslot_keys=timeslot_dict.keys()
					a=timeslot_keys.pop()
					previous_info=timeslot_dict[a]
					previous_subject=previous_info['subject']
					previous_faculty=previous_info['faculty']
					subject_counter=subject_count[sub]
					info=temp_dict[sub]
					subject_load=info['subject_load']
					if previous_subject==sub or subject_counter>1 or subject_load<=0:
						while previous_subject==sub or subject_counter>1 or subject_load<=0:
							sub=random.choice(subject_list)
							info=temp_dict[sub]
							subject_load=info['subject_load']
							subject_counter=subject_count[sub]

					info=temp_dict[sub]
					subject_load=info['subject_load']
					practical_load=info['practical_load']
					theory_load=info['theory_load']
					tutorial_load=info['tutorial_load']
					faculties=info['faculty']
					subject_counter=subject_count[sub]
					key_list=faculties.keys()
					for key in key_list:
						faculty_info=faculties[key]
						faculty_name=faculty_info['name']
						if faculty_name==previous_faculty:
							continue
						else:
							faculty_work_load=faculty_info['work_load']
							faculty_counter=faculty_count[faculty_name]
							if faculty_work_load>0 and faculty_counter<2:
								timeslot_dict[a+1]={'subject':sub,'faculty':faculty_name}
								faculty_work_load-=1
								faculty_counter+=1
								subject_load-=1
								subject_counter+=1
								theory_load-=1
								faculty_count[faculty_name]=faculty_counter
								subject_count[sub]=subject_counter
								faculties[key]={
									'id':faculty_info['id'],
									'position':faculty_info['position'],
									'name':faculty_name,
									'work_load':faculty_work_load
								}
								temp_dict[sub]={
								'subject_load':subject_load,
								'theory_load':theory_load,
								'tutorial_load':tutorial_load,
								'practical_load':practical_load,
								'faculty':faculties
								}
								break
					# listx.append(timeslot_dict)	

				else:	
					info=temp_dict[sub]
					subject_load=info['subject_load']
					practical_load=info['practical_load']
					theory_load=info['theory_load']
					tutorial_load=info['tutorial_load']
					faculties=info['faculty']
					subject_counter=subject_count[sub]
					key_list=faculties.keys()
					for key in key_list:
						faculty_info=faculties[key]
						faculty_work_load=faculty_info['work_load']
						faculty_name=faculty_info['name']
						faculty_counter=faculty_count[faculty_name]
						if faculty_work_load>0 and faculty_counter<2:
							timeslot_dict[x]={'subject':sub,'faculty':faculty_name}
							faculty_work_load-=1
							faculty_counter+=1
							subject_load-=1
							subject_counter+=1
							theory_load-=1
							faculty_count[faculty_name]=faculty_counter
							subject_count[sub]=subject_counter
							faculties[key]={
								'id':faculty_info['id'],
								'position':faculty_info['position'],
								'name':faculty_name,
								'work_load':faculty_work_load
							}
							temp_dict[sub]={
								'subject_load':subject_load,
								'theory_load':theory_load,
								'tutorial_load':tutorial_load,
								'practical_load':practical_load,
								'faculty':faculties
							}
							break
				listx.append(timeslot_dict)
			temp_list.append({'name':str(d.day_name),'slot':listx})
			# days_dict[str(d.day_name)]={'name':str(d.day_name),'slot':listx}				
		days_dict["days"]=temp_list				

	else:
		print("just testing")


	return HttpResponse(json.dumps(days_dict), content_type="application/json") 
# def timetable_subject(request,semester):

# 	db=MySQLDatabase('time_table_test',user='root',password='',host='localhost')
# 	db.connect()

# 	days=TimeTableTestDays.select()
# 	time_slots=TimeTableTestTimeslot.select()
# 	subjects=TimeTableTestSubject.select().where(TimeTableTestSubject.semester==semester)
# 	faculties=TimeTableTestFaculty.select()

# 	subject_count={}
# 	for sub in subjects:
# 		subject_count[str(sub.sub_name)]=0

# 	list1=[]
# 	temp_dict={}
# 	for sub in subjects:
# 		fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub)
# 		for f in fac_sub:
# 			list1.append((f.faculty_id.faculty,f.faculty_id.position,f.faculty_id.faculty_name,f.faculty_id.work_load))
# 		#print(list1)
# 		#list1=[int(x) for x in list1]
# 		list1.sort(key=lambda tup:tup[1],reverse=True)
# 		#print(list1)
# 		sub_info=TimeTableTestSubjectScheme.select().where(TimeTableTestSubjectScheme.sub_code==sub.sub).get()
# 		temp_dict[str(sub.sub_name)]={
# 								'subject_load':int(str(sub_info.sub_load)),
# 								'practical_load':int(str(sub_info.sub_practical_class)),
# 								'theory_load':int(str(sub_info.sub_theory_class)),
# 								'tutorial_load':int(str(sub_info.sub_tutorial_class)),
# 								'faculty':list1
# 									}
# 		#print(sub_info.sub_code.sub_name)
# 		#print(list1)
# 		list1=[]
# 		# print(temp_dict)
# 	#print(temp_dict)

# 		# fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub)
# 		# list1=[]
# 		# for f in fac_sub:
# 		# 	faculty_info=TimeTableTestFaculty.select().where(TimeTableTestFaculty.faculty==f.faculty_id).get()
# 		# 	list1.append(faculty_info.position)

# 	# for sub in subjects:
# 	# 	print(sub.sub_name)
# 	# 	fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub)
# 	# 	for s in fac_sub:
# 	# 		faculty_info=TimeTableTestFaculty.select().order_by(TimeTableTestFaculty.work_load.asc()).where(TimeTableTestFaculty.faculty==s.faculty_id)
# 	# 		for e in faculty_info:
# 	# 			print(e.faculty_name)
# 		# for f in faculty_info:
# 		# 	print(f.faculty_name)
# 	days_dict={}

# 	testing=0
# 	if testing==0:
# 		for d in days:
# 			timeslot_dict={}
			
# 			# subject=TimeTableTestSubject.select()

			
# 			# for k,v in subject_count.iteritems():
# 			# 	print(k,v)
# 			# # for subject in subjects:
# 			# 	print(subject_count[str(subject.sub_name)])
# 			for x in range(1,int(int(TimeTableTestTimeslot.select().count())+1)):
# 				#flag=True
# 				t=TimeTableTestTimeslot.get(TimeTableTestTimeslot.timeslot_id==x)
# 				sub=TimeTableTestSubject.select().order_by(fn.Rand()).limit(1).get()
# 				sub_scheme=TimeTableTestSubjectScheme.select().where(TimeTableTestSubjectScheme.sub_code==sub.sub).get()
# 					#print(sub_info.sub_name)
# 					# for k,v in available_fac.iteritems():
# 					# 	print(k,v)
# 					#faculty_info=TimeTableTestFaculty.select().order_by(TimeTableTestFaculty.position.desc()).having(TimeTableTestFaculty.faculty==f.faculty_id)
# 					# for e in faculty_info:
# 					# 	available_fac.append(e)
# 					# available_fac.reverse()
# 					# for temp_var in range(len(available_fac)):
# 					# 	e=available_fac[time_table_testmp_var]
# 					# 	#print(e.faculty_name)
# 					# available_fac={}
# 						#print(e.faculty_name)
				
					
# 				#faculty_info=TimeTableTestFaculty.select().where(TimeTableTestFaculty.faculty==fac_sub.faculty_id).get()
# 				# for i in fac_sub.TimeTableTestFacultytSubject_details:
# 				# 	print(i)
# 				#print(type(fac_sub))
# 				#print(fac_sub.faculty_id)
# 				#fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub).get()
# 				#print(fac_sub.sub_code)
# 				#faculty_info=TimeTableTestFaculty.select().where(TimeTableTestFaculty.faculty==fac_sub.faculty_id).get()
# 				# for f.faculty in fac_sub:
# 				# 	faculty_info=TimeTableTestFaculty.get(faculty==f.faculty_id)
# 				#print(d.day_name+":"+t.timeslot+":"+faculty_info.faculty_name+"\n")
# 				#print(faculty_info.faculty_name)
# 				#faculty_per_sub=TimeTableTestFaculty.select().where(TimeTableTestFaculty.faculty==(TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub_scheme.sub_code).get(TimeTableTestFacultySubject.faculty_id))).get()
# 				#print(sub_scheme.sub_load)
# 				if len(timeslot_dict)>1:
# 					#pass
# 					a=int(t.timeslot_id)-1
# 					previous_subject=timeslot_dict[a]['subject']
# 					count=subject_count[str(sub.sub_name)]
# 					load=temp_dict[str(sub.sub_name)]['subject_load']
# 					if previous_subject==sub.sub_name or sub_scheme.sub_load<=0 or count>2:
# 						while previous_subject==sub.sub_name or sub_scheme.sub_load<=0 or count>2:
# 							sub=TimeTableTestSubject.select().order_by(fn.Rand()).limit(1).get()

# 					info=temp_dict[str(sub.sub_name)]
# 					subject_load=info['subject_load']
# 					faculties=info['faculty']
# 					practical_load=info['practical_load']
# 					theory_load=info['theory_load']
# 					previous_faculty=timeslot_dict[a]['faculty']
# 					for faculty in faculties:
# 						work_load=int(faculty[3])
# 						faculty_name=str(faculty[2])
# 						if faculty_name!=previous_faculty and work_load>0:
# 							timeslot_dict[int(t.timeslot_id)]={'subject':sub.sub_name,'faculty':faculty_name}
# 							work_load=work_load-1
# 							subject_load=subject_load-1
# 							theory_load=theory_load-1
# 							subject_count[str(sub.sub_name)]=count+1
# 							list1=[]
# 							list1.append(faculty[0],faculty[1],faculty[2],work_load)
							
# 							break;							
# 							# sub_scheme=TimeTableTestSubjectScheme.select().where(TimeTableTestSubjectScheme.sub_code==sub.sub).get()
# 							# sub_info=TimeTableTestSubject.select().where(TimeTableTestSubject.sub==sub.sub).get()
# 							# fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub).get()
# 							# faculty_info=TimeTableTestFaculty.select().where(TimeTableTestFaculty.faculty==fac_sub.faculty_id).get()
# 					#print("current subject:"+sub.sub_name+"-"+"Previous Subject:"+previous_subject)
# 					#print(str(a)+":"+str(previous_subject))
# 					#print(previous_subject)
# 					# sub_scheme=TimeTableTestSubjectScheme.select().where(TimeTableTestSubjectScheme.sub_code==sub.sub).get()
# 					# sub_info=TimeTableTestSubject.select().where(TimeTableTestSubject.sub==sub.sub).get()
# 					# fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub)
# 					# #faculty_info=TimeTableTestFaculty.select().where(TimeTableTestFaculty.faculty==fac_sub.faculty_id).get()
# 					# for f in fac_sub:
# 					# 	#sub_info=TimeTableTestSubject.select().where(TimeTableTestSubject.sub==f.sub_code).get()
					
# 					# 	faculty_info=TimeTableTestFaculty.select(TimeTableTestFaculty.faculty,TimeTableTestFaculty.faculty_name,TimeTableTestFaculty.position,TimeTableTestFaculty.work_load).group_by(sub_info.sub_name).having(TimeTableTestFaculty.faculty==f.faculty_id).dicts()
# 					# # for f in faculty_info:
# 					# # 	print (sub_info.sub_name+":"+f['faculty_name'])
# 					#info=temp_dict[str(sub.sub_name)]
# 					#print(info)
# 				else:
# 					#previous_timeslot_faculty=timeslot_dict[a]['faculty']
# 					info=temp_dict[str(sub.sub_name)]
# 					subject_load=info['subject_load']
# 					faculties=info['faculty']
# 					practical_load=info['practical_load']
# 					theory_load=info['theory_load']
# 					count=subject_count[str(sub.sub_name)]
# 					for faculty in faculties:
# 						work_load=int(faculty[3])
# 						faculty_name=str(faculty[2])
# 						if work_load>0:
# 							timeslot_dict[int(t.timeslot_id)]={'subject':sub.sub_name,'faculty':faculty_name}
# 							work_load=work_load-1
# 							subject_load=subject_load-1
# 							theory_load=theory_load-1
# 							subject_count[str(sub.sub_name)]=count+1
# 							break;
# 			days_dict[str(d.day_name)]=timeslot_dict		

		


# 		for d in days:
# 			timeslot_value=days_dict[str(d.day_name)]
# 			print("\n"+str(d.day_name)+"\n")
# 			for t in time_slots:
# 				value=timeslot_value[int(t.timeslot_id)]
# 				print(str(value['subject'])+":"+str(value['faculty']))		



# 				# sub_scheme=TimeTableTestSubjectScheme.select().where(TimeTableTestSubjectScheme.sub_code==sub.sub).get()
# 				# sub_info=TimeTableTestSubject.select().where(TimeTableTestSubject.sub==sub.sub).get()
# 				# fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub)
# 				# 	#faculty_info=TimeTableTestFaculty.select().where(TimeTableTestFaculty.faculty==fac_sub.faculty_id).get()
# 				# for f in fac_sub:
# 				# 	#sub_info=TimeTableTestSubject.select().where(TimeTableTestSubject.sub==f.sub_code).get()
# 				# 	faculty_info=TimeTableTestFaculty.select(TimeTableTestFaculty.faculty,TimeTableTestFaculty.faculty_name,TimeTableTestFaculty.position,TimeTableTestFaculty.work_load).group_by(sub_info.sub_name).having(TimeTableTestFaculty.faculty==f.faculty_id).dicts()
# 				# 	temp_dict={}
# 				# 	new_list=[]
# 				# 	for fac in faculty_info:
# 				# 		new_list.append(fac['position'])

# 				# 	new_list.sort(reverse=True)
# 				# 	print(new_list)

# 				# 	for fac in faculty_info:
# 				# 		position=fac['position']
# 				# 		for i in new_list:
# 				# 			if i==position:
# 				# 				temp_dict[fac['faculty_name']]=fac['position']
# 				# 				break
# 				# sub_scheme=TimeTableTestSubjectScheme.select().where(TimeTableTestSubjectScheme.sub_code==sub.sub)
# 				# print(sub_scheme.sub_load)

# 					# for k,v in temp_dict.items():
# 					# 	print(k,v)
# 							#print(faculty_list)
# 							# for faculty in faculty_list:
# 		    				# 		print(faculty)
					
# 						#print(sub_info.sub_name+":"+f['faculty_name'])
# 				# sub_info=TimeTableTestSubject.select().where(TimeTableTestSubject.sub==sub.sub).get()
# 				# fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub).get()
# 				# faculty_info=TimeTableTestFaculty.select().group_by(sub_info.sub_name).having(TimeTableTestFaculty.faculty==fac_sub.faculty_id).dicts()
# 				#print(type(faculty_info))
# 				#sorted_faculty_info=OrderedDict(sorted(faculty_info.items(),key=itemgetter(2)))
# 				# print(sorted_faculty_info)
# 				#print(sorted_faculty_info)

				

				
# 				#print(faculty_info.faculty_name)
# 				# print(faculty_info)
# 				#timeslot_dict[t.timeslot_id]={'subject':sub_info.sub_name,'faculty':faculty_info[]}
				
# 				# a=int(sub_scheme.sub_load)
# 				# sub_scheme.sub_load=a-1
# 				# sub_scheme.save()
# 			#days_dict[d.day_name]=timeslot_dict



# 		# for d in days:
# 		# 	print("\n"+d.day_name)
# 		# 	time=days_dict[d.day_name]
# 		# 	for x in range(1,int(TimeTableTestTimeslot.select().count())):
# 		# 		t=TimeTableTestTimeslot.get(TimeTableTestTimeslot.timeslot_id==x)
# 		# 		value=time[t.timeslot_id]
# 		# 		print(str(t.timeslot)+":"+str(value['subject'])+":"+str(value['faculty'])+"\n")
# 	else:
# 		print("just testing")
# 		# for d in days:
# 		# 	print("\n"+d.day_name)
# 		# 	time=days_dict[str(d.day_name)]
# 		# 	for x in range(1,int(TimeTableTestTimeslot.select().count())):
# 		# 		t=TimeTableTestTimeslot.get(TimeTableTestTimeslot.timeslot_id==x)
# 		# 		value=time[t.timeslot_id]
# 		# 		print(str(t.timeslot)+":"+str(value['subject'])+":"+str(value['faculty'])+"\n")

# 		# sub=TimeTableTestSubject.select().order_by(fn.Rand()).limit(1).get()
# 		# sub_scheme=TimeTableTestSubjectScheme.select().where(TimeTableTestSubjectScheme.sub_code==sub.sub).get()
# 		# fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub)
# 		# available_fac={}
# 		# temp_dict={}
# 		# new_list=[]
# 		# list1=[]
# 		# for f in fac_sub:
# 		# 	faculty_info=TimeTableTestFaculty.select().where(TimeTableTestFaculty.faculty==f.faculty_id).get()
# 		# 	list1.append(faculty_info.faculty_name)

# 		# temp_dict[str(sub.sub_name)]=list1
# 		# print(temp_dict[str(sub.sub_name)])




# 	# faculty_subject={}
# 	# for sub in subjects:
# 	# 	fac_sub=TimeTableTestFacultySubject.select().where(TimeTableTestFacultySubject.sub_code==sub.sub).dicts().get()
# 	# 	faculty_subject[sub.sub_name]=fac_sub
# 	# print len(faculty_subject)

# 	# for sub in subjects:
# 	# 	print (faculty_subject[sub.sub_name])
# 	#faculty_subject=TimeTableTestFaculty.select().dicts().get()
# 	#for random number-TimeTableTestDays.select().order_by(fn.Rand())

# 		# subjects=Subject.objects.all()
# 		# context={
# 		# 	'subject':subjects,
# 		# }
# 		# return render(request,'time_table_test/index.html',context)
class Timetable(View):
	def get(self,request):
		subjects=Subject.objects.all()	

		workload_sub={}
		subject_faculty={}
		day_list=[]
		subjects=Subject.objects.all()
		faculty=Faculty.objects.all()
		day=Days.objects.all()
		time_slot=Timeslot.objects.all()
		for d in day:
			day_list.append(d.day_name)

# 		# 	for sub in subjects:
# 		# 		faculty_list=[]
# 		# 		available_faculty=Faculty.objects.filter(sub_code_id=sub.sub_id)

# 	return render(request,'time_table_test',days_dict)	
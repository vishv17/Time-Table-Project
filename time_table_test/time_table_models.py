from peewee import *

database = MySQLDatabase('time_table_test', **{'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class AuthGroup(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'auth_group'

class DjangoContentType(BaseModel):
    app_label = CharField()
    model = CharField()

    class Meta:
        db_table = 'django_content_type'
        indexes = (
            (('app_label', 'model'), True),
        )

class AuthPermission(BaseModel):
    codename = CharField()
    content_type = ForeignKeyField(db_column='content_type_id', rel_model=DjangoContentType, to_field='id')
    name = CharField()

    class Meta:
        db_table = 'auth_permission'
        indexes = (
            (('content_type', 'codename'), True),
        )

class AuthGroupPermissions(BaseModel):
    group = ForeignKeyField(db_column='group_id', rel_model=AuthGroup, to_field='id')
    permission = ForeignKeyField(db_column='permission_id', rel_model=AuthPermission, to_field='id')

    class Meta:
        db_table = 'auth_group_permissions'
        indexes = (
            (('group', 'permission'), True),
        )

class AuthUser(BaseModel):
    date_joined = DateTimeField()
    email = CharField()
    first_name = CharField()
    is_active = IntegerField()
    is_staff = IntegerField()
    is_superuser = IntegerField()
    last_login = DateTimeField(null=True)
    last_name = CharField()
    password = CharField()
    username = CharField(unique=True)

    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(BaseModel):
    group = ForeignKeyField(db_column='group_id', rel_model=AuthGroup, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'auth_user_groups'
        indexes = (
            (('user', 'group'), True),
        )

class AuthUserUserPermissions(BaseModel):
    permission = ForeignKeyField(db_column='permission_id', rel_model=AuthPermission, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'auth_user_user_permissions'
        indexes = (
            (('user', 'permission'), True),
        )

class DjangoAdminLog(BaseModel):
    action_flag = IntegerField()
    action_time = DateTimeField()
    change_message = TextField()
    content_type = ForeignKeyField(db_column='content_type_id', null=True, rel_model=DjangoContentType, to_field='id')
    object = TextField(db_column='object_id', null=True)
    object_repr = CharField()
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'django_admin_log'

class DjangoMigrations(BaseModel):
    app = CharField()
    applied = DateTimeField()
    name = CharField()

    class Meta:
        db_table = 'django_migrations'

class DjangoSession(BaseModel):
    expire_date = DateTimeField(index=True)
    session_data = TextField()
    session_key = CharField(primary_key=True)

    class Meta:
        db_table = 'django_session'

class TimeTableTestDays(BaseModel):
    day = PrimaryKeyField(db_column='day_id')
    day_name = CharField()

    class Meta:
        db_table = 'time_table_test_days'

class TimeTableTestFaculty(BaseModel):
    faculty = PrimaryKeyField(db_column='faculty_id')
    faculty_name = CharField()
    position = IntegerField()
    work_load = IntegerField()

    class Meta:
        db_table = 'time_table_test_faculty'

class TimeTableTestSemester(BaseModel):
    semester_name = CharField()

    class Meta:
        db_table = 'time_table_test_semester'

class TimeTableTestSubject(BaseModel):
    semester_name = ForeignKeyField(db_column='semester_name', rel_model=TimeTableTestSemester, to_field='id')
    sub_code = PrimaryKeyField()
    sub_name = CharField()

    class Meta:
        db_table = 'time_table_test_subject'

class TimeTableTestFacultySubject(BaseModel):
    faculty_id = ForeignKeyField(db_column='faculty_id_id', rel_model=TimeTableTestFaculty, to_field='faculty')
    sub_code = ForeignKeyField(db_column='sub_code', rel_model=TimeTableTestSubject, to_field='sub_code')

    class Meta:
        db_table = 'time_table_test_faculty_subject'

class TimeTableTestSemesterDayTable(BaseModel):
    number_day = IntegerField()
    semester_name = ForeignKeyField(db_column='semester_name', rel_model=TimeTableTestSemester, to_field='id')

    class Meta:
        db_table = 'time_table_test_semester_day_table'

class TimeTableTestSemesterTimeslotTable(BaseModel):
    number_timeslot = IntegerField()
    semester_name = ForeignKeyField(db_column='semester_name', rel_model=TimeTableTestSemester, to_field='id')

    class Meta:
        db_table = 'time_table_test_semester_timeslot_table'

class TimeTableTestSubjectScheme(BaseModel):
    sub_code = ForeignKeyField(db_column='sub_code', rel_model=TimeTableTestSubject, to_field='sub_code')
    sub_load = IntegerField()
    sub_practical_class = IntegerField()
    sub_theory_class = IntegerField()
    sub_tutorial_class = IntegerField()

    class Meta:
        db_table = 'time_table_test_subject_scheme'

class TimeTableTestTimeslot(BaseModel):
    timeslot = CharField()
    timeslot_id = PrimaryKeyField()

    class Meta:
        db_table = 'time_table_test_timeslot'

class TimeTableTestTimeslotDay(BaseModel):
    day_id = ForeignKeyField(db_column='day_id_id', rel_model=TimeTableTestDays, to_field='day')
    faculty_subject_table_id = ForeignKeyField(db_column='faculty_subject_table_id_id', rel_model=TimeTableTestFacultySubject, to_field='id')
    semester = IntegerField()
    timeslot_id = ForeignKeyField(db_column='timeslot_id_id', rel_model=TimeTableTestTimeslot, to_field='timeslot_id')

    class Meta:
        db_table = 'time_table_test_timeslot_day'

class TimeTableTestTimetableMaster(BaseModel):
    semester = IntegerField()
    timeslot_day_table_id = ForeignKeyField(db_column='timeslot_day_table_id_id', rel_model=TimeTableTestTimeslotDay, to_field='id')

    class Meta:
        db_table = 'time_table_test_timetable_master'


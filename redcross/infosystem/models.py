# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DonateMoney(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=12)  # Field name made lowercase.
    org_name = models.CharField(db_column='Org_Name', max_length=100)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=20)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    quantity = models.DecimalField(db_column='Quantity', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    receipt_id = models.CharField(db_column='Receipt_ID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    intention = models.CharField(db_column='Intention', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'donate_money'


class DonateResources(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=12)  # Field name made lowercase.
    org_name = models.CharField(db_column='Org_Name', max_length=100)  # Field name made lowercase.
    res_name = models.CharField(db_column='Res_Name', max_length=100)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=20)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    quantity = models.DecimalField(db_column='Quantity', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    receipt_id = models.CharField(db_column='Receipt_ID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    intention = models.CharField(db_column='Intention', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'donate_resources'


class InfosystemUserinfo(models.Model):
    name = models.CharField(max_length=20)
    bday = models.DateField()
    checked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'infosystem_userinfo'


class ReceiveMoney(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=12)  # Field name made lowercase.
    rec_name = models.CharField(db_column='Rec_Name', max_length=100)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=20)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    quantity = models.DecimalField(db_column='Quantity', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'receive_money'


class ReceiveResources(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=12)  # Field name made lowercase.
    rec_name = models.CharField(db_column='Rec_Name', max_length=100)  # Field name made lowercase.
    res_name = models.CharField(db_column='Res_Name', max_length=100)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=20)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    quantity = models.DecimalField(db_column='Quantity', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'receive_resources'


class Receiver(models.Model):
    rec_name = models.CharField(db_column='Rec_Name', primary_key=True, max_length=100)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'receiver'
        unique_together = (('rec_name', 'province'),)


'''
class Category(models.Model):
    autoid = models.AutoField(primary_key=True)
    email=models.CharField(max_length=150,blank=False)
    comtype=models.CharField(max_length=20,blank=False)
    catname=models.CharField(max_length=150,blank=False) 
      
    def __unicode__(self):
        return '%s' % (self.catname)
      
    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

'''
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib import messages

from .models import Script_Backup

from .models import A1,A2,Ar1,Ar2,At1,At2

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError

from django.http import HttpResponseRedirect

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from simple_history.admin import SimpleHistoryAdmin
import sys

#################################################### Redirect link #################################################

def redirect_to_config(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			if obj.Gateway == 'A1':
				return HttpResponseRedirect("/admin/script_backup/a1/?q=%s" % (obj.Gateway + " " + obj.IP + " " + obj.Model))
			if obj.Gateway == 'A2':
				return HttpResponseRedirect("/admin/script_backup/a2/?q=%s" % (obj.Gateway + " " + obj.IP + " " + obj.Model))
			if obj.Gateway == 'Ar1':
				return HttpResponseRedirect("/admin/script_backup/ar1/?q=%s" % (obj.Gateway + " " + obj.IP + " " + obj.Model))
			if obj.Gateway == 'Ar2':
				return HttpResponseRedirect("/admin/script_backup/ar2/?q=%s" % (obj.Gateway + " " + obj.IP + " " + obj.Model))
			if obj.Gateway == 'At1':
				return HttpResponseRedirect("/admin/script_backup/at1/?q=%s" % (obj.Gateway + " " + obj.IP + " " + obj.Model))
			if obj.Gateway == 'At2':
				return HttpResponseRedirect("/admin/script_backup/at2/?q=%s" % (obj.Gateway + " " + obj.IP + " " + obj.Model))							
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

redirect_to_config.short_description = 'Redirect to mode config'


#################################################### Config Juniper ################################################# Done

def config_bandwidth(gateway,file):

	dev = Device( host= gateway, user='ws.backup', password='netn@m@2016').open()
	dev.timeout = 120
	cfg = Config(dev)
	cfg.lock()
	cfg.load( path=file, format="set", merge=True)
	cfg.commit()
	cfg.unlock()
	dev.close()

###########################################################################################################
############################################# Load Config  ################################################

def Load_Activate(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			if obj.Model == 'Static-Ring':
				config_bandwidth(obj.IP,'Static_Active.txt')
			modeladmin.message_user(request, ("Successfully Updated."))
			if obj.Model == 'VirPOP-Static':
				config_bandwidth(obj.IP,'RMPop_Static_Active.txt')
			modeladmin.message_user(request, ("Successfully Updated."))
			if obj.Model == 'Special':
				config_bandwidth(obj.IP,'Static_Special_Active.txt')
			modeladmin.message_user(request, ("Successfully Updated."))
			if obj.Model == 'Transit-TN':
				config_bandwidth(obj.IP,'TransitTN_Active.txt')
			modeladmin.message_user(request, ("Successfully Updated."))
			if obj.Model == 'Transit-QT':
				config_bandwidth(obj.IP,'TransitQT_Active.txt')
			modeladmin.message_user(request, ("Successfully Updated."))
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

Load_Activate.short_description = 'Load activate file'

def Load_Deactivate(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			if obj.Model == 'Static-Ring':
				config_bandwidth(obj.IP,'Static_Backup.txt')
			modeladmin.message_user(request, ("Successfully Updated."))
			if obj.Model == 'VirPOP-Static':
				config_bandwidth(obj.IP,'RMPop_Static_Backup.txt')
			modeladmin.message_user(request, ("Successfully Updated."))
			if obj.Model == 'Special':
				config_bandwidth(obj.IP,'Static_Special_Backup.txt')
			modeladmin.message_user(request, ("Successfully Updated."))
			if obj.Model == 'Transit-TN':
				config_bandwidth(obj.IP,'TransitTN_Backup.txt')
			modeladmin.message_user(request, ("Successfully Updated."))
			if obj.Model == 'Transit-QT':
				config_bandwidth(obj.IP,'TransitQT_Backup.txt')
			modeladmin.message_user(request, ("Successfully Updated."))
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

Load_Deactivate.short_description = 'Load deactivate file'


#####################################################################################################################

class Script_BackupResource(resources.ModelResource):
	class Meta:
		model = Script_Backup
		fields = ('Gateway', 'IP', 'Via','File','Model')

class Script_Backup_Admin(SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):

	def file(self,obj):
		return  '<br>'.join((obj.File).split())
	file.allow_tags = True
	file.short_description = 'File'

	def get_actions(self, request):
		actions = super(Script_Backup_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	fieldsets = [
	
		('', {'fields': ['Gateway']}),
		('', {'fields': ['IP']}),
		('', {'fields': ['Via']}),
		('', {'fields': ['File']}),
		('', {'fields': ['Model']}),
	]

	resource_class = Script_BackupResource

	search_fields = ('Gateway','IP','Model','Via','File',)

	list_filter = ['Gateway','Via']

	list_display = ('Gateway','IP','Model','Via','file')

	history_list_display = ['Name','Gateway','Model','IP','Via','file']

	list_per_page = 30

	actions = [ redirect_to_config,  ]

admin.site.register(Script_Backup,Script_Backup_Admin) 

###########################################################################################################
#################################################### A1 ################################################### Done

class A1_Admin(admin.ModelAdmin):

	def file(self,obj):
		return  '<br>'.join((obj.File).split())
	file.allow_tags = True
	file.short_description = 'File'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(A1_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Gateway','IP','Model','Via','File',)
		
	list_display = ('Gateway','IP','Model','Via','file')

	list_display_links = None

	list_per_page = 10

	actions = [ Load_Activate, Load_Deactivate ]

admin.site.register(A1,A1_Admin)

###########################################################################################################
#################################################### A2 ################################################### Done

class A2_Admin(admin.ModelAdmin):

	def file(self,obj):
		return  '<br>'.join((obj.File).split())
	file.allow_tags = True
	file.short_description = 'File'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(A2_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Gateway','IP','Model','Via','File',)
		
	list_display = ('Gateway','IP','Model','Via','file')

	list_display_links = None

	list_per_page = 10

	actions = [ Load_Activate, Load_Deactivate ]

admin.site.register(A2,A2_Admin)

###########################################################################################################
#################################################### Ar1 ##################################################

class Ar1_Admin(admin.ModelAdmin):

	def file(self,obj):
		return  '<br>'.join((obj.File).split())
	file.allow_tags = True
	file.short_description = 'File'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(Ar1_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Gateway','IP','Model','Via','File',)
		
	list_display = ('Gateway','IP','Model','Via','file')

	list_display_links = None

	list_per_page = 10

	actions = [ Load_Activate, Load_Deactivate ]

admin.site.register(Ar1,Ar1_Admin)

###########################################################################################################
#################################################### Ar2 ##################################################

class Ar2_Admin(admin.ModelAdmin):

	def file(self,obj):
		return  '<br>'.join((obj.File).split())
	file.allow_tags = True
	file.short_description = 'File'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(Ar2_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Gateway','IP','Model','Via','File',)
		
	list_display = ('Gateway','IP','Model','Via','file')

	list_display_links = None

	list_per_page = 10

	actions = [ Load_Activate, Load_Deactivate ]

admin.site.register(Ar2,Ar2_Admin)

###########################################################################################################
#################################################### At1 ##################################################

class At1_Admin(admin.ModelAdmin):

	def file(self,obj):
		return  '<br>'.join((obj.File).split())
	file.allow_tags = True
	file.short_description = 'File'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(At1_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Gateway','IP','Model','Via','File',)
		
	list_display = ('Gateway','IP','Model','Via','file')

	list_display_links = None

	list_per_page = 10

	actions = [ Load_Activate, Load_Deactivate ]

admin.site.register(At1,At1_Admin)

###########################################################################################################
#################################################### At2 ##################################################

class At2_Admin(admin.ModelAdmin):

	def file(self,obj):
		return  '<br>'.join((obj.File).split())
	file.allow_tags = True
	file.short_description = 'File'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(At2_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Gateway','IP','Model','Via','File',)
		
	list_display = ('Gateway','IP','Model','Via','file')

	list_display_links = None

	list_per_page = 10

	actions = [ Load_Activate, Load_Deactivate ]

admin.site.register(At2,At2_Admin)
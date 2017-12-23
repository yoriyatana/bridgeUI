# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys,shutil
from django.db import models
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect


from .models import Bandwidth
from .models import Static_Ring, Static_ISPOther, Gre_Server, VirPOP_Static
from .models import VirPOP_BGP_Static, DynamicBackup_ISPOther_GRE, DynamicBackup_ISPOther_VirPOP
from .models import DynamicBackup_Ring_Ring, DynamicBackup_SW_EXT_Ring, DynamicBackup_SW_EXT_VirPop
from .models import Special, Transit

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from simple_history.admin import SimpleHistoryAdmin

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.auth.models import User

#################################################### Redirect link ################################################# Done

GATEWAY_DICT = {"A1" : "10.1.1.11", "A2": "10.1.1.12", "Ar1": "10.1.1.23", "Ar2": "10.1.1.24", "At1": "10.1.1.13", "At2": "10.1.1.14"}
INVERTED_GATEWAY_DICT = {v: k for k, v in GATEWAY_DICT.items()}
action_names = { ADDITION: 'Addition', CHANGE: 'Change', DELETION: 'Deletion', }

DST = '/root/bridge/bandwidth/'

#################################################### Redirect link ################################################# Done

def redirect_to_config(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			if obj.Model == 'Static-Ring':
				return HttpResponseRedirect("/admin/bandwidth/static_ring/?q=%s" % (obj.Name))
			if obj.Model == 'Static-ISPOther':
				return HttpResponseRedirect("/admin/bandwidth/static_ispother/?q=%s" % (obj.Name))
			if obj.Model == 'Gre-Server':
				return HttpResponseRedirect("/admin/bandwidth/gre_server/?q=%s" % (obj.Name))
			if obj.Model == 'VirPOP-Static':
				return HttpResponseRedirect("/admin/bandwidth/virpop_static/?q=%s" % (obj.Name))
			if obj.Model == 'VirPOP-BGP-Static':
				return HttpResponseRedirect("/admin/bandwidth/virpop_bgp_static/?q=%s" % (obj.Name))
			if obj.Model == 'DynamicBackup-ISPOther-GRE':
				return HttpResponseRedirect("/admin/bandwidth/dynamicbackup_ispother_gre/?q=%s" % (obj.Name))
			if obj.Model == 'DynamicBackup-ISPOther-VirPOP':
				return HttpResponseRedirect("/admin/bandwidth/dynamicbackup_ispother_virpop/?q=%s" % (obj.Name))
			if obj.Model == 'DynamicBackup-Ring-Ring':
				return HttpResponseRedirect("/admin/bandwidth/dynamicbackup_ring_ring/?q=%s" % (obj.Name))
			if obj.Model == 'DynamicBackup-SW-EXT-Ring':
				return HttpResponseRedirect("/admin/bandwidth/dynamicbackup_sw_ext_ring/?q=%s" % (obj.Name))
			if obj.Model == 'DynamicBackup-SW-EXT-VirPop':
				return HttpResponseRedirect("/admin/bandwidth/dynamicbackup_sw_ext_virpop/?q=%s" % (obj.Name))
			if obj.Model == 'Special':
				return HttpResponseRedirect("/admin/bandwidth/special/?q=%s" % (obj.Name))
			if obj.Model == 'Transit':
				return HttpResponseRedirect("/admin/bandwidth/transit/?q=%s" % (obj.Name))
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

redirect_to_config.short_description = 'Redirect to mode config'

#####################################################################################################################
#################################################### Edit link ###################################################### Done

def Edit_Customer(modeladmin, request, queryset):
	if queryset.count() == 1:
		for obj in queryset:
			return HttpResponseRedirect("/admin/bandwidth/bandwidth/%s" % (obj.id))			
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

Edit_Customer.short_description = 'Go to edit'

##################################################################################################################### 
#################################################### Config Juniper ################################################# Done

def Config_Bandwidth(gateway,modeladmin,request,Name):

		try:
			dev = Device( host= gateway, user='ws.backup', password='netn@m@2016')
			dev.open()
			#dev.timeout = 120
		except ConnectError as err:
			modeladmin.message_user(request, ("Cannot connect to device: {0}".format(err)),level=messages.ERROR)
			return

		dev.bind(cu=Config)

		# Lock the configuration
		try:
			dev.cu.lock()
		except LockError as err:
			modeladmin.message_user(request, ("Unable to lock configuration: {0}".format(err)),level=messages.ERROR)
			dev.close()
			return

		#Loading configuration changes
		try:
			dev.cu.load(path="bandwidth.txt", format="set", merge=True)
		except (ConfigLoadError, Exception) as err:
			modeladmin.message_user(request, ("Unable to load configuration changes: {0}".format(err)),level=messages.ERROR)
			try:
				dev.cu.unlock()
			except UnlockError:
				modeladmin.message_user(request,("Unable to unlock configuration: {0}".format(err)),level=messages.ERROR)
			dev.close()
			return

		#Committing the configuration
		try:
			dev.cu.commit(comment='Loaded by WebUI.')
		except CommitError as err:
			modeladmin.message_user(request,("Unable to commit configuration: {0}".format(err)),level=messages.ERROR)
			try:
				dev.cu.unlock()
			except UnlockError as err:
				modeladmin.message_user(request,("Unable to unlock configuration: {0}".format(err)),level=messages.ERROR)
			dev.close()
			return

		try:
			dev.cu.unlock()
			modeladmin.message_user(request, ("%s has been updated to %s successfully ." % (Name,INVERTED_GATEWAY_DICT[gateway])))
		except UnlockError as err:
			modeladmin.message_user(request,("Unable to unlock configuration: {0}".format(err)),level=messages.ERROR)

		# End the NETCONF session and close the connection
		dev.close()
		
##################################################################################################################### 
######################################################## Policer #################################################### Done

def Policer(Gateway,IXP,NIX):
	print ("set logical-systems %s firewall policer %sM if-exceeding bandwidth-limit %sm burst-size-limit %sk" % (Gateway,IXP,IXP,IXP*3750/100))	
	print ("set logical-systems %s firewall policer %sM then discard" %(Gateway,IXP))
	print ("set logical-systems %s firewall policer %sM if-exceeding bandwidth-limit %sm burst-size-limit %sk" % (Gateway,NIX,NIX,NIX*3750/100))	
	print ("set logical-systems %s firewall policer %sM then discard" %(Gateway,NIX))


#####################################################################################################################
#################################################### Static-Ring #################################################### Done

def Config_Static_Ring(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-ixp term up_ixp_%s then policer %sM" % (Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_ixp_%s then policer %sM" %(Gateway,VLAN,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.up-nix term up_nix_%s then policer %sM" % (Gateway,Cus_ID,NIX));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_nix_%s then policer %sM" %(Gateway,VLAN,Cus_ID,NIX));

def A1_Static_Ring(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A1',int(obj.IXP),int(obj.NIX))
			Config_Static_Ring("A1",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_Static_Ring.short_description = 'Apply to A1'

def A2_Static_Ring(modeladmin, request,queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A2',int(obj.IXP),int(obj.NIX))
			Config_Static_Ring("A2",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A2'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A2_Static_Ring.short_description = 'Apply to A2'

class Static_Ring_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(Static_Ring_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_Static_Ring, A2_Static_Ring  ]

admin.site.register(Static_Ring,Static_Ring_Admin)

########################################################################################################################
#################################################### Static-ISPOther ################################################### Done

def Config_Static_ISPOther(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-ixp term up_ixp_%s then policer %sM" % (Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.down-ISPOther term down_ixp_%s then policer %sM" %(Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.up-nix term up_nix_%s then policer %sM" % (Gateway,Cus_ID,NIX));
	print ("set logical-systems %s firewall family inet filter f.down-ISPOther term down_nix_%s then policer %sM" %(Gateway,Cus_ID,NIX));

def A1_Static_ISPOther(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			if obj.Model == 'Static-ISPOther':
				Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
				temp = sys.stdout
				sys.stdout = open("bandwidth.txt","w")
				Policer('A1',int(obj.IXP),int(obj.NIX))
				Config_Static_ISPOther("A1",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
				sys.stdout.close()
				sys.stdout = temp
				Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_Static_ISPOther.short_description = 'Apply to A1'

class Static_ISPOther_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(Static_ISPOther_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_Static_ISPOther  ]

admin.site.register(Static_ISPOther,Static_ISPOther_Admin)

####################################################################################################################
#################################################### Gre-Server #################################################### Done

def Config_Gre_Server(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-ixp term up_ixp_%s then policer %sM" % (Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.down-GRE term down_ixp_%s then policer %sM" %(Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.up-nix term up_nix_%s then policer %sM" % (Gateway,Cus_ID,NIX));
	print ("set logical-systems %s firewall family inet filter f.down-GRE term down_nix_%s then policer %sM" %(Gateway,Cus_ID,NIX));

def A1_Gre_Server(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			if obj.Model == 'Gre-Server':
				Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
				temp = sys.stdout
				sys.stdout = open("bandwidth.txt","w")
				Policer('A1',int(obj.IXP),int(obj.NIX))
				Config_Gre_Server("A1",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
				sys.stdout.close()
				sys.stdout = temp
				Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_Gre_Server.short_description = 'Apply to A1'

def A2_Gre_Server(modeladmin, request,queryset):

	if queryset.count() == 1:
		for obj in queryset:
			if obj.Model == 'Gre-Server':
				Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
				temp = sys.stdout
				sys.stdout = open("bandwidth.txt","w")
				Policer('A2',int(obj.IXP),int(obj.NIX))
				Config_Gre_Server("A2",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
				sys.stdout.close()
				sys.stdout = temp
				Config_Bandwidth(GATEWAY_DICT['A2'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A2_Gre_Server.short_description = 'Apply to A2'

class Gre_Server_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(Gre_Server_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_Gre_Server, A2_Gre_Server  ]

admin.site.register(Gre_Server,Gre_Server_Admin)

#######################################################################################################################
#################################################### VirPOP-Static #################################################### Done

def Config_VirPOP_Static(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-ixp term up_ixp_%s then policer %sM" % (Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_ixp_%s then policer %sM" %(Gateway,VLAN,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.up-nix term up_nix_%s then policer %sM" % (Gateway,Cus_ID,NIX));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_nix_%s then policer %sM" %(Gateway,VLAN,Cus_ID,NIX));

def A1_VirPOP_Static(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A1',int(obj.IXP),int(obj.NIX))
			Config_VirPOP_Static("A1",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_VirPOP_Static.short_description = 'Apply to A1'

def A2_VirPOP_Static(modeladmin, request,queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A2',int(obj.IXP),int(obj.NIX))
			Config_VirPOP_Static_Ring("A2",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A2'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A2_VirPOP_Static.short_description = 'Apply to A2'

class VirPOP_Static_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(VirPOP_Static_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_Static_Ring, A2_Static_Ring  ]

admin.site.register(VirPOP_Static,VirPOP_Static_Admin)


###########################################################################################################################
#################################################### VirPOP-BGP-Static #################################################### Done

def Config_VirPOP_BGP_Static(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-ixp term up_ixp_%s then policer %sM" % (Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_ixp_%s then policer %sM" %(Gateway,VLAN,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.up-nix term up_nix_%s then policer %sM" % (Gateway,Cus_ID,NIX));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_nix_%s then policer %sM" %(Gateway,VLAN,Cus_ID,NIX));

def A1_VirPOP_BGP_Static(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			VLAN = (obj.VLAN).split(" ")
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A1',int(obj.IXP),int(obj.NIX))
			Config_VirPOP_BGP_Static("A1",Cus_ID,VLAN[0],obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)

	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_VirPOP_BGP_Static.short_description = 'Apply to A1'

def A2_VirPOP_BGP_Static(modeladmin, request,queryset):

	if queryset.count() == 1:
		for obj in queryset:
			VLAN = (obj.VLAN).split(" ")
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A2',int(obj.IXP),int(obj.NIX))
			Config_VirPOP_BGP_Static("A2",Cus_ID,VLAN[1],obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A2'],modeladmin,request,obj.Name)

	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A2_VirPOP_BGP_Static.short_description = 'Apply to A2'

class VirPOP_BGP_Static_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(VirPOP_BGP_Static_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_VirPOP_BGP_Static, A2_VirPOP_BGP_Static  ]

admin.site.register(VirPOP_BGP_Static,VirPOP_BGP_Static_Admin)

###########################################################################################################################
#################################################### DynamicBackup-ISPOther-GRE ########################################### Done

def Config_DynamicBackup_ISPOther(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-ixp term up_ixp_%s then policer %sM" % (Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.down-ISPOther term down_ixp_%s then policer %sM" %(Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.up-nix term up_nix_%s then policer %sM" % (Gateway,Cus_ID,NIX));
	print ("set logical-systems %s firewall family inet filter f.down-ISPOther term down_nix_%s then policer %sM" %(Gateway,Cus_ID,NIX));

def Config_DynamicBackup_Gre_Server(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-ixp term up_ixp_%s then policer %sM" % (Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.down-GRE term down_ixp_%s then policer %sM" %(Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.up-nix term up_nix_%s then policer %sM" % (Gateway,Cus_ID,NIX));
	print ("set logical-systems %s firewall family inet filter f.down-GRE term down_nix_%s then policer %sM" %(Gateway,Cus_ID,NIX));

def A1_DynamicBackup_ISPOther(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A1',int(obj.IXP),int(obj.NIX))
			Config_DynamicBackup_ISPOther("A1",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_DynamicBackup_ISPOther.short_description = 'Apply to A1'

def A2_DynamicBackup_ISPOther(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A2',int(obj.IXP),int(obj.NIX))
			Config_DynamicBackup_Gre_Server("A2",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A2'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A2_DynamicBackup_ISPOther.short_description = 'Apply to A2'

class DynamicBackup_ISPOther_GRE_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(DynamicBackup_ISPOther_GRE_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_DynamicBackup_ISPOther, A2_DynamicBackup_ISPOther  ]

admin.site.register(DynamicBackup_ISPOther_GRE,DynamicBackup_ISPOther_GRE_Admin)


###########################################################################################################################
#################################################### DynamicBackup-ISPOther-VirPOP ######################################## Done

def A1_DynamicBackup_ISPOther_VirPOP(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A1',int(obj.IXP),int(obj.NIX))
			Config_DynamicBackup_ISPOther("A1",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)

	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_DynamicBackup_ISPOther_VirPOP.short_description = 'Apply to A1'

def A2_DynamicBackup_ISPOther_VirPOP(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A2',int(obj.IXP),int(obj.NIX))
			Config_VirPOP_Static("A2",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A2'],modeladmin,request,obj.Name)

	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A2_DynamicBackup_ISPOther_VirPOP.short_description = 'Apply to A2'

class DynamicBackup_ISPOther_VirPOP_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(DynamicBackup_ISPOther_VirPOP_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_DynamicBackup_ISPOther_VirPOP, A2_DynamicBackup_ISPOther_VirPOP  ]

admin.site.register(DynamicBackup_ISPOther_VirPOP,DynamicBackup_ISPOther_VirPOP_Admin)

###########################################################################################################################
#################################################### DynamicBackup-Ring-Ring ############################################## Done

def A1_DynamicBackup_Ring_Ring(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			if obj.Model == "DynamicBackup-Ring-Ring":
				VLAN = (obj.VLAN).split(" ")
				Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
				temp = sys.stdout
				sys.stdout = open("bandwidth.txt","w")
				Policer('A1',int(obj.IXP),int(obj.NIX))
				Config_Static_Ring("A1",Cus_ID,VLAN[0],obj.IXP,obj.NIX)
				sys.stdout.close()
				sys.stdout = temp
				Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_DynamicBackup_Ring_Ring.short_description = 'Apply to A1'

def A2_DynamicBackup_Ring_Ring(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			if obj.Model == "DynamicBackup-Ring-Ring":
				VLAN = (obj.VLAN).split(" ")
				Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
				temp = sys.stdout
				sys.stdout = open("bandwidth.txt","w")
				Policer('A2',int(obj.IXP),int(obj.NIX))
				Config_Static_Ring("A2",Cus_ID,VLAN[1],obj.IXP,obj.NIX)
				sys.stdout.close()
				sys.stdout = temp
				Config_Bandwidth(GATEWAY_DICT['A2'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A2_DynamicBackup_Ring_Ring.short_description = 'Apply to A2'

class DynamicBackup_Ring_Ring_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(DynamicBackup_Ring_Ring_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_DynamicBackup_Ring_Ring, A2_DynamicBackup_Ring_Ring  ]

admin.site.register(DynamicBackup_Ring_Ring,DynamicBackup_Ring_Ring_Admin)

###########################################################################################################################
#################################################### DynamicBackup-SW-EXT-Ring ############################################ Done

def Config_DynamicBackup_SW_EXT(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-ixp term up_ixp_%s then policer %sM" % (Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.down-ext-vlan%s term down_ixp_%s then policer %sM" %(Gateway,VLAN,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.up-nix term up_nix_%s then policer %sM" % (Gateway,Cus_ID,NIX));
	print ("set logical-systems %s firewall family inet filter f.down-ext-vlan%s term down_nix_%s then policer %sM" %(Gateway,VLAN,Cus_ID,NIX));

def A1_DynamicBackup_SW_EXT_Ring(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			VLAN = (obj.VLAN).split(" ")
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A1',int(obj.IXP),int(obj.NIX))
			Config_DynamicBackup_SW_EXT("A1",Cus_ID,VLAN[0],obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_DynamicBackup_SW_EXT_Ring.short_description = 'Apply to A1'

def A2_DynamicBackup_SW_EXT_Ring(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			VLAN = (obj.VLAN).split(" ")
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A2',int(obj.IXP),int(obj.NIX))
			Config_Static_Ring("A2",Cus_ID,VLAN[1],obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A2'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A2_DynamicBackup_SW_EXT_Ring.short_description = 'Apply to A2'

class DynamicBackup_SW_EXT_Ring_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(DynamicBackup_SW_EXT_Ring_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_DynamicBackup_SW_EXT_Ring, A2_DynamicBackup_SW_EXT_Ring  ]

admin.site.register(DynamicBackup_SW_EXT_Ring,DynamicBackup_SW_EXT_Ring_Admin)

###########################################################################################################################
#################################################### DynamicBackup-SW-EXT-VirPop ########################################## Done

def A1_DynamicBackup_SW_EXT_VirPop(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			VLAN = (obj.VLAN).split(" ")
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A1',int(obj.IXP),int(obj.NIX))
			Config_DynamicBackup_SW_EXT("A1",Cus_ID,VLAN[0],obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_DynamicBackup_SW_EXT_VirPop.short_description = 'Apply to A1'

def A2_DynamicBackup_SW_EXT_VirPop(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			VLAN = (obj.VLAN).split(" ")
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A2',int(obj.IXP),int(obj.NIX))
			Config_VirPOP_Static("A2",Cus_ID,VLAN[1],obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A2'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A2_DynamicBackup_SW_EXT_VirPop.short_description = 'Apply to A2'

class DynamicBackup_SW_EXT_VirPop_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(DynamicBackup_SW_EXT_VirPop_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_DynamicBackup_SW_EXT_VirPop, A2_DynamicBackup_SW_EXT_VirPop  ]

admin.site.register(DynamicBackup_SW_EXT_VirPop,DynamicBackup_SW_EXT_VirPop_Admin)


###########################################################################################################################
#################################################### Special ############################################################## Done

def Config_Special(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-ixp term up_ixp_%s then policer %sM" % (Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_ixp_%s then policer %sM" %(Gateway,VLAN,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.up-nix term up_nix_%s then policer %sM" % (Gateway,Cus_ID,NIX));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_nix_%s then policer %sM" %(Gateway,VLAN,Cus_ID,NIX));

def Config_Special_Web(Gateway,Cus_ID,VLAN,WEB):
	print ("set logical-systems %s firewall family inet filter f.up-web term up_web_%s then policer %sM" % (Gateway,Cus_ID,WEB));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_web_%s then policer %sM" %(Gateway,VLAN,Cus_ID,WEB));

def Ar1_Special(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('Ar1',int(obj.IXP),int(obj.NIX))
			Config_Special("Ar1",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['Ar1'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

Ar1_Special.short_description = 'Apply to Ar1'

def Ar2_Special(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('Ar2',int(obj.IXP),int(obj.NIX))
			Config_Special("Ar2",Cus_ID,obj.VLAN,obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['Ar2'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

Ar2_Special.short_description = 'Apply to Ar2'

def Ar1_Special_Web(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('Ar1',int(obj.WEB),int(obj.WEB))
			Config_Special_Web("Ar1",Cus_ID,obj.VLAN,obj.WEB)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['Ar1'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

Ar1_Special_Web.short_description = 'Apply Web to Ar1'

def Ar2_Special_Web(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('Ar2',int(obj.WEB),int(obj.WEB))
			Config_Special_Web("Ar2",Cus_ID,obj.VLAN,obj.WEB)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['Ar2'],modeladmin,request,obj.Name)
	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

Ar2_Special_Web.short_description = 'Apply Web to Ar2 '

class Special_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(Special_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','WEB','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [Edit_Customer,Ar1_Special,Ar2_Special,Ar1_Special_Web,Ar2_Special_Web]  

admin.site.register(Special,Special_Admin)

###########################################################################################################################
#################################################### Transit ############################################################## Done

def Config_Transit_QT(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-ixp term up_ixp_%s then policer %sM" % (Gateway,Cus_ID,IXP));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_ixp_%s then policer %sM" %(Gateway,VLAN,Cus_ID,IXP));

def Config_Transit_TN(Gateway,Cus_ID,VLAN,IXP,NIX):
	print ("set logical-systems %s firewall family inet filter f.up-nix term up_nix_%s then policer %sM" % (Gateway,Cus_ID,NIX));
	print ("set logical-systems %s firewall family inet filter f.down-vlan%s term down_nix_%s then policer %sM" %(Gateway,VLAN,Cus_ID,NIX));

def A1_Transit(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			VLAN = (obj.VLAN).split(" ")
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A1',int(obj.IXP),int(obj.NIX))
			Config_Transit_TN("A1",Cus_ID,VLAN[0],obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A1'],modeladmin,request,obj.Name)

	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A1_Transit.short_description = 'Apply to A1'

def A2_Transit(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			VLAN = (obj.VLAN).split(" ")
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('A2',int(obj.IXP),int(obj.NIX))
			Config_Transit_TN("A2",Cus_ID,VLAN[0],obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['A2'],modeladmin,request,obj.Name)

	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

A2_Transit.short_description = 'Apply to A2'

def At1_Transit(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			VLAN = (obj.VLAN).split(" ")
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('At1',int(obj.IXP),int(obj.NIX))
			Config_Transit_QT("At1",Cus_ID,VLAN[1],obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['At1'],modeladmin,request,obj.Name)

	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

At1_Transit.short_description = 'Apply to At1'

def At2_Transit(modeladmin, request, queryset):

	if queryset.count() == 1:
		for obj in queryset:
			VLAN = (obj.VLAN).split(" ")
			Cus_ID = "%s_%s" %(obj.CusID,obj.Name)
			temp = sys.stdout
			sys.stdout = open("bandwidth.txt","w")
			Policer('At2',int(obj.IXP),int(obj.NIX))
			Config_Transit_QT("At2",Cus_ID,VLAN[1],obj.IXP,obj.NIX)
			sys.stdout.close()
			sys.stdout = temp
			Config_Bandwidth(GATEWAY_DICT['At2'],modeladmin,request,obj.Name)

	else:
		modeladmin.message_user(request, ("Just select one item in order to perform actions on it."), level=messages.ERROR)

At2_Transit.short_description = 'Apply to At2'

class Transit_Admin(admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(Transit_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	search_fields = ('Name', 'CusID')
		
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	list_display_links = None

	list_per_page = 6

	actions = [ Edit_Customer, A1_Transit, A2_Transit, At1_Transit, At2_Transit  ]

admin.site.register(Transit,Transit_Admin)


##################################################################################################################### 
#################################################### Bandwidth ###################################################### Done

class BandwidthResource(resources.ModelResource):
	class Meta:
		model = Bandwidth
		fields = ('id', 'CusID', 'Name','Network','VLAN','IXP','NIX','Model')

# ImportExportModelAdmin
#class Bandwidth_Admin(SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
class Bandwidth_Admin(SimpleHistoryAdmin,admin.ModelAdmin):

	def network(self,obj):
		return  '<br>'.join((obj.Network).split())
	network.allow_tags = True
	network.short_description = 'NETWORK'

	def vlan(self,obj):
		return  '<br>'.join((obj.VLAN).split())
	vlan.allow_tags = True
	vlan.short_description = 'VLAN'

	def get_actions(self, request):
		actions = super(Bandwidth_Admin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	def get_readonly_fields(self, request, obj=None):
		if request.user.is_superuser:
			readonly_fields = ('CreatedAt','LastModified')
			return self.readonly_fields 
		else:
			self.readonly_fields = ('Name', 'CusID','Network','VLAN','WEB','Model','CreatedAt','LastModified')
			return self.readonly_fields 

	fieldsets = [
		('', {'fields': ['Name']}),
		('', {'fields': ['CusID']}),
		('', {'fields': ['Network']}),
		('', {'fields': ['VLAN']}),
		('', {'fields': ['IXP']}),
		('', {'fields': ['NIX']}),
		('', {'fields': ['WEB']}),
		('', {'fields': ['Model']}),
		('', {'fields': ['Note']}),
	]

	resource_class = BandwidthResource

	#readonly_fields = ('CreatedAt','LastModified')

	search_fields = ('Name', 'CusID', 'Network', 'VLAN')

	list_filter = ['Model','Note']
			
	list_display = ('Name','CusID','network','vlan','IXP','NIX','Model','Note')

	history_list_display = ['Network','VLAN','IXP','NIX','WEB','Model',]

	list_per_page = 20

	actions = [ redirect_to_config,  ]

admin.site.register(Bandwidth,Bandwidth_Admin)


#################################################### Log entries ################################################# Done

class FilterBase(admin.SimpleListFilter):
	def queryset(self, request, queryset):
		if self.value():
			dictionary = dict(((self.parameter_name, self.value()),))
			return queryset.filter(**dictionary)

class ActionFilter(FilterBase):
	title = 'action'
	parameter_name = 'action_flag'
	def lookups(self, request, model_admin):
		return action_names.items()

class UserFilter(FilterBase):
	# Use this filter to only show current users, who appear in the log.
	title = 'user'
	parameter_name = 'user_id'
	def lookups(self, request, model_admin):
		return tuple((u.id, u.username)
			for u in User.objects.filter(pk__in =
				LogEntry.objects.values_list('user_id').distinct())
		)

class AdminFilter(UserFilter):
	# Use this filter to only show current Superusers.
	title = 'admin'
	def lookups(self, request, model_admin):
		return tuple((u.id, u.username) for u in User.objects.filter(is_superuser=True))

class StaffFilter(UserFilter):
	# Use this filter to only show current Staff members.
	title = 'staff'
	def lookups(self, request, model_admin):
		return tuple((u.id, u.username) for u in User.objects.filter(is_staff=True))

class LogEntryAdmin(admin.ModelAdmin):

	readonly_fields = LogEntry._meta.get_all_field_names()

	list_display_links = None

	list_per_page = 10

	list_filter = [
		UserFilter,
		ActionFilter,
		'action_time',
	]

	search_fields = [
		'object_repr',
		'change_message'
	]


	list_display = [
		'action_time',
		'user',
		'object_link',
		'action_description',
		'change_message',
	]

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return request.user.is_superuser and request.method != 'POST'

	def has_delete_permission(self, request, obj=None):
		return False

	def object_link(self, obj):
		ct = obj.content_type
		repr_ = escape(obj.object_repr)
		try:
			href = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id])
			link = u'<a href="%shistory">%s</a>' % (href, repr_)
		except NoReverseMatch:
			link = repr_
		return link if obj.action_flag != DELETION else repr_
		
	object_link.allow_tags = True
	object_link.admin_order_field = 'object_repr'
	object_link.short_description = u'object'

	def queryset(self, request):
		return super(LogEntryAdmin, self).queryset(request) \
			.prefetch_related('content_type')

	def action_description(self, obj):
		return action_names[obj.action_flag]
	action_description.short_description = 'Action'

admin.site.register(LogEntry, LogEntryAdmin)


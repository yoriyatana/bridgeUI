from django.db import models

# Create your models here.

from simple_history.models import HistoricalRecords

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError

from django.http import HttpResponseRedirect

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from simple_history.admin import SimpleHistoryAdmin
import sys


class A1_Manager(models.Manager):
    def get_queryset(self):
        return super(A1_Manager,self).get_queryset().filter(Gateway='A1')

class A2_Manager(models.Manager):
    def get_queryset(self):
        return super(A2_Manager,self).get_queryset().filter(Gateway='A2')

class Ar1_Manager(models.Manager):
    def get_queryset(self):
        return super(Ar1_Manager,self).get_queryset().filter(Gateway='Ar1')

class Ar2_Manager(models.Manager):
    def get_queryset(self):
        return super(Ar2_Manager,self).get_queryset().filter(Gateway='Ar2')

class At1_Manager(models.Manager):
    def get_queryset(self):
        return super(At1_Manager,self).get_queryset().filter(Gateway='At1')

class At2_Manager(models.Manager):
    def get_queryset(self):
        return super(At2_Manager,self).get_queryset().filter(Gateway='At2')

class Script_Backup(models.Model):

    Gateway = models.CharField(max_length=255)
    IP = models.CharField(max_length=255)
    Via = models.CharField(max_length=255)
    File = models.CharField(max_length=255)
    

    MODEL_CHOICES = (
        ("Static-Ring", "Static-Ring"),
        ("VirPOP-Static", "VirPOP-Static"),
        ("Special", "Special"),
        ("Transit-TN", "Transit-TN"),
        ("Transit-QT", "Transit-QT")
    )

    Model = models.CharField(
        max_length=255,
        choices=MODEL_CHOICES,
        default="?"
    )

    history = HistoricalRecords()
    
    def __str__(self):
        return '%s' % (self.Gateway)

    class Meta:
        ordering = ['Gateway', 'Via']
        verbose_name = "Gateway"
        verbose_name_plural = " Gateway"

##################################################################################################
############################################### A1 ###############################################

class A1(models.Model):

    Gateway = models.CharField(max_length=255)
    IP = models.CharField(max_length=255)
    Via = models.CharField(max_length=255)
    File = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    
    A1_Objects = A1_Manager()

    def __str__(self):
        return '%s' % (self.Gateway)

    class Meta:
        ordering = ['Gateway','Via']
        verbose_name = "Gateway"
        verbose_name_plural = "A1"
        managed = True
        db_table = 'script_backup_script_backup'

##################################################################################################
############################################### A2 ###############################################

class A2(models.Model):

    Gateway = models.CharField(max_length=255)
    IP = models.CharField(max_length=255)
    Via = models.CharField(max_length=255)
    File = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    
    A2_Objects = A2_Manager()

    def __str__(self):
        return '%s' % (self.Gateway)

    class Meta:
        ordering = ['Gateway','Via']
        verbose_name = "Gateway"
        verbose_name_plural = "A2"
        managed = True
        db_table = 'script_backup_script_backup'

##################################################################################################
############################################### Ar1 ##############################################

class Ar1(models.Model):

    Gateway = models.CharField(max_length=255)
    IP = models.CharField(max_length=255)
    Via = models.CharField(max_length=255)
    File = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    
    Ar1_Objects = Ar1_Manager()

    def __str__(self):
        return '%s' % (self.Gateway)

    class Meta:
        ordering = ['Gateway','Via']
        verbose_name = "Gateway"
        verbose_name_plural = "Ar1"
        managed = True
        db_table = 'script_backup_script_backup'

##################################################################################################
############################################### Ar2 ##############################################

class Ar2(models.Model):

    Gateway = models.CharField(max_length=255)
    IP = models.CharField(max_length=255)
    Via = models.CharField(max_length=255)
    File = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    
    Ar2_Objects = Ar2_Manager()

    def __str__(self):
        return '%s' % (self.Gateway)

    class Meta:
        ordering = ['Gateway','Via']
        verbose_name = "Gateway"
        verbose_name_plural = "Ar2"
        managed = True
        db_table = 'script_backup_script_backup'

##################################################################################################
############################################### At1 ##############################################

class At1(models.Model):

    Gateway = models.CharField(max_length=255)
    IP = models.CharField(max_length=255)
    Via = models.CharField(max_length=255)
    File = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    
    At1_Objects = At1_Manager()

    def __str__(self):
        return '%s' % (self.Gateway)

    class Meta:
        ordering = ['Gateway','Via']
        verbose_name = "Gateway"
        verbose_name_plural = "At1"
        managed = True
        db_table = 'script_backup_script_backup'

##################################################################################################
############################################### At2 ##############################################

class At2(models.Model):

    Gateway = models.CharField(max_length=255)
    IP = models.CharField(max_length=255)
    Via = models.CharField(max_length=255)
    File = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    
    At2_Objects = At2_Manager()

    def __str__(self):
        return '%s' % (self.Gateway)

    class Meta:
        ordering = ['Gateway','Via']
        verbose_name = "Gateway"
        verbose_name_plural = "At2"
        managed = True
        db_table = 'script_backup_script_backup'
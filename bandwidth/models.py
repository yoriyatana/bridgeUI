# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.

class Static_Ring_Manager(models.Manager):
    def get_queryset(self):
        return super(Static_Ring_Manager,self).get_queryset().filter(Model='Static-Ring')

class Static_ISPOther_Manager(models.Manager):
    def get_queryset(self):
        return super(Static_ISPOther_Manager,self).get_queryset().filter(Model='Static-ISPOther')

class Gre_Server_Manager(models.Manager):
    def get_queryset(self):
        return super(Gre_Server_Manager,self).get_queryset().filter(Model='Gre-Server')

class VirPOP_Static_Manager(models.Manager):
    def get_queryset(self):
        return super(VirPOP_Static_Manager,self).get_queryset().filter(Model='VirPOP-Static')

class VirPOP_BGP_Static_Manager(models.Manager):
    def get_queryset(self):
        return super(VirPOP_BGP_Static_Manager,self).get_queryset().filter(Model='VirPOP-BGP-Static')

class DynamicBackup_ISPOther_GRE_Manager(models.Manager):
    def get_queryset(self):
        return super(DynamicBackup_ISPOther_GRE_Manager,self).get_queryset().filter(Model='DynamicBackup-ISPOther-GRE')  

class DynamicBackup_ISPOther_VirPOP_Manager(models.Manager):
    def get_queryset(self):
        return super(DynamicBackup_ISPOther_VirPOP_Manager,self).get_queryset().filter(Model='DynamicBackup-ISPOther-VirPOP')

class DynamicBackup_Ring_Ring_Manager(models.Manager):
    def get_queryset(self):
        return super(DynamicBackup_Ring_Ring_Manager,self).get_queryset().filter(Model='DynamicBackup-Ring-Ring')  

class DynamicBackup_SW_EXT_Ring_Manager(models.Manager):
    def get_queryset(self):
        return super(DynamicBackup_SW_EXT_Ring_Manager,self).get_queryset().filter(Model='DynamicBackup-SW-EXT-Ring')  

class DynamicBackup_SW_EXT_VirPop_Manager(models.Manager):
    def get_queryset(self):
        return super(DynamicBackup_SW_EXT_VirPop_Manager,self).get_queryset().filter(Model='DynamicBackup-SW-EXT-VirPop')            

class Special_Manager(models.Manager):
    def get_queryset(self):
        return super(Special_Manager,self).get_queryset().filter(Model='Special')   

class Transit_Manager(models.Manager):
    def get_queryset(self):
        return super(Transit_Manager,self).get_queryset().filter(Model='Transit')

########################################################################################
########################################################################################

class Bandwidth(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=7,blank=True)
    IXP = models.CharField(max_length=3)
    NIX = models.CharField(max_length=3)
    WEB = models.CharField(max_length=3,blank=True)

    MODEL_CHOICES = (
        ("Static-Ring", "Static-Ring"),
        ("Static-ISPOther", "Static-ISPOther"),
        ("Gre-Server", "Gre-Server"),
        ("VirPOP-Static", "VirPOP-Static"),
        ("VirPOP-BGP-Static", "VirPOP-BGP-Static"),
        ("DynamicBackup-ISPOther-GRE", "DynamicBackup-ISPOther-GRE"),
        ("DynamicBackup-ISPOther-VirPOP", "DynamicBackup-ISPOther-VirPOP"),
        ("DynamicBackup-Ring-Ring", "DynamicBackup-Ring-Ring"),
        ("DynamicBackup-SW-EXT-Ring", "DynamicBackup-SW-EXT-Ring"),
        ("DynamicBackup-SW-EXT-VirPop", "DynamicBackup-SW-EXT-VirPop"),
        ("Special", "Special"),
        ("Transit", "Transit"),
    )

    Model = models.CharField(
        max_length=255,
        choices=MODEL_CHOICES,
        default="?"
    )

    CreatedAt = models.DateTimeField('Created',auto_now_add=True)
    LastModified = models.DateTimeField('Last Modified',auto_now=True)
    Note = models.CharField(max_length=255,blank=True)

    history = HistoricalRecords()


    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "Customer"
        verbose_name_plural = " Summary"

class Static_Ring(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    Static_Ring_Objects = Static_Ring_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "Static Ring Customer"
        verbose_name_plural = 'Static Ring'
        managed = True
        db_table = 'bandwidth_bandwidth'

class Static_ISPOther(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    Static_ISPOther_Objects = Static_ISPOther_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "Static ISPOther Customer"
        verbose_name_plural = 'Static ISPOther'
        managed = True
        db_table = 'bandwidth_bandwidth'

class Gre_Server(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    Gre_Server_Objects = Gre_Server_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "Gre Customer"
        verbose_name_plural = 'Gre Server'
        managed = True
        db_table = 'bandwidth_bandwidth' 

class VirPOP_Static(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    VirPOP_Static_Objects = VirPOP_Static_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "VirPOP Static Customer"
        verbose_name_plural = 'VirPOP Static'
        managed = True
        db_table = 'bandwidth_bandwidth'

class VirPOP_BGP_Static(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    VirPOP_BGP_Static_Objects = VirPOP_BGP_Static_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "VirPOP BGP Static Customer"
        verbose_name_plural = 'VirPOP BGP Static'
        managed = True
        db_table = 'bandwidth_bandwidth'

class DynamicBackup_ISPOther_GRE(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    DynamicBackup_ISPOther_GRE_Objects = DynamicBackup_ISPOther_GRE_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "DynamicBackup ISPOther GRE Customer"
        verbose_name_plural = 'DynamicBackup ISPOther GRE'
        managed = True
        db_table = 'bandwidth_bandwidth' 

class DynamicBackup_ISPOther_VirPOP(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    DynamicBackup_ISPOther_VirPOP_Objects = DynamicBackup_ISPOther_VirPOP_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "DynamicBackup ISPOther VirPOP Customer"
        verbose_name_plural = 'DynamicBackup ISPOther VirPOP'
        managed = True
        db_table = 'bandwidth_bandwidth' 

class DynamicBackup_Ring_Ring(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    DynamicBackup_Ring_Ring_Objects = DynamicBackup_Ring_Ring_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "DynamicBackup Ring Ring Customer"
        verbose_name_plural = 'DynamicBackup Ring Ring'
        managed = True
        db_table = 'bandwidth_bandwidth' 

class DynamicBackup_SW_EXT_Ring(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    DynamicBackup_SW_EXT_Ring_Objects = DynamicBackup_SW_EXT_Ring_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "DynamicBackup SW EXT Ring Customer"
        verbose_name_plural = 'DynamicBackup SW EXT Ring'
        managed = True
        db_table = 'bandwidth_bandwidth' 

class DynamicBackup_SW_EXT_VirPop(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    DynamicBackup_SW_EXT_VirPop_Objects = DynamicBackup_SW_EXT_VirPop_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "DynamicBackup SW EXT VirPop Customer"
        verbose_name_plural = 'DynamicBackup SW EXT VirPop'
        managed = True
        db_table = 'bandwidth_bandwidth' 

class Special(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    WEB = models.CharField(max_length=255,blank=True)
    Special_Objects = Special_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "Special Customer"
        verbose_name_plural = 'Special'
        managed = True
        db_table = 'bandwidth_bandwidth'

class Transit(models.Model):

    CusID = models.CharField('Cus ID',max_length=255)
    Name = models.CharField('Name',max_length=255)
    Network = models.CharField(max_length=255)
    VLAN = models.CharField(max_length=255,blank=True)
    IXP = models.CharField(max_length=255)
    NIX = models.CharField(max_length=255)
    Model = models.CharField(max_length=255)
    Note = models.CharField(max_length=255,blank=True)
    Transit_Objects = Transit_Manager()

    def __str__(self):
        return '%s' % (self.Name)

    class Meta:
        ordering = ['Name']
        verbose_name = "Transit Customer"
        verbose_name_plural = 'Transit'
        managed = True
        db_table = 'bandwidth_bandwidth'    

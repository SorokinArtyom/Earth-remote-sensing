from django.db import models


# Create your models here.

class Forest_Images(models.Model):
    Image = models.ImageField(upload_to='Images')

    class Meta:
        managed = True
        db_table = 'Forest_Images'

    #def __str__(self):
    #    return self.Image


class Water_Images(models.Model):
    Image = models.ImageField(upload_to='Images')

    class Meta:
        managed = True
        db_table = 'Water_Images'


class City_Images(models.Model):
    Image = models.ImageField(upload_to='Images')

    class Meta:
        managed = True
        db_table = 'City_Images'


class Meadows_Images(models.Model):
    Image = models.ImageField(upload_to='Images')

    class Meta:
        managed = True
        db_table = 'Meadows_Images'



class Saved_Images(models.Model):
    Image = models.IntegerField(db_column='ID_Image')
    Users = models.IntegerField(db_column='ID_User')

    class Meta:
        managed = True
        db_table = 'Saved_Image'


class ALL_Images(models.Model):

    Image = models.ImageField(upload_to='Images')
    Type = models.IntegerField(db_column='ID_Type')

    class Meta:
        managed = True
        db_table = 'ALL_Images'


class Types_Images(models.Model):
    Type = models.CharField(db_column='Type', max_length=20)

    class Meta:
        managed = True
        db_table = 'Types_Images'
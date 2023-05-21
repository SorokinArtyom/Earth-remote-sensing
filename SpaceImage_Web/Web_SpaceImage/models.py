from django.db import models


# Create your models here.
class ALL_Images(models.Model):

    Image = models.ImageField(upload_to='Images')
    Type = models.IntegerField(db_column='ID_Type')
    UsersID = models.IntegerField(db_column='ID_User')


    class Meta:
        managed = True
        db_table = 'ALL_Images'


class Types_Images(models.Model):
    Type = models.CharField(db_column='Type', max_length=20)

    class Meta:
        managed = True
        db_table = 'Types_Images'
from django.db import models
import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your models here.


class Attribute(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    capacity = models.IntegerField()
    attributes = models.ManyToManyField(Attribute)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class FreeTerm(models.Model):
    room = models.ForeignKey(Room)
    date = models.DateField()
    begin = models.IntegerField()
    end = models.IntegerField()

    def __str__(self):  # __unicode__ on Python 2
        return self.room.name + ' ' + self.date.strftime('%d-%m-%Y') + ' ' + str(self.begin) + '-' + str(self.end)

    def clean(self):
        #check for expired date
        if self.date < datetime.date.today():
            raise ValidationError("Provided date is in the past")

        #check for proper hours
        if self.begin >= self.end:
            raise ValidationError("The end hours has to be past beginning hour")

        if self.begin < 0 or self.end > 24:
            raise ValidationError("An hour is an integer in range [0;24]")

        #check if the new term doesn't cross an already existing FreeTerm for the given room and date
        lookup_range = FreeTerm.objects.filter(date=self.date).filter(room=self.room)
        tmp1 = lookup_range.filter(begin__gt=self.begin).filter(end__lte=self.end)
        tmp2 = lookup_range.filter(begin__gte=self.begin).filter(end__lt=self.end)
        tmp3 = lookup_range.filter(begin__lte=self.begin).filter(end__gte=self.end)

        if tmp1.count() + tmp2.count() + tmp3.count() > 0:
            raise ValidationError("Provided hours intersect with an existing FreeTerm")

        #check if the new term doesn't cross an existing Reservation
        lookup_range = Reservation.objects.filter(date=self.date).filter(room=self.room)
        tmp1 = lookup_range.filter(begin__gt=self.begin).filter(end__lte=self.end)
        tmp2 = lookup_range.filter(begin__gte=self.begin).filter(end__lt=self.end)
        tmp3 = lookup_range.filter(begin__lte=self.begin).filter(end__gte=self.end)

        if tmp1.count() + tmp2.count() + tmp3.count() > 0:
            raise ValidationError("Provided hours intersect with an existing Reservation")


class Reservation(models.Model):
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room)
    date = models.DateField()
    begin = models.IntegerField()
    end = models.IntegerField()

    def __str__(self):
        return self.room.name + ' ' + self.date.strftime('%d-%m-%Y') + ' ' + str(self.begin) + '-' + str(self.end)

    def clean(self):
        #check for proper hours
        if self.begin >= self.end:
            raise ValidationError("The end hours has to be past beginning hour")

        if self.begin < 0 or self.end > 24:
            raise ValidationError("An hour is an integer in [0;24]")

    def save(self, *args, **kwargs):
        tmp = FreeTerm.objects.select_for_update().filter(date=self.date).filter(room=self.room) \
            .filter(begin__lte=self.begin).filter(end__gte=self.end)

        if tmp.count() == 0:
            raise IntegrityError("No FreeTerm in provided time")

        for term in tmp:
            super(Reservation, self).save(*args, **kwargs)

            FreeTerm.objects.filter(date=term.date).filter(room=term.room) \
                .filter(begin=term.begin).filter(end=term.end).delete()

            #adding (if needed) new terms created due to splitting from reservation
            if term.begin != self.begin:
                x = FreeTerm(room=self.room, date=self.date, begin=term.begin, end=self.begin)
                x.save()

            if term.end != self.end:
                y = FreeTerm(room=self.room, date=self.date, begin=self.end, end=term.end)
                y.save()

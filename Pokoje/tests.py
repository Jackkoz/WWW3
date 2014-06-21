from django.test import TestCase
from Pokoje.models import Room, FreeTerm, Reservation
import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Create your tests here.


class FreeTermTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="test", capacity=123, description="test_description")
        self.term = FreeTerm.objects.create(room=self.room, date=datetime.date.today(), begin=18, end=21)
        self.date = datetime.date.today()

    def testHour(self):
        err = False

        testTerm = FreeTerm(room=self.room, date=self.date, begin=-3, end=5)
        try:
            testTerm.clean()
        except ValidationError:
            err = True
        self.assertTrue(err)

        err = False

        testTerm = FreeTerm(room=self.room, date=self.date, begin=10, end=9)
        try:
            testTerm.clean()
        except ValidationError:
            err = True
        self.assertTrue(err)

        err = True

        testTerm = FreeTerm(room=self.room, date=self.date, begin=10, end=15)
        try:
            testTerm.clean()
        except ValidationError:
            err = False
        self.assertTrue(err)

    def testDate(self):
        err = False
        testTerm = FreeTerm(room=self.room, date=(self.date - datetime.timedelta(days=1)), begin=10, end=15)

        try:
            testTerm.clean()
        except ValidationError:
            err = True
        self.assertTrue(err)

    def testTerm(self):
        err = False
        testTerm = FreeTerm.objects.create(room=self.room, date=self.date, begin=19, end=20)

        try:
            testTerm.clean()
        except ValidationError:
            err = True
        self.assertTrue(err)


class ReservationTest(TestCase):
    def setUp(self):
        self.room1 = Room.objects.create(name="test1", capacity=1, description="asd")
        self.room2 = Room.objects.create(name="test2", capacity=2, description="dsa")
        self.term1 = FreeTerm.objects.create(room=self.room1, date=datetime.date.today(), begin=13, end=18)
        self.term2 = FreeTerm.objects.create(room=self.room2, date=datetime.date.today(), begin=5, end=15)
        self.user = User.objects.create_user('user', 'user@user.com', 'password')
        self.date = datetime.date.today()

    def testHour(self):
        err = False

        reservation = Reservation(room=self.room1, user=self.user, date=self.date, begin=-3, end=14)

        try:
            reservation.clean()
        except ValidationError:
            err = True
        self.assertTrue(err)

        err = False
        reservation = Reservation(room=self.room1, user=self.user, date=self.date, begin=15, end=14)
        try:
            reservation.clean()
        except ValidationError:
            err = True
        self.assertTrue(err)

    def testSplit(self):
        reservation = Reservation(room=self.room2, user=self.user, date=self.date, begin=10, end=12)
        reservation.save()

        self.assertTrue(FreeTerm.objects.filter(room=self.room2).filter(date=datetime.date.today())\
                        .filter(begin=5).filter(end=10).exists())
        self.assertTrue(FreeTerm.objects.filter(room=self.room2).filter(date=datetime.date.today())\
                        .filter(begin=12).filter(end=15).exists())

    def testNoTerm(self):
        err = False
        reservation = Reservation(room=self.room1, user=self.user, date=self.date, begin=2, end=4)

        try:
            reservation.save()
        except IntegrityError:
            err = True
        self.assertTrue(err)

    def tearDown(self):
        self.user.delete()
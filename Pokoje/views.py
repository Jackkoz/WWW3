import django.contrib.auth
import django.contrib.sessions.serializers
import django.http
from django.shortcuts import render, redirect
import django.template
import django.utils.dateformat
from Pokoje.models import Room, FreeTerm, Reservation, Attribute
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from Pokoje.forms import ReservationForm, SearchForm
from django.core.context_processors import csrf
import datetime
from django.db import transaction
from django.db import IntegrityError
import django_tables2 as tables
from django_tables2.utils import A
from django_tables2 import RequestConfig
import json
from django.core import serializers

# Create your views here.


class RoomTable(tables.Table):
    class Meta:
        model = Room
        empty_text = "No rooms to display"
        attrs = {"class": "paleblue"}

    name = tables.LinkColumn('room', args=[A('pk')])
    my_column = tables.TemplateColumn(verbose_name=(' '),
            template_name='my_column.html',
            orderable=False)


class TermTable(tables.Table):
    class Meta:
        model = FreeTerm
        empty_text = "No free terms to display"
        attrs = {"class": "paleblue"}


class ReservationTable(tables.Table):
    class Meta:
        model = Reservation
        empty_text = "No reservations to display"
        attrs = {"class": "paleblue"}


def userlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = django.contrib.auth.authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            messages.error(request, 'Your account is inactive')
    else:
        messages.error(request, 'Incorrect login data')
    return redirect('template')


def userlogout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('template')


def room_list(request):
    if not request.user.is_authenticated():
        messages.error(request, 'You must log in to reserve a room')
        return redirect('template')
    else:
        rooms = Room.objects.all()
        table = RoomTable(rooms)
        RequestConfig(request).configure(table)
        table.paginate(page=request.GET.get('page', 1), per_page=10)

        result = {}
        result.update(csrf(request))
        result['table'] = table
        result['rooms'] = rooms
        return render(request, 'room_list.html', result)


def search(request):
    if not request.user.is_authenticated():
        return redirect('template')

    if not request.method == "POST":
        form = SearchForm()
    else:
        form = SearchForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']

            searchedName = Room.objects.filter(name__contains=key)
            searchedCapacity = Room.objects.filter(capacity__contains=key)
            searchedDescription = Room.objects.filter(description__contains=key)
            result = searchedName | searchedCapacity | searchedDescription

            min_capacity = form.cleaned_data['min_capacity']
            if min_capacity:
                result = result.filter(capacity__gte=min_capacity)

            max_capacity = form.cleaned_data['max_capacity']
            if max_capacity:
                result = result.filter(capacity__lte=max_capacity)

            attr = request.POST.getlist('attributes')
            for a in attr:
                result = result.filter(attributes__name=a)

            table = RoomTable(result)
            RequestConfig(request).configure(table)
            table.paginate(page=request.GET.get('page', 1), per_page=10)

            # return render(request, 'search_list.html', {'table': table})
            return render(request, 'room_list.html', {'rooms': result})

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'search.html', args)


#reservations made by logged user
def reservations(request):
    if not request.user.is_authenticated():
        return redirect('template')
    else:
        userReservations = Reservation.objects.filter(user=request.user.id)

        table = ReservationTable(userReservations)
        RequestConfig(request).configure(table)
        table.paginate(page=request.GET.get('page', 1), per_page=10)

        result = {}
        result.update(csrf(request))
        result['table'] = table

        return render(request, 'reservations.html', result)


#show room details
def room(request, room_id=1):
    if not request.user.is_authenticated():
        return redirect('template')

    result = {'room': Room.objects.get(id=room_id)}
    return render(request, "room.html", result)


def update_database(request):
    now = datetime.datetime.now()
    FreeTerm.objects.filter(date__lt=now.date()).delete()
    Reservation.objects.filter(date__lt=now.date()).delete()


def term(request, room_id=1):
    update_database(request)

    if not request.user.is_authenticated():
        return redirect('template')

    requestedRoom = Room.objects.get(id=room_id)

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            tempForm = form.save(commit=False)
            isFree = FreeTerm.objects.filter(date=tempForm.date).filter(room=room_id)\
                .filter(begin__lte=tempForm.begin).filter(end__gte=tempForm.end)

            if isFree.count() == 0:
                messages.error(request, 'The room is not free in the provided term')
            elif isFree.count() == 1:
                for a in isFree:
                    tempForm.room = requestedRoom
                    tempForm.user = request.user

                    confirmationForm = {}
                    confirmationForm['form'] = tempForm

                    request.session['form_date'] = tempForm.date.isoformat()
                    request.session['form_room'] = tempForm.room_id
                    request.session['form_begin'] = tempForm.begin
                    request.session['form_end'] = tempForm.end
                return render(request, 'confirmation.html', confirmationForm)
            else:  # assert(false)
                messages.error(request, 'An unexpected error occurred')
    else:
        form = ReservationForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form

    table = TermTable(FreeTerm.objects.all().filter(room=requestedRoom))
    table.paginate(page=request.GET.get('page', 1), per_page=10)
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get('page', 1), per_page=10)
    args['table'] = table

    return render(request, 'reserve.html', args)


def ajax_term(request, room_id=1):
    update_database(request)

    requestedRoom = Room.objects.get(id=room_id)

    args = {}
    args['terms'] = FreeTerm.objects.values('date').filter(room=requestedRoom).distinct()
    args['terms'] = args['terms'].extra(order_by=['date'])
    args['fullt'] = FreeTerm.objects.filter(room=requestedRoom).extra(order_by=['begin'])
    args['room'] = requestedRoom.id
    # args['user'] = request.user

    return render(request, 'ajax_reserve.html', args)


def confirm(request):
    date = request.session.get('form_date')
    room_id = request.session.get('form_room')
    begin = request.session.get('form_begin')
    end = request.session.get('form_end')

    res_room = Room.objects.get(id=room_id)
    res = Reservation(room=res_room, user=request.user, date=date, begin=begin, end=end)

    try:
        with transaction.atomic():
            res.save()
            messages.success(request, 'The room has been reserved')
    except IntegrityError:
        messages.error(request, 'An error has occurred, please try again')

    return redirect('template')


def ajax_confirm(request):
    date = request.POST['date']
    room_id = request.POST['room']
    hours = request.POST.getlist('hours[]')
    res_room = Room.objects.get(id=room_id)
    previous = -1
    start = -1
    end = 0

    try:
        for h in hours:
            h1 = int(h)
            if not FreeTerm.objects.all().filter(begin__lte=h1).filter(end__gte=h1):
                args = {}
                args['start'] = h1
                args['end'] = h1 + 1
                return render(request, 'fail.html', args)
            if h1 == previous + 1:
                if start == -1:
                    start = 0

                if not FreeTerm.objects.all().filter(begin__lte=start).filter(end__gte=h1):
                    end = previous
                    res = Reservation(room=res_room, user=request.user, date=date, begin=start, end=end)
                    with transaction.atomic():
                        res.save()

                    start = previous
                    previous = h1
                    end = h1 + 1
                else:
                    previous = h1
                    end = h1 + 1

            else:
                if start != -1:
                    res = Reservation(room=res_room, user=request.user, date=date, begin=start, end=end)
                    with transaction.atomic():
                        res.save()

                previous = h1
                start = h1
                end = h1 + 1

        res = Reservation(room=res_room, user=request.user, date=date, begin=start, end=end)
        with transaction.atomic():
            res.save()

    except IntegrityError:
        args = {}
        args['start'] = start
        args['end'] = end
        return render(request, 'fail.html', args)

    return render(request, 'success.html')


def success(request):
    return render(request, 'success.html')


def offline(request):
    args = {}
    args['rooms'] = Room.objects.all()
    args['terms'] = FreeTerm.objects.all()
    args['reservations'] = Reservation.objects.all().filter(user=request.user)
    args['attributes'] = Attribute.objects.all()


    return render(request, args)


# def offline_db(request):
#     data = serializers.serialize("json", list(Room.objects.all())
#             + list(FreeTerm.objects.all()) + list(Attribute.objects.all()))
#     return django.http.HttpResponse(data, content_type="application/json")


def offline_db(request):
    room_json = serializers.serialize('json', Room.objects.all())
    room_list = json.loads(room_json)

    term_json = serializers.serialize('json', FreeTerm.objects.all())
    term_list = json.loads(term_json)

    attribute_json = serializers.serialize('json', Attribute.objects.all())
    attribute_list = json.loads(attribute_json)

    json_data = json.dumps({'rooms': room_list, 'terms': term_list, 'attributes': attribute_list})
    return django.http.HttpResponse(json_data, content_type='application/json')
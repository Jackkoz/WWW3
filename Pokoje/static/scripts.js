var rooms = [];
var terms = [];
var attributes = [];

function Room(id, name, description, capacity, attributes)
{
    this.id = id;
    this.name = name;
    this.description = description;
    this.capacity = capacity;
    this.attributes = attributes;

}

Room.prototype.getInfo = function() {
return this.id + ' ' + this.name + ' ' + this.description;
};

function FreeTerm(id, room, date, begin, end)
{
    this.id = id;
    this.room = room;
    this.date = date;
    this.begin = begin;
    this.end = end;
}

function Attribute(id, name)
{
    this.id = id;
    this.name = name;
}

function fetchData()
{
    $.getJSON( "/reserve/offline", function(data)
    {
        $.each( data['rooms'], function( key, val ) {
            var room = new Room(val['pk'], val['fields']['name'], val['fields']['description'],
                    val['fields']['capacity'], val['fields']['attributes']);
            rooms.push(room);
        });

        localStorage.setItem("rooms", JSON.stringify(rooms));

        $.each(data['terms'], function(key, val) {
            terms.push(new FreeTerm(val['pk'], val['fields']['room'], val['fields']['date'],
                    val['fields']['begin'], val['fields']['end']));
        });

        terms.sort(function(a,b)
        {
            return a > b;
        });

        localStorage.setItem("terms", JSON.stringify(terms));

        $.each(data['attributes'], function(key, val) {
           attributes.push(new Attribute(val['pk'], val['fields']['name']));
        });

        localStorage.setItem("attributes", JSON.stringify(attributes));
    });
}

function retrieveData()
{
    rooms = JSON.parse(localStorage.getItem("rooms"));
    terms = JSON.parse(localStorage.getItem("terms"));
    attributes = JSON.parse(localStorage.getItem("attributes"));
}

function offline()
{
        retrieveData();

        $('#search').append('Key: <INPUT TYPE="text" id="key" VALUE=""></input><P></p>');
        $('#search').append('Capacity: <INPUT TYPE="text" id="from" VALUE=""> - <INPUT TYPE="text" id="to" VALUE=""><P>');
        for (i=0; i<attributes.length; i++)
            $('#search').append(attributes[i].name+': <INPUT TYPE="checkbox" id="'+attributes[i].id+'" VALUE=""><P>');

        $('#search').append('<button class="btn btn-warning" role="button" onclick="search()">Search</button>');

        showRooms(rooms);
}

function showRooms(rooms)
{
    var table = "<table class=\"table\">\
                <thead>\
                    <tr>\
                        <th>\
                            Name\
                        </th>\
                        <th>\
                            Capacity\
                        </th>\
                        <th>\
                            Description\
                        </th>\
                    </tr>\
                </thead>\
                <tbody> ";

    for (var i = 0; i < rooms.length; i++)
    {
        table = table.concat("<tr>\
        <td>"+rooms[i].name+"</td>\
        <td>"+rooms[i].capacity+"</td>\
        <td>"+rooms[i].description+"</td>\
        <td>\
            <button class='btn btn-primary btn-small' id='przycisk'\
                    onclick=\"showModal('"+rooms[i].id+"')\" >\
                Reserve\
            </button>\
        </td>\
        <br>\
        </tr>");
    }

    table = table.concat("	</tbody> </table>");
    $('#room-table').html(table);
}

function search()
{
    var result = rooms;
    var key = $('#key').val();

    if (key !== '')
    {
        result = result.filter(function(obj) {
           return (obj.name.indexOf(key) > -1) || (obj.description.indexOf(key) > -1);
        });
    }

    var from = $('#from').val();
    if (! isNaN(from) && from !== "")
    {
        result = result.filter(function(obj) {
           return obj.capacity >= from;
        });
    }

    var to = $('#to').val();

    if (! isNaN(to) && to !== "")
    {
        result = result.filter(function(obj) {
           return obj.capacity <= to;
        });
    }

    for (var i = 0; i < attributes.length; i++)
    {
        var j = i+1;
        var box = $('#'+j).is(':checked');
        if (box)
        {
            result = result.filter(function(obj) {
                return obj.attributes.indexOf(j) > -1;
            });
        }
    }

    showRooms(result);
}

function showModal(id)
{
    newTerms = terms.filter(function(obj) {
        return obj.room == id;
    });

    for (var i = newTerms.length - 1; i > 0; i--)
        if (newTerms[i].date === newTerms[i-1].date)
            newTerms.splice(i, 1);

    newTerms.sort(function(a, b) {
        return a.date > b.date;
    });

    $('#accordion').html('');

    for (var i = 0; i < newTerms.length; i++)
    {
        insertTerm(newTerms[i]);
    }

    $('#myModal').modal('show');
}

function insertTerm(term)
{
    var panel = '\
        <div class="panel panel-default">\
            <div class="panel-heading">\
              <h4 class="panel-title">\
                <a data-toggle="collapse" data-parent="#accordion"\
                        href="#collapse'+term.date+'">\
                    '+term.date+' :';
                    for (var i = 0; i < terms.length; i++)
                    {
                        if (terms[i].date == term.date)
                            panel = panel.concat(' (' + terms[i].begin + ' - ' + terms[i].end + ')');
                    }
               panel = panel.concat('</a>\
              </h4>\
            </div>\
            <div id="collapse'+term.date+'" class="panel-collapse collapse" >\
              <div class="panel-body" id="'+term.date+'">\
                  <div class="btn-group" data-toggle="buttons" id="checkboxy">');
                  for (var i = 0; i < terms.length; i++)
                  {
                      if (terms[i].date == term.date)
                      {
                          for (var h = 0; h < 24; h++)
                          {
                              if (h >= terms[i].begin && h < terms[i].end)
                              {
                                  panel = panel.concat('<label class="btn btn-primary">\
                                        <input type="checkbox" name="'+term.date+'"\
                                               value="'+h+'"> '+h+'\
                                  </label>');
                              }
                          }
                      }
                  }

                  panel = panel.concat('</div>\
                    <br><hr>\
                    <div id="info">\
                    </div>\
                  <button class="btn btn-info btn-small" id="przycisk"\
                          onclick="confirm(\''+term.date+'\',\
                                  $(\'input:checkbox[name='+term.date+']:checked\'),'+ term.room+')" >\
                      Reserve\
                  </button>\
              </div>\
            </div>\
        </div>\
        ');

    $('#accordion').append(panel);
}

function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});

function confirm(date, hours, room)
{
    var hours_array = [];
    hours.each(function()
    {
        hours_array.push($(this).val());
    });
    if (hours_array.length === 0)
        return;

    var d = new Date(date);
    var converted_date = d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);

    var jqxhr = $.ajax( "/reserve/ajax_confirm", {type:"POST",
            data: {'date': converted_date, 'room': room, 'user': '{{ user }}','hours': hours_array} } )
        .done(function(data) {
            console.log( "success" );
                window.alert(data);
        })
        .fail(function(data) {
            console.log( "error" );
                window.alert("Could not reach the reservation server.");
        })
        .always(function() {
        });
}

function confirmOffline(date, hours, room)
{
      var hours_array = [];
    hours.each(function()
    {
        hours_array.push($(this).val());
    });
    if (hours_array.length === 0)
        return;

    var d = new Date(date);
    var converted_date = d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);

    var jqxhr = $.ajax( "/reserve/ajax_confirm", {type:"POST",
        data: {'date': converted_date, 'room': room, 'user': '{{ user }}','hours': hours_array} } )
        .done(function(data) {
            console.log( "success" );
            window.alert(data);
        })
        .fail(function(data) {
            console.log( "error" );
            window.alert("Please go online to make a reservation.");
        })
        .always(function() {
        });
}
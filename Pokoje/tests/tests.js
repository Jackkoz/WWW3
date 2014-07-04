//function Room(id, name, description, capacity, attributes)
//    {
//        this.id = id;
//        this.name = name;
//        this.description = description;
//        this.capacity = capacity;
//        this.attributes = attributes;
//
//    }
//
//    function FreeTerm(id, room, date, begin, end)
//    {
//        this.id = id;
//        this.room = room;
//        this.date = date;
//        this.begin = begin;
//        this.end = end;
//    }
//
//    function Attribute(id, name)
//    {
//        this.id = id;
//        this.name = name;
//    }


QUnit.test("Room test", function(assert)
{
    var room = new Room(15, "pokój", "z widokiem na wojnę", 4363, [1, 3]);

    assert.ok(room.id === 15, "ok");
    assert.ok(room.name === "pokój", "ok");
    assert.ok(room.description === "z widokiem na wojnę", "ok");
    assert.ok(room.capacity === 4363, "ok");
});

QUnit.test("Term test", function(assert)
{
    var term = new FreeTerm(54, 2, "2010-06-04", 15, 18);
    assert.ok(term.id === 54, "ok");
    assert.ok(term.room === 2, "ok");
    console.log(term.date);
    assert.ok(term.date === "2010-06-04", "ok");
    assert.ok(term.begin === 15, "ok");
    assert.ok(term.end === 18, "ok");
});

QUnit.test("Attribute test", function(assert)
{
   var attribute = new Attribute(1, "chair");
    assert.ok(attribute.id === 1, "ok");
    assert.ok(attribute.name === "chair", "ok");
});

//QUnit.test("Search test", function(assert)
//{
//    var rooms = [];
//    rooms.push(new Room(15, "pokój", "z widokiem na wojnę", 4363, [1, 3]));
//    rooms.push(new Room(123, "room", "testtesttest", 444, [2]));
//
//});
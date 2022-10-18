db = db.getSiblingDB("catalogos_db");
db.catalogo_tb.drop();

db.catalogo_tb.insertMany([
    {
        "id": 1,
        "name": "The Red Carpet",
        "description": "An example of catalog",
        "user": "Mariana Hinojosa"
    },
    {
        "id": 2,
        "name": "The Crown",
        "description": "An example of catalog 2",
        "user": "Fher Torres"
    },
    {
        "id": 3,
        "name": "Something",
        "description": "An example of catalog 3",
        "user": "Mariana Hinojosa"
    },
]);
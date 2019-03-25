# Customers Service

The Customer service will allow developers to exchange data between the web application and the customer database.

## Installation

To run the application locally, download the code to a local directory. This application uses Vagrant. Please ensure that it is installed.

To test if you have Vagrant installed, enter the following in the command line

```
vagrant -v
```

## Running  the Application

Start the virtual environment with the following command

```
vagrant up
```

Then, ssh into the virtual environment with the following command

```
vagrant ssh
```

## Customer Collection documentation

The service will follow the RESTful structure. The collection will contain the CRUD methods and a few others.

### Create
Create a new customer in the customer database.
```
POST    /customers
```

#### Test for Create
```
POST    /customers
Request
Body:{
	"firstname":"John",
	"lastname":"Doe",
	"email":"jdoe@email.com",
	"subscribed": true,
	"address": {
		"address1": "1 Second St",
		"address2":"1B",
		"city":"New York",
		"province":"NY",
		"country":"USA",
		"zip":"24233"
	}
}

Response
Expected Status: 201
Body:{
    "address": {
        "address1": "1 Second St",
        "address2": "1B",
        "city": "New York",
        "country": "USA",
        "province": "NY",
        "zip": "24233"
    },
    "email": "jdoe@email.com",
    "firstname": "John",
    "id": 2,
    "lastname": "Doe",
    "subscribed": true
}
```

### Read
Read customer data from the customer database.
```
GET    /customers/2
```

#### Test for Read
```
GET    /customers/2

Response
Excpected Status: 200
Body:{
    "address": {
        "address1": "1 Second St",
        "address2": "1B",
        "city": "New York",
        "country": "USA",
        "province": "NY",
        "zip": "24233"
    },
    "email": "jdoe@email.com",
    "firstname": "John",
    "id": 2,
    "lastname": "Doe",
    "subscribed": true
}
```

### Update
Update customer data from the customer database. For now, it will only return a basic response and will not update a customer record.
```
PUT    /customers/2
```

#### Test for Update
```
PUT    /customers/123
Request
Body:{
	"firstname":"John",
	"lastname":"Doe",
	"email":"newemailaddress@email.com",
	"subscribed": true,
	"address": {
		"address1": "1 Second St",
		"address2":"1B",
		"city":"New York",
		"province":"NY",
		"country":"USA",
		"zip":"24233"
	}
}

Response
Expected Status: 200
Body:{
    "address": {
        "address1": "1 Second St",
        "address2": "1B",
        "city": "New York",
        "country": "USA",
        "province": "NY",
        "zip": "24233"
    },
    "email": "newemailaddress@email.com",
    "firstname": "John",
    "id": 2,
    "lastname": "Doe",
    "subscribed": true
}
```

### Delete
Delete customer data from the customer database.
```
DELETE    /customers/2
```

#### Test for Delete
```
DELETE    /customers/2

Excpected Status: 204
No content

```

### List All Customers
Get all customers in the customer database.
```
GET    /customers
```

#### Test for List All Customers
```
Get    /customers

Excpected Status: 200
Body:[
    {
        "address": {
            "address1": "3 Avenue Rd",
            "address2": "2F",
            "city": "New York",
            "country": "USA",
            "province": "NY",
            "zip": "24523"
        },
        "email": "sallym@email.com",
        "firstname": "Sally",
        "id": 1,
        "lastname": "May",
        "subscribed": false
    },
    {
        "address": {
            "address1": "1 Second St",
            "address2": "1B",
            "city": "New York",
            "country": "USA",
            "province": "NY",
            "zip": "24233"
        },
        "email": "newemailaddress@email.com",
        "firstname": "John",
        "id": 2,
        "lastname": "Doe",
        "subscribed": true
    }
]

```

### Unsubscribe (Action route)
Unsubscribe customer from communication.
```
PUT    /customers/2/unsubscribe
```

#### Test for Unsubscribe
```
PUT    /customers/2/unsubscribe

Excpected Status: 200
{
    "address": {
        "address1": "1 Second St",
        "address2": "1B",
        "city": "New York",
        "country": "USA",
        "province": "NY",
        "zip": "24233"
    },
    "email": "newemailaddress@email.com",
    "firstname": "John",
    "id": 2,
    "lastname": "Doe",
    "subscribed": false
}

```

### Read with Query
Read customer data from the customer database with query.
```
GET    /customers?lastname=Doe
```

#### Test for Read with Query string
```
GET    /customers?lastname=Doe

Excpected Status: 200
[
    {
        "address": {
            "address1": "1 Second St",
            "address2": "1B",
            "city": "New York",
            "country": "USA",
            "province": "NY",
            "zip": "24233"
        },
        "email": "newemailaddress@email.com",
        "firstname": "John",
        "id": 2,
        "lastname": "Doe",
        "subscribed": false
    }
]

```

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

The service will follow the RESTful structure. The collection will contain the CRUD methods.

### Create
Create a new customer in the customer database. For now, it will only return a basic response and will not create a customer.
```
POST    /customers
```

#### Test for Create
```
POST    /customers

Excpected Status: 200
{
	data: 'You executed the create route'
}
```

### Read
Read customer data from the customer database. For now, it will only return a basic response and will not return a customer record.
```
GET    /customers/123
```

#### Test for Create
```
GET    /customers/123

Excpected Status: 200
{
	data: 'You executed the read route'
}
```

### Update
Update customer data from the customer database. For now, it will only return a basic response and will not update a customer record.
```
PUT    /customers/123
```

#### Test for Create
```
PUT    /customers/123

Excpected Status: 200
{
	data: 'You executed the update route'
}
```

### Delete
Delete customer data from the customer database. For now, it will only return a basic response and will not delete a customer record.
```
DELETE    /customers/123
```

#### Test for Create
```
DELETE    /customers/123

Excpected Status: 200
{
	data: 'You executed the delete route'
}
```

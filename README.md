# rider-service
This is a basic python-based microservice aiming to aggregate and provide some statistics for riders and their rides.

## Tech stack
The following solutions are used within the service:
1. [MongoDB](https://www.mongodb.com) - for storing and accessing rides data
2. [Connexion](https://github.com/zalando/connexion) - framework on top of Flask automagically handling HTTP requests based on OpenAPI 2.0 Specification
3. [Pandas](https://pandas.pydata.org) - for data aggregation, basic statistics calculation and csv export
4. [Matplotlib](https://matplotlib.org) - for statistics plotting

## API description

Below one can find the API description however full API specification is available in [http://localhost:9090/ui/](http://localhost:9090/ui/) path providing Swagger Console UI

URI | METHOD | Description
--- | ------ | -----------
/store | POST | Stores ride information to the database.
/get | GET | Returns information on {size} last each rider's rides serialized in json.
/stats | GET | Returns csv with information on {size} last riders' rides sorted by Euclidian distance.
/chart | GET | Returns scatter plot with X - rides count and Y - ride distance variance for each rider.

## Set up

In order to get the service up and running the following steps should be performed:

1. Clone the repo
```
$ git clone https://github.com/zvezdysima/rider-service/
```

2. Run Mongo (from \data\db\ directory)
```
$ mongod
```
3. Install dependencies
```
$ pip install -r requirements.txt
```
4. Run service 
```
$ python app.py
```

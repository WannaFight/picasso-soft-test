# Picasso Soft Test

## Stack
Django 4.1 + DRF

## To run
Inside docker:
```shell
docker-compose up
```

Only postgres inside docker
```shell
docker-compose up --scale django=0
./manage.py runserver
```

## Contents
`requirements.txt` - dependencies
`debug.log` - log file for script parsing csv file


## DB Model
DB model created with help of [Django](police_reports/models.py)
SQL script to create table:
```postgresql
create table police_reports_crime
(
    id              bigserial
        constraint police_reports_crime_pkey
            primary key,
    crime_id        integer                  not null
        constraint police_reports_crime_crime_id_key
            unique
        constraint police_reports_crime_crime_id_check
            check (crime_id >= 0),
    crime_type      varchar(50)              not null,
    report_date     date                     not null,
    call_date       date                     not null,
    offense_date    date                     not null,
    call_time       varchar(5)               not null,
    call_date_time  timestamp with time zone not null,
    disposition     varchar(15)              not null,
    address         varchar(100)             not null,
    address_type    varchar(20)              not null,
    city            varchar(50)              not null,
    state           varchar(2)               not null,
    agency_id       integer                  not null
        constraint police_reports_crime_agency_id_check
            check (agency_id >= 0),
    common_location varchar(100)
);

alter table police_reports_crime
    owner to django;
```

## Parsing CSV
`./manage.py load_data_from_csv`
- progress in shell + logging to debug.log
- read csv by chunks (100 000 rows), because there are too many of them

## API
`GET :8000/api/crime_reports`
- supports `page` query param for pagination
- supports `date_from` and `date_to` query params for filtering by "Report Date"
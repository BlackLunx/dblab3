creating = '''
create extension if not exists dblink;
create or replace function create_database() returns void as $$
    begin
        if not exists (select from pg_database where datname = 'lab') then
            perform dblink_exec(
                'dbname=postgres user=postgres password=postgres',
                'create database lab with owner lab_user'
          );
        end if;
    end;
$$ language plpgsql;

create extension if not exists dblink;
create or replace function drop_database() returns void as $$
    begin
            perform dblink_exec(
                'dbname=postgres user=postgres password=postgres',
                'drop database if exists lab;'
            );
    end;
$$ language plpgsql;
'''
functions = '''
CREATE TABLE IF NOT EXISTS clothes
(
    ID INT,
    Brand varchar NOT NULL,
    size varchar(2) NOT NULL CHECK (size in ('XS', 'S', 'M', 'L', 'XL')),
    cost money NOT NULL
);

create index if not exists ID on clothes (ID);

CREATE TABLE IF NOT EXISTS location
(
    Brand varchar PRIMARY KEY NOT NULL,
    place varchar
);

create index if not exists Brand on location (Brand);

CREATE OR REPLACE FUNCTION generate_id()
returns TRIGGER
    AS $$
    DECLARE
        nextId INTEGER;
        BEGIN
            SELECT MAX(clothes.id)+1 INTO nextId FROM clothes;
            if nextId is NULL
            THEN
                nextId = 1;
            end if;
            new.id = nextId;
            return new;
        end;
    $$
LANGUAGE plpgsql;

drop trigger if exists genid on clothes;
CREATE TRIGGER genId before insert on clothes
    for row EXECUTE procedure generate_id();

CREATE OR REPLACE FUNCTION insert_clothes(_brand varchar, _size varchar(2), _cost money)
RETURNS void AS
    $$
    BEGIN
        INSERT into clothes(brand, size, cost) values(_brand, _size, _cost);
    end;
    $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION show_clothes(_id INTEGER, _brand varchar, _size varchar, _cost money)
RETURNS TABLE(ID INTEGER,
    Brand varchar,
    size varchar(2),
    cost money) as
    $$
    DECLARE
        lowerBound money;
        upperBound money;
        lowerBoundId INTEGER;
        upperBoundId INTEGER;
        BEGIN

            lowerBound = money(0);
            upperBound = money(100000000);
            lowerBoundId = -1;
            upperBoundId = 1e9;
            if _brand = '' then
                _brand = '%';
            end if;
            if _size = '' then
                _size = '%';
            end if;
            if _cost != money(-1) then
                lowerBound = _cost;
                upperBound = _cost;
            end if;
            if _id != -1 then
                lowerBoundId = _id;
                upperBoundId = _id;
            end if;
            return query (SELECT * FROM clothes
            WHERE clothes.brand SIMILAR TO _brand and clothes.size SIMILAR TO _size and lowerBound <= clothes.cost and
                  clothes.cost <= upperBound and lowerBoundId <= clothes.id and clothes.id <= upperBoundId);

        end;
    $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION count_clothes(_id INTEGER, _brand varchar, _size varchar, _cost money)
returns INTEGER as
    $$
    DECLARE
        lowerBound money;
        upperBound money;
        lowerBoundId INTEGER;
        upperBoundId INTEGER;
        BEGIN
            lowerBound = money(0);
            upperBound = money(100000000);
            lowerBoundId = -1;
            upperBoundId = 1e9;
            if _brand = '' then
                _brand = '%';
            end if;
            if _size = '' then
                _size = '%';
            end if;
            if _cost != money(-1) then
                lowerBound = _cost;
                upperBound = _cost;
            end if;
            if _id != -1 then
                lowerBoundId = _id;
                upperBoundId = _id;
            end if;
            return (select count(*) from clothes
            WHERE clothes.brand SIMILAR TO _brand and clothes.size SIMILAR TO _size and lowerBound <= clothes.cost and
                  clothes.cost <= upperBound and lowerBoundId <= clothes.id and clothes.id <= upperBoundId);

        end;

    $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_clothes(_id INTEGER, _brand varchar, _size varchar, _cost money)
returns void as
    $$
    DECLARE
         lowerBound money;
        upperBound money;
        lowerBoundId INTEGER;
        upperBoundId INTEGER;
        BEGIN
            lowerBound = money(0);
            upperBound = money(100000000);
            lowerBoundId = -1;
            upperBoundId = 1e9;
            if _brand = '' then
                _brand = '%';
            end if;
            if _size = '' then
                _size = '%';
            end if;
            if _cost != money(-1) then
                lowerBound = _cost;
                upperBound = _cost;
            end if;
            if _id != -1 then
                lowerBoundId = _id;
                upperBoundId = _id;
            end if;
            DELETE FROM clothes
            WHERE clothes.brand SIMILAR TO _brand and clothes.size SIMILAR TO _size and lowerBound <= clothes.cost and
                  clothes.cost <= upperBound and lowerBoundId <= clothes.id and clothes.id <= upperBoundId;

        end;

    $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_location(_brand varchar, _place varchar)
RETURNS void AS
    $$
    BEGIN
        INSERT into location(brand, place) values(_brand, _place);
    end;
    $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION show_location(_brand varchar, _place varchar)
RETURNS TABLE(
    Brand varchar,
    place varchar) as
    $$
    DECLARE
        BEGIN
            if _brand = '' then
                _brand = '%';
            end if;
            if _place = '' then
                _place = '%';
            end if;
            return query (SELECT * FROM location
            WHERE location.brand SIMILAR TO _brand and location.place SIMILAR TO _place);

        end;
    $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION count_location(_brand varchar, _place varchar)
returns INTEGER as
    $$
    DECLARE
        BEGIN
            if _brand = '' then
                _brand = '%';
            end if;
            if _place = '' then
                _place = '%';
            end if;
            return (SELECT count(*) FROM location
            WHERE location.brand SIMILAR TO _brand and location.place SIMILAR TO _place);

        end;

    $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_location(_brand varchar, _place varchar)
returns void as
    $$
    DECLARE
        BEGIN
            if _brand = '' then
                _brand = '%';
            end if;
            if _place = '' then
                _place = '%';
            end if;
            DELETE FROM location
            WHERE location.brand SIMILAR TO _brand and location.place SIMILAR TO _place;

        end;

    $$
LANGUAGE plpgsql;

create or replace function truncate_clothes() returns void as $$
    begin
        truncate clothes;
    end;
$$ language plpgsql;


create or replace function truncate_location() returns void as $$
    begin
        truncate location;
    end;
$$ language plpgsql;

'''
import os
import datetime
from typing import Callable, Any
from psycopg import connect
from pydantic import ValidationError, validate_call

try:

    @validate_call
    def fill_table(tbl_name: str, cursor: Any, insert_row: Callable):
        with open('datafiles/' + tbl_name + '.txt', 'r') as data_file:
            for line in data_file:
                if len(line) > 1:
                    insert_row(cursor, line)
        print('inserted ' + tbl_name)

    connection = connect("dbname=birddb user=postgres host=localhost password=postgres")
    with connection:
        with connection.cursor() as cursor:
            print('connected')

            @validate_call
            def insert_config_row(cursor: Any, line: str):
                tokens = line.split(';')
                name = tokens[0]
                description = tokens[1]
                value = tokens[2][0:-1]
                cursor.execute("""INSERT INTO config ("name", "description", "value") 
                                  VALUES (%s, %s, %s)""",
                               (name, description, value,))
            fill_table('config', cursor, insert_config_row)

            @validate_call
            def insert_region_row(cursor: Any, line: str):
                cursor.execute("""INSERT INTO region ("name") VALUES (%s)""", (line[0:-1],))
            fill_table('region', cursor, insert_region_row)

            @validate_call
            def insert_location_row(cursor: Any, line: str):
                tokens = line.split(';')
                location = tokens[0]
                region = tokens[1][0:-1]
                cursor.execute("""INSERT INTO location ("name", "region_id") VALUES (%s, 
                                  (SELECT region_id FROM region WHERE "name" = %s))""", 
                                  (location, region,))
            fill_table('location', cursor, insert_location_row)

            @validate_call
            def insert_category_row(cursor: Any, line: str):
                cursor.execute("""INSERT INTO category ("name") VALUES (%s)""", (line[0:-1],))
            fill_table('category', cursor, insert_category_row)

            @validate_call
            def insert_species_row(cursor: Any, line: str):
                tokens = line.split(';')
                species = tokens[0]
                category = tokens[1][0:-1]
                cursor.execute("""INSERT INTO species ("name", "category_id") VALUES (%s, 
                                  (SELECT category_id FROM category WHERE "name" = %s))""",
                               (species, category,))
            fill_table('species', cursor, insert_species_row)

            @validate_call
            def insert_book_row(cursor: Any, line: str):
                date = datetime.datetime.strptime(line[0:-1], '%Y-%m-%d').date()
                cursor.execute("""INSERT INTO book ("date") VALUES (%s)""", (date,))
            fill_table('book', cursor, insert_book_row)

            @validate_call
            def insert_observation_type__row(cursor: Any, line: str):
                cursor.execute("""INSERT INTO observation_type ("observation_type") VALUES (%s)""", 
                               (line[0:-1],))
            fill_table('observation_type', cursor, insert_observation_type__row)

    connection.close()

    print('done inserting')

except ValidationError as exc:
    print(exc)

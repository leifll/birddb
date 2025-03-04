import os
from datetime import datetime
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
                date = datetime.strptime(line[0:-1], '%Y-%m-%d').date()
                cursor.execute("""INSERT INTO book ("date") VALUES (%s)""", (date,))
            fill_table('book', cursor, insert_book_row)

            @validate_call
            def insert_observation_type__row(cursor: Any, line: str):
                cursor.execute("""INSERT INTO observation_type ("name") VALUES (%s)""", 
                               (line[0:-1],))
            fill_table('observation_type', cursor, insert_observation_type__row)

            @validate_call
            def insert_observation_and_photo_rows(cursor: Any, line: str):
                tokens = line.split(';')
                dir_name = tokens[0]
                location = tokens[1].lower()
                date = None
                if (len(tokens[2]) > 0):
                    date = datetime.strptime(tokens[2], '%y%m%d').date()
                file_name = tokens[3]
                species = tokens[4].lower()
                observation_type = tokens[5].lower()
                quantity = tokens[6]
                page_no = tokens[7]
                comment = tokens[8][0:-1]

                cursor.execute("""SELECT value FROM config WHERE name = %s""", ("photo-path-prefix",))
                file_path_prefix = cursor.fetchone()[0]

                if (len(dir_name) > 0):
                    cursor.execute("""INSERT INTO photo (file_path, time) VALUES (%s, %s)""", 
                                       (file_path_prefix + "/" + dir_name + "/" + file_name, date))

                cursor.execute("""INSERT INTO observation (date, location_id, species_id, photo_id,
                                  observation_type_id, quantity, comment) VALUES (%s,
                                  (SELECT location_id FROM location WHERE lower(name) = %s),
                                  (SELECT species_id FROM species WHERE lower(name) = %s),
                                  (SELECT photo_id FROM photo WHERE file_path ~ %s), 
                                  (SELECT observation_type_id FROM observation_type WHERE lower(name) = %s),
                                  NULLIF(%s, '')::int, NULLIF(%s, ''))""", 
                                  (date, location, species, ".*" + dir_name + "/" + file_name + "$", 
                                   observation_type, quantity, comment))
            fill_table('obs_and_photo', cursor, insert_observation_and_photo_rows)

    connection.close()

    print('done inserting')

except ValidationError as exc:
    print(exc)

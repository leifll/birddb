import os
import psycopg
import datetime

def fill_table(tbl_name, cursor, insert_row):
    with open('datafiles/' + tbl_name + '.txt', 'r') as data_file:
        for line in data_file:
            if len(line) > 1:
                insert_row(cursor, line)
    print('inserted ' + tbl_name)

connection =  psycopg.connect("dbname=birddb user=postgres host=localhost password=postgres")
with connection:
    with connection.cursor() as cursor:
        print('connected')

        def insert_config_row(cursor, line):
            tokens = line.split(';')
            name = tokens[0]
            description = tokens[1]
            value = tokens[2][0:-1]
            cursor.execute("""INSERT INTO config ("name", "description", "value") 
                              VALUES (%s, %s, %s)""",
                           (name, description, value,))
        fill_table('config', cursor, insert_config_row)

        def insert_region_row(cursor, line):
            cursor.execute("""INSERT INTO region ("name") VALUES (%s)""", (line[0:-1],))
        fill_table('region', cursor, insert_region_row)

        def insert_location_row(cursor, line):
            tokens = line.split(';')
            location = tokens[0]
            region = tokens[1][0:-1]
            cursor.execute("""INSERT INTO location ("name", "region_id") VALUES (%s, 
                              (SELECT region_id FROM region WHERE "name" = %s))""", 
                              (location, region,))
        fill_table('location', cursor, insert_location_row)

        def insert_category_row(cursor, line):
            cursor.execute("""INSERT INTO category ("name") VALUES (%s)""", (line[0:-1],))
        fill_table('category', cursor, insert_category_row)

        def insert_species_row(cursor, line):
            tokens = line.split(';')
            species = tokens[0]
            category = tokens[1][0:-1]
            cursor.execute("""INSERT INTO species ("name", "category_id") VALUES (%s, 
                              (SELECT category_id FROM category WHERE "name" = %s))""",
                              (species, category,))
        fill_table('species', cursor, insert_species_row)

        def insert_book_row(cursor, line):
            date = datetime.datetime.strptime(line[0:-1], '%Y-%m-%d').date()
            cursor.execute("""INSERT INTO book ("date") VALUES (%s)""", (date,))
        fill_table('book', cursor, insert_book_row)

connection.close()

print('done inserting')

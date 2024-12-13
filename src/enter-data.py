import os
import psycopg

def fill_table(tbl_name, cursor, insert_row):
    with open('datafiles/' + tbl_name + '.txt', 'r') as data_file:
        for line in data_file:
            if len(line) > 1:
                insert_row(cursor, line)
    print('inserted ' + tbl_name)

with psycopg.connect("dbname=birddb user=postgres host=localhost password=postgres") as connection:
    with connection.cursor() as cursor:
        print('connected')

        def insert_region_row(cursor, line):
            cursor.execute("""INSERT INTO region ("name") VALUES (%s)""", (line[0:-1],))
        fill_table('region', cursor, insert_region_row)

        def insert_location_row(cursor, line):
            tokens = line.split(';')
            location = tokens[0]
            region = tokens[1][0:-1]
            cursor.execute("""INSERT INTO location ("name", "region_id") VALUES (%s, 
                              (select region_id from region where "name" = %s))""", 
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
                              (select category_id from category where "name" = %s))""",
                              (species, category,))
        fill_table('species', cursor, insert_species_row)

    connection.commit()

print('done inserting')

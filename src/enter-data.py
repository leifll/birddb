import os
import psycopg

def fill_table(tbl_name, connection, insert_row):
    with open('datafiles/' + tbl_name + '.txt', 'r') as data_file:
        for line in data_file:
            if len(line) > 1:
                insert_row(connection, line)
    print('inserted ' + tbl_name)

with psycopg.connect("dbname=birddb user=postgres host=localhost password=postgres") as connection:
    print('connected')

    def insert_location_row(connection, line):
        connection.execute('INSERT INTO location ("name") VALUES (\'' + line[0:-1].strip() + '\')')
    fill_table('location', connection, insert_location_row)

    def insert_category_row(connection, line):
        connection.execute('INSERT INTO category ("name") VALUES (\'' + line[0:-1] + '\')')
    fill_table('category', connection, insert_category_row)

    def insert_species_row(connection, line):
        tokens = line.split(';')
        species = tokens[0]
        category = tokens[1][0:-1]
        connection.execute('INSERT INTO species ("name", "category_id") VALUES (\'' + species + 
                         '\', (select category_id from category where "name" = \'' + category + '\'))')
    fill_table('species', connection, insert_species_row)

    print('done inserting')

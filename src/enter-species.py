import os
import psycopg

with psycopg.connect("dbname=birddb user=postgres host=localhost password=postgres") as connection:
  print('connected')

  with open('datafiles/species.txt', 'r') as dataFile:
    for line in dataFile:
      if len(line) > 1:
        tokens = line.split(';')
        species = tokens[0]
        category = tokens[1][0:-1]
        connection.execute('INSERT INTO species ("name", "category_id") VALUES (\'' + species + 
                         '\', (select category_id from category where "name" = \'' + category + '\'))')
        print('inserted species:' + species + ', category:' + category)

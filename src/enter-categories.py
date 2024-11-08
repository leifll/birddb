import os
import psycopg

with psycopg.connect("dbname=birddb user=postgres host=localhost password=postgres") as connection:
  print('connected')

  with open('datafiles/categories.txt', 'r') as dataFile:

    for line in dataFile:
      if len(line) > 1:
        connection.execute('INSERT INTO category ("name") VALUES (\'' + line[0:-1] + '\')')
        print(line[0:-1] + " inserted")

print('done')

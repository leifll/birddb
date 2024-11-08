import os
import psycopg

with psycopg.connect("dbname=birddb user=postgres host=localhost password=postgres") as connection:
  print('connected')

  with open('datafiles/locations-unique.txt', 'r') as dataFile:

    for line in dataFile:
      if len(line) > 1:
        connection.execute('INSERT INTO location ("name") VALUES (\'' + line[0:-1].strip() + '\')')
        print(line[0:-1] + " inserted")

print('done')

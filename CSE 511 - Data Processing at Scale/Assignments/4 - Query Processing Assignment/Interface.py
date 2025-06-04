#!/usr/bin/python3
#Shachi Shah
# Query Processing Assignment

import psycopg2
import os
import sys

DATABASE_NAME='dds_assignment'
RATINGS_TABLE_NAME='ratings'
RANGE_TABLE_PREFIX='range_part'
RROBIN_TABLE_PREFIX='rrobin_part'
RANGE_QUERY_OUTPUT_FILE='RangeQueryOut.txt'
PONT_QUERY_OUTPUT_FILE='PointQueryOut.txt'
RANGE_RATINGS_METADATA_TABLE ='rangeratingsmetadata'
RROBIN_RATINGS_METADATA_TABLE='roundrobinratingsmetadata'

# Do not close the connection inside this file
def RangeQuery(ratingsTableName, ratingMinValue, ratingMaxValue, openconnection):
    cursor = openconnection.cursor()
    results = []

    # Get all range partition tables
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'range_part%'")
    range_tables = [row[0] for row in cursor.fetchall()]

    for partition_name in range_tables:
        cursor.execute(f"SELECT userid, movieid, rating FROM {partition_name} WHERE rating >= %s AND rating <= %s",
                       (ratingMinValue, ratingMaxValue))
        for row in cursor.fetchall():
            results.append((partition_name, *row))

    # Get all round robin partition tables
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'rrobin_part%'")
    rr_tables = [row[0] for row in cursor.fetchall()]

    for partition_name in rr_tables:
        cursor.execute(f"SELECT userid, movieid, rating FROM {partition_name} WHERE rating >= %s AND rating <= %s",
                       (ratingMinValue, ratingMaxValue))
        for row in cursor.fetchall():
            results.append((partition_name, *row))

    writeToFile(RANGE_QUERY_OUTPUT_FILE, results)
    cursor.close()


def PointQuery(ratingsTableName, ratingValue, openconnection):
    cursor = openconnection.cursor()
    results = []

    # Get all range partition tables
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'range_part%'")
    range_tables = [row[0] for row in cursor.fetchall()]

    for partition_name in range_tables:
        cursor.execute(f"SELECT userid, movieid, rating FROM {partition_name} WHERE rating = %s", (ratingValue,))
        for row in cursor.fetchall():
            results.append((partition_name, *row))

    # Get all round robin partition tables
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'rrobin_part%'")
    rr_tables = [row[0] for row in cursor.fetchall()]

    for partition_name in rr_tables:
        cursor.execute(f"SELECT userid, movieid, rating FROM {partition_name} WHERE rating = %s", (ratingValue,))
        for row in cursor.fetchall():
            results.append((partition_name, *row))

    writeToFile(PONT_QUERY_OUTPUT_FILE, results)
    cursor.close()



def writeToFile(filename, rows):
    with open(filename, 'w') as f:
        for line in rows:
            f.write(','.join(str(s) for s in line))
            f.write('\n')

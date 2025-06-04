# Shachi Shah
# Data Fragmentation Assignment

#!/usr/bin/python3
#
# Interface for the assignement
#

import psycopg2

def getOpenConnection(user='postgres', password='1234', dbname='postgres'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")


# Load data from ratings file into PostgreSQL table
def loadRatings(ratingstablename, ratingsfilepath, openconnection):
    cursor = openconnection.cursor()

    # Drop the table if it already exists
    cursor.execute(f"DROP TABLE IF EXISTS {ratingstablename}")

    # Create the ratings table
    cursor.execute(f"""
        CREATE TABLE {ratingstablename} (
            userid INT,
            movieid INT,
            rating FLOAT
        );
    """)

    # Read and insert data
    with open(ratingsfilepath, 'r') as file:
        for line in file:
            parts = line.strip().split("::")
            if len(parts) < 3:
                continue  # Skip bad lines
            userid, movieid, rating = int(parts[0]), int(parts[1]), float(parts[2])
            cursor.execute(
                f"INSERT INTO {ratingstablename} (userid, movieid, rating) VALUES (%s, %s, %s)",
                (userid, movieid, rating)
            )

    openconnection.commit()
    cursor.close()

# Partition the base table into N range-based partitions
def rangePartition(ratingstablename, numberofpartitions, openconnection):
    cursor = openconnection.cursor()

    # Drop old range partitions if they exist
    for i in range(numberofpartitions):
        cursor.execute(f"DROP TABLE IF EXISTS range_part{i}")

    # Calculate interval size
    interval = 5.0 / numberofpartitions

    # Create each range partition table and insert rows
    for i in range(numberofpartitions):
        start = i * interval
        end = start + interval

        cursor.execute(f"""
            CREATE TABLE range_part{i} (
                userid INT,
                movieid INT,
                rating FLOAT
            );
        """)

        if i == 0:
            # Include start and end: [0, end]
            cursor.execute(f"""
                INSERT INTO range_part{i}
                SELECT * FROM {ratingstablename}
                WHERE rating >= {start} AND rating <= {end}
            """)
        else:
            # Exclusive start, inclusive end: (start, end]
            cursor.execute(f"""
                INSERT INTO range_part{i}
                SELECT * FROM {ratingstablename}
                WHERE rating > {start} AND rating <= {end}
            """)

    openconnection.commit()
    cursor.close()

# Partition the base table into N round-robin partitions
def roundRobinPartition(ratingstablename, numberofpartitions, openconnection):
    cursor = openconnection.cursor()

    # Drop old round robin partitions
    for i in range(numberofpartitions):
        cursor.execute(f"DROP TABLE IF EXISTS rrobin_part{i}")

    # Create new rrobin_part tables
    for i in range(numberofpartitions):
        cursor.execute(f"""
            CREATE TABLE rrobin_part{i} (
                userid INT,
                movieid INT,
                rating FLOAT
            );
        """)

    # Add row numbers to rows in base table
    cursor.execute(f"""
        SELECT userid, movieid, rating,
               ROW_NUMBER() OVER () as rownum
        FROM {ratingstablename}
    """)

    rows = cursor.fetchall()

    for row in rows:
        userid, movieid, rating, rownum = row
        target_partition = (rownum - 1) % numberofpartitions
        cursor.execute(
            f"INSERT INTO rrobin_part{target_partition} (userid, movieid, rating) VALUES (%s, %s, %s)",
            (userid, movieid, rating)
        )

    openconnection.commit()
    cursor.close()

# Insert a new row into the appropriate round-robin partition
def roundrobininsert(ratingstablename, userid, itemid, rating, openconnection):
    cursor = openconnection.cursor()

    # Insert into base ratings table
    cursor.execute(
        f"INSERT INTO {ratingstablename} (userid, movieid, rating) VALUES (%s, %s, %s)",
        (userid, itemid, rating)
    )

    # Check if metadata table exists
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'rrobin_metadata'
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute("CREATE TABLE rrobin_metadata (last_used INT)")
        cursor.execute("INSERT INTO rrobin_metadata VALUES (0)")
        last_used = 0
    else:
        cursor.execute("SELECT last_used FROM rrobin_metadata")
        last_used = cursor.fetchone()[0]

    # Count how many round-robin partitions exist
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name LIKE 'rrobin_part%'")
    num_partitions = cursor.fetchone()[0]

    # Insert into the correct partition
    target_partition = last_used % num_partitions
    cursor.execute(
        f"INSERT INTO rrobin_part{target_partition} (userid, movieid, rating) VALUES (%s, %s, %s)",
        (userid, itemid, rating)
    )

    # Update metadata
    cursor.execute("UPDATE rrobin_metadata SET last_used = %s", (last_used + 1,))

    openconnection.commit()
    cursor.close()


# Insert a new row into the correct range partition
def rangeinsert(ratingstablename, userid, itemid, rating, openconnection):
    cursor = openconnection.cursor()

    # Insert into base ratings table
    cursor.execute(
        f"INSERT INTO {ratingstablename} (userid, movieid, rating) VALUES (%s, %s, %s)",
        (userid, itemid, rating)
    )

    # Get number of partitions by counting range_part tables
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name LIKE 'range_part%'")
    num_partitions = int(cursor.fetchone()[0])

    interval = 5.0 / num_partitions

    # Determine which partition to insert into
    partition = 0
    for i in range(num_partitions):
        lower = i * interval
        upper = lower + interval
        if i == 0:
            if lower <= rating <= upper:
                partition = i
                break
        else:
            if lower < rating <= upper:
                partition = i
                break

    # Insert into the right partition
    cursor.execute(
        f"INSERT INTO range_part{partition} (userid, movieid, rating) VALUES (%s, %s, %s)",
        (userid, itemid, rating)
    )

    openconnection.commit()
    cursor.close()

# Create a new database if it doesn't exist
def createDB(dbname='dds_assignment'):
    """
    We create a DB by connecting to the default user and database of Postgres
    The function first checks if an existing database exists for a given name, else creates it.
    :return:None
    """
    # Connect to the default database
    con = getOpenConnection(dbname='postgres')
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    # Check if an existing database with the same name exists
    cur.execute('SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname=\'%s\'' % (dbname,))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute('CREATE DATABASE %s' % (dbname,))  # Create the database
    else:
        print('A database named {0} already exists'.format(dbname))

    # Clean up
    cur.close()
    con.close()

# Drop specific or all tables
def deletepartitionsandexit(openconnection):
    cur = openconnection.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    l = []
    for row in cur:
        l.append(row[0])
    for tablename in l:
        cur.execute("drop table if exists {0} CASCADE".format(tablename))

    cur.close()

def deleteTables(ratingstablename, openconnection):
    try:
        cursor = openconnection.cursor()
        if ratingstablename.upper() == 'ALL':
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            for table_name in tables:
                cursor.execute('DROP TABLE %s CASCADE' % (table_name[0]))
        else:
            cursor.execute('DROP TABLE %s CASCADE' % (ratingstablename))
        openconnection.commit()
    except psycopg2.DatabaseError as e:
        if openconnection:
            openconnection.rollback()
        print('Error %s' % e)
    except IOError as e:
        if openconnection:
            openconnection.rollback()
        print('Error %s' % e)
    finally:
        if cursor:
            cursor.close()
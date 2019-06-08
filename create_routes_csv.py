import psycopg2
import csv
import os

try:
    connection = psycopg2.connect(user = "postgres",
                                password = "admin",
                                host = "localhost",
                                port = "5432",
                                database = "milan-gtfs")
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    # print ( connection.get_dsn_parameters(),"\n")

    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

    # Get list of stops for each transportation line
    # NOTE: splitting lines (e.g. Bisceglie-Rho Fiera) are added in manually later outside this script

    where = {}
    result = {}
    where["tram"] = "where route_id like 'T%'"
    where["metro"] = "where route_id like 'M%'"
    where["bus"] = "where route_id like 'B%'"

    for key, w in where.items():
        cursor.execute('''
        select route_id, stop_name, stop_id, stop_sequence, stop_lat, stop_lon, shape_id
        from
        (
            select distinct on (route_id) route_id, trip_id, shape_id
            from 
            (
                select route_id, trip_id, count(trip_id) as count, shape_id
                from trips
                join stop_times using (trip_id)
                group by route_id, trip_id
                order by count
            ) as x
            order by route_id desc
        ) as y
        join stop_times using (trip_id)
        join stops using (stop_id) ''' + w +
        ''' order by route_id desc, stop_sequence::int
        ''')

        result[key] = cursor.fetchall()
        # Extract the column names
        col_names = []
        for e in cursor.description:
            col_names.append(e[0])

        result[key] = [col_names] + result[key]

    # Write CSV

    if not os.path.exists("data/"):
        os.makedirs("data/")
        os.makedirs("data/csv")

    for key, table in result.items():

        with open("data/csv/" + key + ".csv", mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in table:
                writer.writerow(row)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


DROP TABLE IF EXISTS agency;
CREATE TABLE agency (
    agency_id text,
    agency_name text,
    agency_url text,
    agency_timezone text,
	agency_lang text,
	agency_phone text,
	agency_fare_url text,
	primary key(agency_id)
);

DROP TABLE IF EXISTS calendar;
CREATE TABLE calendar (
    service_id text,
	monday text,
	tuesday text,
	wednesday text,
	thursday text,
	friday text,
	saturday text,
	sunday text,
	start_date text,	
	end_date text
);

CREATE INDEX ON calendar (service_id);

DROP TABLE IF EXISTS calendar_dates;
CREATE TABLE calendar_dates (
    service_id text,
    date text,
    exception_type text
);

CREATE INDEX ON calendar_dates (service_id);
CREATE INDEX ON calendar_dates (exception_type);

DROP TABLE IF EXISTS routes;
CREATE TABLE routes (
    route_id text,
	agency_id text,
	route_short_name text,
	route_long_name text,
	route_type text,
	route_desc text,
	route_url text,
	route_color text,
	route_text_color text,
	x_accessibilita_linea text,
	x_ordinamento_linea text,
	primary key(route_id)
);

CREATE INDEX ON routes (agency_id);
CREATE INDEX ON routes (route_type);

DROP TABLE IF EXISTS stop_times;
CREATE TABLE stop_times (
    trip_id text,
	arrival_time text,
	departure_time text,
	stop_id text,
	stop_sequence text,
	stop_headsign text,
	pickup_type text,
	drop_off_type text,
	shape_dist_traveled text
);

CREATE INDEX ON stop_times (trip_id);
CREATE INDEX ON stop_times (stop_id);
CREATE INDEX ON stop_times (stop_sequence);
CREATE INDEX ON stop_times (pickup_type);
CREATE INDEX ON stop_times (drop_off_type);

DROP TABLE IF EXISTS stops;
CREATE TABLE stops (
    stop_id text,
	stop_code text,
	stop_name text,
	stop_desc text,
	stop_lat float,
	stop_lon float,
	zone_id text,
	stop_url text,
	location_type text,
	parent_station text,
	stop_timezone text,
	wheelchair_boarding text,
	primary key(stop_id)
);

CREATE INDEX ON stops (zone_id);
CREATE INDEX ON stops (stop_lat);
CREATE INDEX ON stops (stop_lon);

DROP TABLE IF EXISTS trips;
CREATE TABLE trips (
    route_id text,
	service_id text,
	trip_id text,
	trip_headsign text,
	trip_short_name text,
	direction_id text,
	block_id text,
	shape_id text,
	wheelchair_accessible text,
	x_trip_desc text,
	x_shape_id_order text,
	primary key(trip_id)
);

CREATE INDEX ON trips (route_id);
CREATE INDEX ON trips (service_id);
CREATE INDEX ON trips (direction_id);
CREATE INDEX ON trips (block_id);

COPY agency FROM '/tmp/dataset/agency.txt' delimiter ',' CSV HEADER;
COPY calendar FROM '/tmp/dataset/calendar.txt' delimiter ',' CSV HEADER;
COPY calendar_dates  from '/tmp/dataset/calendar_dates.txt' delimiter ',' CSV HEADER;
COPY routes  from '/tmp/dataset/routes.txt' delimiter ',' CSV HEADER;
COPY stop_times  from '/tmp/dataset/stop_times.txt' delimiter ',' CSV HEADER;
COPY stops  from '/tmp/dataset/stops.txt' delimiter ',' CSV HEADER;
COPY trips  from '/tmp/dataset/trips.txt' delimiter ',' CSV HEADER;

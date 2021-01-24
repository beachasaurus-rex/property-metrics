from sqlite3 import connect

location_schema = \
'''
create table if not exists location (
    property_id text,
    management_type text,
    condo_name text,
    street_address text,
    unit text,
    municipality text,
    zip_code text,
    city text,
    county text,
    state text,
    latitude real,
    longitude real,
    work_distance real
)
'''
status_schema = \
'''
create table if not exists status (
    record_id text,
    property_id text,
    lookup_date text,
    sell_date text,
    days_on_market integer,
    listing_status text,
    price real,
    condo_fee real,
    property_tax real,
    tax_year text,
    listing_office text
)
'''
pets_schema = \
'''
create table if not exists pets (
    property_id text,
    pets_are_allowed integer,
    cat_limit integer,
    dog_limit integer,
    other text
)
'''
pet_restrictions_schema = \
'''
create table if not exists pet_restrictions (
    property_id text,
    pet_type text,
    restriction text
)
'''
inclusions_schema = \
'''
create table if not exists inclusions (
    property_id text,
    inclusion_type text,
    item text
)
'''
utilities_schema = \
'''
create table if not exists utilities (
    property_id text,
    water_source text,
    sewer_outlet text
)
'''
heating_methods_schema = \
'''
create table if not exists heating_methods (
    property_id text,
    heating_method text
)
'''
cooling_methods_schema = \
'''
create table if not exists cooling_methods (
    property_id text,
    cooling_method text
)
'''
heating_fuels_schema = \
'''
create table if not exists heating_fuels (
    property_id text,
    heating_fuel text
)
'''
parking_schema = \
'''
create table if not exists parking (
    property_id text,
    location text,
    count integer
)
'''
rooms_schema = \
'''
create table if not exists rooms (
    property_id text,
    zoning_type text,
    year_built text,
    exterior text,
    property_type text,
    floor_count integer,
    room_count integer,
    est_sq_ft real,
    has_basement integer,
    basement_type text,
    bed_count integer,
    full_bath_count integer,
    half_bath_count integer,
    garage_spaces integer,
    garage_type text
)
'''
reference_schema = \
'''
create table if not exists reference (
    property_id text,
    reference_type text,
    reference text
)
'''
isp_schema = \
'''
create table if not exists ISP (
    property_id text,
    zip_code text,
    isp text,
    connection text,
    reference_base_url text
)
'''
def setup_schema(dbpath: str):
    schemas = [
        location_schema,
        status_schema,
        pets_schema,
        pet_restrictions_schema,
        inclusions_schema,
        utilities_schema,
        heating_methods_schema,
        cooling_methods_schema,
        heating_fuels_schema,
        parking_schema,
        rooms_schema,
        reference_schema,
        isp_schema
    ]
    for schema in schemas:
        con = connect(dbpath)
        con.execute(schema)
        con.close()

def drop_schema(dbpath: str):
    con = connect(dbpath)
    curs = con.execute("select name from sqlite_master where type = 'table';")
    records = curs.fetchall()
    for record in records:
        curs.execute(f"drop table {record[0]}")
    con.commit()
    con.close()
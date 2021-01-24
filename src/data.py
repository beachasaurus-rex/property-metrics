from enum import Enum
from datetime import date
from sqlite3 import connect

class ListingStatus(Enum):
    S = 0
    A = 1
    AWO = 2
    E = 3

class GarageType(Enum):
    detached = 0
    attached = 1

class Status:
    def __init__(self,
        record_id: str,
        lookup_date: str,
        sell_date: str,
        days_on_market: int,
        listing_status: str,
        price: float,
        condo_fee: float,
        property_tax: float,
        tax_year: str,
        listing_office: str
    ):
        self.record_id = record_id
        self.lookup_date = date.fromisoformat(lookup_date)
        if sell_date is None:
            self.sell_date = sell_date
        else:
            self.sell_date = date.fromisoformat(sell_date)
        self.days_on_market = days_on_market
        self.listing_status = ListingStatus[listing_status]
        self.price = price
        self.condo_fee = condo_fee
        self.property_tax = property_tax
        self.tax_year = tax_year
        self.listing_office = listing_office

class Location:
    def __init__(self,
        management_type: str,
        condo_name: str,
        street_address: str,
        unit: str,
        municipality: str,
        zip_code: str,
        city: str,
        county: str,
        state: str,
        latitude: float,
        longitude: float,
        work_distance: float
    ):
        self.management_type = management_type,
        self.condo_name = condo_name,
        self.street_address = street_address,
        self.unit = unit,
        self.municipality = municipality,
        self.zip_code = zip_code,
        self.city = city,
        self.county = county,
        self.state = state,
        self.latitude = latitude,
        self.longitude = longitude,
        self.work_distance = work_distance
        if unit is None:
            if condo_name is None:
                self.total_address = f"{street_address} {city}, {state} {zip_code}"
            else:
                self.total_address = f"{street_address} {condo_name} {city}, {state} {zip_code}"
        else:
            if condo_name is None:
                self.total_address = f"{street_address} {unit} {city}, {state} {zip_code}"
            else:
                self.total_address = f"{street_address} {unit} {condo_name} {city}, {state} {zip_code}"

class PetRestriction:
    def __init__(self,
        pet_type: str,
        restriction: str
    ):
        self.pet_type = pet_type,
        self.restriction = restriction

class PetDetails:
    def __init__(self,
        pets_are_allowed: int,
        cat_limit: int,
        dog_limit: int,
        other: str,
        restrictions: list
    ):
        if len(restrictions) > 0:
            if not(type(restrictions[0]) is PetRestriction) \
            and not(restrictions[0] is None):
                raise TypeError("'restrictions' must be a list of PetRestriction objects")
        self.pets_are_allowed = bool(pets_are_allowed)
        self.cat_limit = cat_limit
        self.dog_limit = dog_limit
        self.other = other
        self.restrictions = restrictions

class Inclusion:
    def __init__(self,
        inclusion_type: str,
        item: str
    ):
        self.inclusion_type = inclusion_type
        self.item = item

class UtilityDetails:
    def __init__(self,
        water_source: str,
        sewer_outlet: str,
        heating_methods: list,
        cooling_methods: list,
        heating_fuels: list
    ):
        self.water_source = water_source
        self.sewer_outlet = sewer_outlet
        self.heating_methods = heating_methods
        self.cooling_methods = cooling_methods
        self.heating_fuels = heating_fuels

class RoomDetails:
    def __init__(self,
        zoning_type: str,
        year_built: str,
        exterior_materials: str,
        property_type: str,
        floor_count: int,
        room_count: int,
        est_sq_ft: float,
        has_basement: int,
        basement_type: str,
        bed_count: int,
        full_bath_count: int,
        half_bath_count: int,
        garage_spaces: int,
        garage_type: str
    ):
        self.zoning_type = zoning_type
        self.year_built = year_built
        self.exterior_materials = exterior_materials.split(';')
        self.property_type = property_type
        self.floor_count = floor_count
        self.room_count = room_count
        self.est_sq_ft = est_sq_ft
        self.has_basement = bool(has_basement)
        self.basement_type = basement_type
        self.bed_count = bed_count
        self.full_bath_count = full_bath_count
        self.half_bath_count = half_bath_count
        self.garage_spaces = garage_spaces
        self.garage_type = GarageType[garage_type]

class Reference:
    def __init__(self,
        reference_type: str,
        item: str
    ):
        self.reference_type = reference_type
        self.item = item

class InternetProvider:
    def __init__(self,
        name: str,
        connection_type: str,
        base_url_ref: str
    ):
        self.name = name,
        self.connection_type = connection_type
        self.base_url_ref = base_url_ref

class Property:
    def __init__(self,
        statuses: list,
        location: Location,
        pet_details: PetDetails,
        inclusions: list,
        utility_details: UtilityDetails,
        room_details: RoomDetails,
        reference: Reference,
        isps: list
    ):
        if not(type(statuses[0]) is Status):
            raise TypeError("'statuses' must be a list of Status objects")
        if not(type(inclusions[0]) is Inclusion) \
        and not(inclusions[0] is None):
            raise TypeError("'inclusions' must be a list of Inclusion objects")
        if not(type(isps[0]) is InternetProvider) \
        and not(isps[0] is None):
            raise TypeError("'isps' must be a list of InternetProvider objects")
        self.statuses = statuses
        self.location = location
        self.pet_details = pet_details
        self.inclusions = inclusions
        self.utility_details = utility_details
        self.room_details = room_details
        self.reference = reference
        self.isps = isps

def order_data(dbpath: str):
    #get all property ids
    con = connect(dbpath)
    curs = con.execute("select property_id from location")
    records = curs.fetchall()
    prop_ids = [rec[0] for rec in records]
    con.close()

    props = []
    #get all data based on property ids & pack into data structures
    for prop_id in prop_ids:
        con = connect(dbpath)
        curs = con.execute("select * from status where property_id = ?", (prop_id,))
        raw_statuses = curs.fetchall()
        curs = con.execute("select * from location where property_id = ?", (prop_id,))
        raw_location = curs.fetchall()
        raw_location = raw_location[0]
        curs = con.execute("select * from pets where property_id = ?", (prop_id,))
        raw_pets = curs.fetchall()
        raw_pets = raw_pets[0]
        curs = con.execute("select * from pet_restrictions where property_id = ?", (prop_id,))
        raw_pet_restrictions = curs.fetchall()
        curs = con.execute("select * from inclusions where property_id = ?", (prop_id,))
        raw_inclusions = curs.fetchall()
        curs = con.execute("select * from utilities where property_id = ?", (prop_id,))
        raw_utilities = curs.fetchall()
        if len(raw_utilities) > 0:
            raw_utilities = raw_utilities[0]
        curs = con.execute("select * from heating_methods where property_id = ?", (prop_id,))
        raw_heating_methods = curs.fetchall()
        curs = con.execute("select * from cooling_methods where property_id = ?", (prop_id,))
        raw_cooling_methods = curs.fetchall()
        curs = con.execute("select * from heating_fuels where property_id = ?", (prop_id,))
        raw_heating_fuels = curs.fetchall()
        curs = con.execute("select * from rooms where property_id = ?", (prop_id,))
        raw_rooms = curs.fetchall()
        raw_rooms = raw_rooms[0]
        curs = con.execute("select * from reference where property_id = ?", (prop_id,))
        raw_ref = curs.fetchall()
        raw_ref = raw_ref[0]
        curs = con.execute("select * from ISP where property_id = ?", (prop_id,))
        raw_isps = curs.fetchall()
        con.close()

        #build the data structures
        statuses = []
        for raw_status in raw_statuses:
            status = Status(
                raw_status[1],
                raw_status[2],
                raw_status[3],
                raw_status[4],
                raw_status[5],
                raw_status[6],
                raw_status[7],
                raw_status[8],
                raw_status[9],
                raw_status[10]
            )
            statuses.append(status)

        location = Location(
            raw_location[1],
            raw_location[2],
            raw_location[3],
            raw_location[4],
            raw_location[5],
            raw_location[6],
            raw_location[7],
            raw_location[8],
            raw_location[9],
            raw_location[10],
            raw_location[11],
            raw_location[12],
        )

        pet_restrictions = []
        for raw_restr in raw_pet_restrictions:
            restr = PetRestriction(
                raw_restr[1],
                raw_restr[2]
            )
            pet_restrictions.append(restr)
        pet_details = PetDetails(
            raw_pets[1],
            raw_pets[2],
            raw_pets[3],
            raw_pets[4],
            pet_restrictions
        )

        inclusions = []
        for raw_inc in raw_inclusions:
            inc = Inclusion(
                raw_inc[1],
                raw_inc[2]
            )
            inclusions.append(inc)
        
        heating_methods = [hm[1] for hm in raw_heating_methods]
        cooling_methods = [cm[1] for cm in raw_cooling_methods]
        heating_fuels = [hf[1] for hf in raw_heating_fuels]
        if len(raw_utilities) > 0:
            utility_details = UtilityDetails(
                raw_utilities[1],
                raw_utilities[2],
                heating_methods,
                cooling_methods,
                heating_fuels
            )
        else:
            utility_details = UtilityDetails(
                None,
                None,
                heating_methods,
                cooling_methods,
                heating_fuels
            )

        room_details = RoomDetails(
            raw_rooms[1],
            raw_rooms[2],
            raw_rooms[3],
            raw_rooms[4],
            raw_rooms[5],
            raw_rooms[6],
            raw_rooms[7],
            raw_rooms[8],
            raw_rooms[9],
            raw_rooms[10],
            raw_rooms[11],
            raw_rooms[12],
            raw_rooms[13],
            raw_rooms[14]
        )

        reference = Reference(
            raw_ref[1],
            raw_ref[2]
        )

        isps = []
        for raw_isp in raw_isps:
            isp = InternetProvider(
                raw_isp[2],
                raw_isp[3],
                raw_isp[4]
            )
            isps.append(isp)
        
        prop = Property(
            statuses,
            location,
            pet_details,
            inclusions,
            utility_details,
            room_details,
            reference,
            isps
        )
        props.append(prop)
    return props
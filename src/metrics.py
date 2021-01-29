from data import (
    Property,
    UtilityInclusions
)

#things to answer:
#   1. what will i be paying each month in "rent"?
#   2. what is the property's relative scoring for us?

def calculate_monthly_expenses(prop: Property):
    status = prop.current_status
    #an assumed interest rate
    interest_rate = 0.05

    #estimate monthly utility bill
    #conservative estimate for monthly utility usage
    monthly_utility_bill = 400
    has_water_inclusion = False
    has_elec_inclusion = False
    has_nat_gas_inclusion = False
    has_hot_water_inclusion = False
    has_sewer_inclusion = False
    for inc in prop.inclusions:
        if inc.item == UtilityInclusions.water.name:
            has_water_inclusion = True
        if inc.item == UtilityInclusions.electricity.name:
            has_elec_inclusion = True
        if inc.item.replace(" ", "_") == UtilityInclusions.natural_gas.name:            
            has_nat_gas_inclusion = True
        if inc.item.replace(" ", "_") == UtilityInclusions.hot_water.name:
            has_hot_water_inclusion = True
        if inc.item == UtilityInclusions.sewer.name:
            has_sewer_inclusion = True
    utility_bill_frac = monthly_utility_bill / 4
    if has_water_inclusion:
        # print(f"has water inclusion = {has_water_inclusion}")
        monthly_utility_bill -= utility_bill_frac
    if has_elec_inclusion:
        # print(f"has elec inclusion = {has_elec_inclusion}")
        monthly_utility_bill -= utility_bill_frac
    if has_nat_gas_inclusion:
        # print(f"has NG inclusion = {has_nat_gas_inclusion}")
        monthly_utility_bill -= utility_bill_frac
    if has_hot_water_inclusion:
        # print(f"has hot water inclusion = {has_hot_water_inclusion}")
        monthly_utility_bill -= utility_bill_frac
    if has_sewer_inclusion:
        # print(f"has sewer inclusion = {has_sewer_inclusion}")
        monthly_utility_bill -= monthly_utility_bill / 8

    #estimate monthly property tax payment
    monthly_property_tax = 0
    if status.property_tax is None:
        monthly_property_tax = status.price * 0.01991 / 12
    else:
        monthly_property_tax = status.property_tax / 12
    monthly_mortgage = status.price * (1 + interest_rate) / (12*30)

    prop.metrics.monthly_utility_bill = monthly_utility_bill
    prop.metrics.monthly_property_tax = monthly_property_tax
    prop.metrics.monthly_mortgage = monthly_mortgage
    prop.metrics.monthly_condo_fee = status.condo_fee

def calculate_property_score(prop: Property,
    mean_monthly_expense: float,
    mean_work_distance: float,
    mean_area: float,
    mean_bed_count: float,
    mean_full_bath_count: float,
    mean_half_bath_count: float
):
    #weights
    laundry_weight = 10
    expense_weight = 1.9
    range_weight = 1.9
    fridge_weight = 1.9
    water_softener_weight = 1.8
    trash_collection_weight = 1.7
    bath_weight = 1.7
    area_weight = 1.6
    bed_weight = 1.6
    gas_fireplace_weight = 1.55
    wood_fireplace_weight = 1.5
    work_distance_weight = 1.5
    pet_weight = 1.3

    #calculations
    expenses_score = expense_weight * mean_monthly_expense / prop.metrics.get_monthly_expenses()
    work_distance_score = work_distance_weight * mean_work_distance / prop.location.work_distance
    area_score = area_weight * prop.room_details.est_sq_ft / mean_area
    bed_score = bed_weight * prop.room_details.bed_count / mean_bed_count
    bath_score = bath_weight * (prop.room_details.full_bath_count/ mean_full_bath_count + 0.5 * prop.room_details.half_bath_count / mean_half_bath_count)
    has_unit_laundry = False
    has_gas_fireplace = False
    has_wood_fireplace = False
    has_trash_collection = False
    has_range = False
    has_fridge = False
    has_water_softener = False
    for inc in prop.inclusions:
        if (
            inc.item == "in-unit laundry"
            or (
                inc.item == "dryer"
                and inc.item == "washer"
            )
        ):
            has_unit_laundry = True
        if inc.item == "gas fireplace":
            has_gas_fireplace = True
        if inc.item == "natural fireplace":
            has_wood_fireplace = True
        if inc.item == "trash collection":
            has_trash_collection = True
        if inc.item == "range":
            has_range = True
        if inc.item == "refrigerator":
            has_fridge = True
        if inc.item == "water softener":
            has_water_softener = True

    allows_cats = False
    if prop.pet_details.pets_are_allowed \
    and not(prop.pet_details.cat_limit is None):
        if prop.pet_details.cat_limit > 1:
            allows_cats = True

    prop.metrics.property_score += expenses_score
    prop.metrics.property_score += work_distance_score
    prop.metrics.property_score += area_score
    prop.metrics.property_score += bed_score
    prop.metrics.property_score += bath_score

    base_score = 1
    prop.metrics.property_score += base_score * laundry_weight * int(has_unit_laundry)
    prop.metrics.property_score += base_score * pet_weight * int(allows_cats)
    prop.metrics.property_score += base_score * gas_fireplace_weight * int(has_gas_fireplace)
    prop.metrics.property_score += base_score * wood_fireplace_weight * int(has_wood_fireplace)
    prop.metrics.property_score += base_score * trash_collection_weight * int(has_trash_collection)
    prop.metrics.property_score += base_score * range_weight * int(has_range)
    prop.metrics.property_score += base_score * fridge_weight * int(has_fridge)
    prop.metrics.property_score += base_score * water_softener_weight * int(has_water_softener)

    prop.metrics.monthly_expense_score = expenses_score
    prop.metrics.work_distance_score = work_distance_score
    prop.metrics.area_score = area_score
    prop.metrics.bed_score = bed_score
    prop.metrics.bath_score = bath_score
    prop.metrics.has_unit_laundry = has_unit_laundry
    prop.metrics.has_gas_fireplace = has_gas_fireplace
    prop.metrics.has_wood_fireplace = has_wood_fireplace
    prop.metrics.has_trash_collection = has_trash_collection
    prop.metrics.has_range = has_range
    prop.metrics.has_fridge = has_fridge
    prop.metrics.has_water_softener = has_water_softener

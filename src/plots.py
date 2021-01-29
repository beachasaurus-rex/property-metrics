from matplotlib import (
    pyplot,
    patches
)
from pandas import (
    DataFrame,
    qcut
)
from decimal import Decimal

from data import (
    ListingStatus,
    get_current_status
)
from metrics import (
    calculate_monthly_expenses,
    calculate_property_score
)

def make_plots(properties: list, folder_path: str):
    headers = [
        "total_monthly_expenses",
        "work_distance",
        "area",
        "bed_count",
        "full_bath_count",
        "half_bath_count"
    ]
    csv_data = []
    for prop in properties:
        get_current_status(prop)
        calculate_monthly_expenses(prop)
        if not(
            prop.current_status.listing_status == ListingStatus.S
            or prop.current_status.listing_status == ListingStatus.E
        ):
            csv_data.append([
                prop.metrics.get_monthly_expenses(),
                prop.location.work_distance,
                prop.room_details.est_sq_ft,
                prop.room_details.bed_count,
                prop.room_details.full_bath_count,
                prop.room_details.half_bath_count
            ])
    
    df = DataFrame.from_records(csv_data, columns=headers)
    mean_monthly_exp = df["total_monthly_expenses"].mean()
    mean_work_dist = df["work_distance"].mean()
    mean_area = df["area"].mean()
    mean_bed_count = df["bed_count"].mean()
    mean_full_bath_count = df["full_bath_count"].mean()
    mean_half_bath_count = df["half_bath_count"].mean()
    headers = [
        "property_id",
        "full_adress",
        "price",
        "total_monthly_expenses",
        "monthly_utility_bill",
        "monthly_property_tax",
        "monthly_mortgage",
        "monthly_condo_fee",
        "utility_bill_ratio",
        "property_tax_ratio",
        "mortgage_ratio",
        "condo_fee_ratio",
        "property_score",
        "latitudes",
        "longitudes"
    ]
    csv_data = []
    for prop in properties:
        calculate_property_score(prop,
            mean_monthly_exp,
            mean_work_dist,
            mean_area,
            mean_bed_count,
            mean_full_bath_count,
            mean_half_bath_count
        )
        if not(
            prop.current_status.listing_status == ListingStatus.S
            or prop.current_status.listing_status == ListingStatus.E
        ):
            csv_data.append([
                prop.pid,
                prop.location.total_address,
                prop.current_status.price,
                prop.metrics.get_monthly_expenses(),
                prop.metrics.monthly_utility_bill,
                prop.metrics.monthly_property_tax,
                prop.metrics.monthly_mortgage,
                prop.metrics.monthly_condo_fee,
                prop.metrics.get_ratio_utility_bills(),
                prop.metrics.get_ratio_property_tax(),
                prop.metrics.get_ratio_mortgage(),
                prop.metrics.get_ratio_condo_fee(),
                prop.metrics.property_score,
                prop.location.latitude,
                prop.location.longitude
            ])
    
    df = DataFrame.from_records(csv_data, columns=headers)
    plot_price_v_monthly_exp(
        df["price"],
        df["total_monthly_expenses"],
        df["property_id"],
        folder_path
    )
    plot_price_v_prop_score(
        df["price"],
        df["property_score"],
        df["property_id"],
        folder_path
    )
    plot_monthly_exp_v_prop_score(
        df["total_monthly_expenses"],
        df["property_score"],
        df["property_id"],
        folder_path
    )
    plot_abs_location_v_monthly_exp(
        df["latitudes"],
        df["longitudes"],
        df["total_monthly_expenses"],
        df["property_id"],
        folder_path
    )
    plot_abs_location_v_price(
        df["latitudes"],
        df["longitudes"],
        df["price"],
        df["property_id"],
        folder_path
    )
    plot_abs_location_v_property_score(
        df["latitudes"],
        df["longitudes"],
        df["property_score"],
        df["property_id"],
        folder_path
    )

def plot_price_v_monthly_exp(
    prices: DataFrame,
    monthly_exp: DataFrame,
    property_ids: DataFrame,
    folder_path: str
):
    fig, ax = pyplot.subplots()
    ax.scatter(prices, monthly_exp)
    for i, txt in enumerate(property_ids):
        ax.annotate(txt, (prices[i], monthly_exp[i]))
    pyplot.xlabel("price")
    pyplot.ylabel("est monthly expenses")
    pyplot.ylim(900,1800)
    pyplot.xlim(1E+05, 2.3E+05)
    pyplot.savefig(f"{folder_path}/price_v_monthly_exp.png", format="png")

def plot_price_v_prop_score(
    prices: DataFrame,
    scores: DataFrame,
    property_ids: DataFrame,
    folder_path: str
):
    fig, ax = pyplot.subplots()
    ax.scatter(prices, scores)
    for i, txt in enumerate(property_ids):
        ax.annotate(txt, (prices[i], scores[i]))
    pyplot.xlabel("price")
    pyplot.ylabel("property score")
    pyplot.savefig(f"{folder_path}/price_v_prop_score.png", format="png")

def plot_monthly_exp_v_prop_score(
    monthly_exp: DataFrame,
    scores: DataFrame,
    property_ids: DataFrame,
    folder_path: str
):
    fig, ax = pyplot.subplots()
    ax.scatter(monthly_exp, scores)
    for i, txt in enumerate(property_ids):
        ax.annotate(txt, (monthly_exp[i], scores[i]))
    pyplot.xlabel("est monthly expenses")
    pyplot.ylabel("property score")
    pyplot.xlim(900,1800)
    pyplot.savefig(f"{folder_path}/monthly_exp_v_prop_score.png", format="png")

def plot_abs_location_v_monthly_exp(
    latitudes: DataFrame,
    longitudes: DataFrame,
    monthly_exp: DataFrame,
    property_ids: DataFrame,
    folder_path: str
):
    colors = ["purple", "blue", "green", "red"]
    exp_lists = [[exp] for exp in monthly_exp]
    exp = DataFrame.from_records(exp_lists, columns=["monthly_exp"])
    exp["colors"], bins = qcut(exp["monthly_exp"], q=[0, 0.25, 0.5, 0.75, 1], precision=0, retbins=True, labels=colors)
    color_patches = []
    for i in range(0, len(colors)):
        label_str = ""
        mini = int(Decimal(str(round(bins[i],0))))
        maxi = int(Decimal(str(round(bins[i+1],0))))
        if i == 0:
            label_str = f"({mini} to {maxi}]"
        else:
            label_str = f"[{mini} to {maxi})"
        color_patches.append(patches.Patch(color=colors[i], label=label_str))

    fig, ax = pyplot.subplots()
    lats = [lat[0] for lat in latitudes]
    longs = [l[0] for l in longitudes]
    ax.scatter(longs, lats, c=exp["colors"])
    for i, txt in enumerate(property_ids):
        ax.annotate(txt, (longs[i], lats[i]))
    pyplot.xlabel("latitude")
    pyplot.ylabel("longitude")
    pyplot.title("Absolute Location vs. Monthly Expenses")
    pyplot.legend(handles=color_patches)
    pyplot.savefig(f"{folder_path}/abs_location_v_monthly_exp.png", format="png")

def plot_abs_location_v_price(
    latitudes: DataFrame,
    longitudes: DataFrame,
    price: DataFrame,
    property_ids: DataFrame,
    folder_path: str
):
    colors = ["purple", "blue", "green", "red"]
    exp_lists = [[exp] for exp in price]
    exp = DataFrame.from_records(exp_lists, columns=["price"])
    exp["colors"], bins = qcut(exp["price"], q=[0, 0.25, 0.5, 0.75, 1], precision=0, retbins=True, labels=colors)
    color_patches = []
    for i in range(0, len(colors)):
        label_str = ""
        mini = int(Decimal(str(round(bins[i],0))))
        maxi = int(Decimal(str(round(bins[i+1],0))))
        if i == 0:
            label_str = f"({mini} to {maxi}]"
        else:
            label_str = f"[{mini} to {maxi})"
        color_patches.append(patches.Patch(color=colors[i], label=label_str))

    fig, ax = pyplot.subplots()
    lats = [lat[0] for lat in latitudes]
    longs = [l[0] for l in longitudes]
    ax.scatter(longs, lats, c=exp["colors"])
    for i, txt in enumerate(property_ids):
        ax.annotate(txt, (longs[i], lats[i]))
    pyplot.xlabel("latitude")
    pyplot.ylabel("longitude")
    pyplot.title("Absolute Location vs. Price")
    pyplot.legend(handles=color_patches)
    pyplot.savefig(f"{folder_path}/abs_location_v_price.png", format="png")

def plot_abs_location_v_property_score(
    latitudes: DataFrame,
    longitudes: DataFrame,
    scores: DataFrame,
    property_ids: DataFrame,
    folder_path: str
):
    colors = ["purple", "blue", "green", "red"]
    score_lists = [[score] for score in scores]
    scores = DataFrame.from_records(score_lists, columns=["scores"])
    scores["colors"], bins = qcut(scores["scores"], q=[0, 0.37, 0.5275, 0.685, 1], precision=0, retbins=True, labels=colors)
    color_patches = []
    for i in range(0, len(colors)):
        label_str = ""
        mini = int(Decimal(str(round(bins[i],0))))
        maxi = int(Decimal(str(round(bins[i+1],0))))
        if i == 0:
            label_str = f"({mini} to {maxi}]"
        else:
            label_str = f"[{mini} to {maxi})"
        color_patches.append(patches.Patch(color=colors[i], label=label_str))

    fig, ax = pyplot.subplots()
    lats = [lat[0] for lat in latitudes]
    longs = [l[0] for l in longitudes]
    ax.scatter(longs, lats, c=scores["colors"])
    for i, txt in enumerate(property_ids):
        ax.annotate(txt, (longs[i], lats[i]))
    pyplot.xlabel("latitude")
    pyplot.ylabel("longitude")
    pyplot.title("Absolute Location vs. Property Score")
    pyplot.legend(handles=color_patches)
    pyplot.savefig(f"{folder_path}/abs_location_v_property_score.png", format="png")
import pandas as pd
from db_schema import Base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///candy_distributor.db")

# Get data into Pandas DataFrames
def load_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    sales = pd.read_csv("./data/Candy_Sales.csv")
    factories = pd.read_csv("./data/Candy_Factories.csv")
    products = pd.read_csv("./data/Candy_Products.csv")
    targets = pd.read_csv("./data/Candy_Targets.csv")
    zip_codes = pd.read_csv("./data/uszips.csv")

    # Load data into factories table
    factories.columns = ["factory", "latitude", "longitude"]
    factories.to_sql("factories", engine, if_exists="append", index=False)

    # Load data into products table
    products.columns = ["division", "product_name", "factory", "product_id", "unit_price", "unit_cost"]
    products.to_sql("products", engine, if_exists="append", index=False)

    # Load data into zip_codes table
    zip_codes = zip_codes.drop(columns=["parent_zcta", "county_weights", "county_names_all", "county_fips_all"])
    zip_codes["zip"] = zip_codes["zip"].astype(str).str.zfill(5)
    zip_codes["county_fips"] = zip_codes["county_fips"].astype(str)
    zip_codes.to_sql("zip_codes", engine, if_exists="append", index=False)

    # Load data into targets table
    targets.columns = ["division", "target"]
    targets.to_sql("targets", engine, if_exists="append", index=False)

    # Load data into sales table
    sales = sales.drop(columns=["Division", "Product Name"])
    sales.columns = ["row_id", "order_id", "order_date", "ship_date", "ship_mode", "customer_id", "country_region", "city", "state_province", "postal_code", "region", "product_id", "sales", "units", "gross_profit", "cost"]
    sales["order_date"] = pd.to_datetime(sales["order_date"]).dt.date
    sales["ship_date"] = pd.to_datetime(sales["ship_date"]).dt.date
    sales["postal_code"] = sales["postal_code"].str.zfill(5)
    sales.to_sql("sales", engine, if_exists="append", index=False)

if __name__ == "__main__":
    load_data()
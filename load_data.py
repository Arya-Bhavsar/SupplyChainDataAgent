import pandas as pd

# Get data into Pandas DataFrames
sales = pd.read_csv("./data/Candy_Sales.csv")
factories = pd.read_csv("./data/Candy_Factories.csv")
products = pd.read_csv("./data/Candy_Products.csv")
targets = pd.read_csv("./data/Candy_Targets.csv")
zip_codes = pd.read_csv("./data/uszips.csv")

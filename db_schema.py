from sqlalchemy import ForeignKey, String, Integer, Numeric, Boolean, Float, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date

class Base(DeclarativeBase):
    pass

# Sales schema
class Sale(Base):
    __tablename__ = "sales"

    row_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[str] = mapped_column(String)
    order_date: Mapped[date] = mapped_column(Date)
    ship_date: Mapped[date] = mapped_column(Date)
    ship_mode: Mapped[str] = mapped_column(String)
    customer_id: Mapped[int] = mapped_column(Integer)
    country_region: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    state_province: Mapped[str] = mapped_column(String)
    postal_code: Mapped[str] = mapped_column(String)
    region: Mapped[str] = mapped_column(String)
    product_id: Mapped[str] = mapped_column(String, ForeignKey("products.product_id"))
    sales: Mapped[float] = mapped_column(Numeric(10, 2))
    units: Mapped[int] = mapped_column(Integer)
    gross_profit: Mapped[float] = mapped_column(Numeric(10, 2))
    cost: Mapped[float] = mapped_column(Numeric(10, 2))

# Factories schema
class Factory(Base):
    __tablename__ = "factories"

    factory: Mapped[str] = mapped_column(String, primary_key=True)
    latitude: Mapped[float] = mapped_column(Numeric(8, 6))
    longitude: Mapped[float] = mapped_column(Numeric(9, 6))

# Products schema
class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(String, primary_key=True)
    product_name: Mapped[str] = mapped_column(String)
    division: Mapped[str] = mapped_column(String)
    factory: Mapped[str] = mapped_column(String, ForeignKey("factories.factory"))
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2))
    unit_cost: Mapped[float] = mapped_column(Numeric(10, 2))

# Targets schema
class Target(Base):
    __tablename__ = "targets"

    division: Mapped[str] = mapped_column(String, primary_key=True)
    target: Mapped[int] = mapped_column(Integer)

# US Zip schema
class ZipCode(Base):
    __tablename__ = "zip_codes"

    zip: Mapped[str] = mapped_column(String, primary_key=True)
    lat: Mapped[float] = mapped_column(Numeric(8, 6))
    lng: Mapped[float] = mapped_column(Numeric(9, 6))
    city: Mapped[str] = mapped_column(String)
    state_id: Mapped[str] = mapped_column(String)
    state_name: Mapped[str] = mapped_column(String)
    zcta: Mapped[bool] = mapped_column(Boolean)
    population: Mapped[int | None] = mapped_column(Integer)
    density: Mapped[float | None] = mapped_column(Float)
    county_fips: Mapped[str] = mapped_column(String)
    county_name: Mapped[str] = mapped_column(String)
    imprecise: Mapped[bool] = mapped_column(Boolean)
    military: Mapped[bool] = mapped_column(Boolean)
    timezone: Mapped[str] = mapped_column(String)
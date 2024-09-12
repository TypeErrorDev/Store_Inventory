from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine("sqlite:///inventory.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Brands(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)

    def __repr__(self):
        return f"""
        \nBrand ID: {self.brand_id}\r
        Brand Name: {self.brand_name}
        """
    
class Products(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)
    brand_id = Column(Integer, ForeignKey=True)

    def __repr__(self):
        return f"""
        \nProducts {self.product_id}\r
        Brand ID: {self.brand_id}
        Name: {self.product_name}
        Quantity: {self.product_quantity}
        Price: {self.product_price}
        Last Updated: {self.date_updated}
        """


if __name__ == "__main__":
    Base.metadata.create_all(engine)
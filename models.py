from sqlalchemy import (create_engine, Column, Integer, 
                        String, Date, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Brands(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    brand_name = Column(String, nullable=False,)
    products = relationship("Products", back_populates="brand")

    def __repr__(self):
        return f""" 
        \n***** BRANDS *****
        \nBrand ID: {self.brand_id}\r
        Brand Name: {self.brand_name}
        """
    

class Products(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))
    product_name = Column(String, nullable=False)
    product_quantity = Column(Integer, nullable=False)
    product_price = Column(Integer, nullable=False)
    date_updated = Column(Date, nullable=False)
    

    brand = relationship("Brands", back_populates="products")
    

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
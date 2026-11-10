from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

clothing_category = Table(
    "clothing_category",
    Base.metadata,
    Column("clothing_id", Integer, ForeignKey("clothes.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    clothes = relationship("Clothing", secondary=clothing_category, back_populates="categories")

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    country_of_origin = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    clothes = relationship("Clothing", back_populates="brand")

    def __repr__(self) -> str:
        return f"Brand(id={self.id}, name={self.name})"


class Clothing(Base):
    __tablename__ = "clothes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    price_sale = Column(Float, nullable=False)
    price_cost = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    brand = relationship("Brand", back_populates="clothes")
    categories = relationship("Category", secondary=clothing_category, back_populates="clothes")
    variations = relationship("Variation", back_populates="clothing", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Clothing(id={self.id}, name={self.name})"


class Variation(Base):
    __tablename__ = "variations"

    id = Column(Integer, primary_key=True, index=True)
    clothing_id = Column(Integer, ForeignKey("clothes.id"), nullable=False)
    size = Column(String(20), nullable=False)
    color = Column(String(50), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)

    __table_args__ = (UniqueConstraint("clothing_id", "size", "color", name="uq_variacao_roupa_tamanho_cor"),)

    clothing = relationship("Clothing", back_populates="variations")
    sale_items = relationship("SaleItem", back_populates="variation")
    stock_entry_items = relationship("StockEntryItem", back_populates="variation")

    def __repr__(self) -> str:
        return f"Variation(id={self.id}, size={self.size}, color={self.color})"


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    cpf = Column(String(20), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    phone = Column(String(50), nullable=True)
    birth_date = Column(Date, nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    observation = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    sales = relationship("Sale", back_populates="client")

    def __repr__(self) -> str:
        return f"Client(id={self.id}, name={self.name})"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    cpf = Column(String(20), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    phone = Column(String(50), nullable=True)
    hire_date = Column(Date, nullable=True)
    role = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    sales = relationship("Sale", back_populates="employee")
    stock_entries = relationship("StockEntry", back_populates="employee")

    def __repr__(self) -> str:
        return f"Employee(id={self.id}, name={self.name})"


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    document_number = Column(String(50), nullable=False, unique=True)
    email = Column(String(150), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    observation = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    stock_entries = relationship("StockEntry", back_populates="supplier")

    def __repr__(self) -> str:
        return f"Supplier(id={self.id}, name={self.name})"


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_value = Column(Float, nullable=False, default=0.0)
    payment_method = Column(String(50), nullable=False)
    status = Column(String(30), nullable=False, default="Pendente")
    observation = Column(Text, nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    client = relationship("Client", back_populates="sales")
    employee = relationship("Employee", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Sale(id={self.id}, total={self.total_value})"


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    variation_id = Column(Integer, ForeignKey("variations.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False, default=0.0)
    subtotal = Column(Float, nullable=False, default=0.0)

    sale = relationship("Sale", back_populates="items")
    variation = relationship("Variation", back_populates="sale_items")

    def __repr__(self) -> str:
        return f"SaleItem(id={self.id}, quantity={self.quantity})"


class StockEntry(Base):
    __tablename__ = "stock_entries"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    invoice_number = Column(String(100), nullable=False)
    total_value = Column(Float, nullable=False, default=0.0)
    observation = Column(Text, nullable=True)
    confirmed = Column(Boolean, default=False, nullable=False)

    supplier = relationship("Supplier", back_populates="stock_entries")
    employee = relationship("Employee", back_populates="stock_entries")
    items = relationship("StockEntryItem", back_populates="entry", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"StockEntry(id={self.id}, invoice_number={self.invoice_number})"


class StockEntryItem(Base):
    __tablename__ = "stock_entry_items"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("stock_entries.id"), nullable=False)
    variation_id = Column(Integer, ForeignKey("variations.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False, default=0.0)

    entry = relationship("StockEntry", back_populates="items")
    variation = relationship("Variation", back_populates="stock_entry_items")

    def __repr__(self) -> str:
        return f"StockEntryItem(id={self.id}, quantity={self.quantity})"

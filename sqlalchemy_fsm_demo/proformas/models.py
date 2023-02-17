from sqlalchemy import Column, Integer, String, Date, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_fsm import FSMField
from django.db import models

# Create your models here.

Base = declarative_base()


class Proforma(Base):
    __tablename__ = "proformas"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    creation_date = Column(Date)
    total_value = Column(Double)
    state = Column(FSMField, nullable=False)

    def __init__(self, full_name, date, total_value, state="created") -> None:
        self.full_name = full_name
        self.creation_date = date
        self.total_value = total_value
        self.state = state

    def __repr__(self) -> str:
        return f"Proforma({self.full_name},{self.creation_date},{self.total_value},{self.state})"

    class Meta:
        app_label = "proformas"

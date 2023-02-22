from sqlalchemy import Column, Integer, String, Date, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_fsm import FSMField, transition

# Create your models here.

Base = declarative_base()


# Class object with two methods, no need to call specifically its methods
# it will execute them based on the source state
@transition(target="pagada")
class ProformaHandler(object):
    @transition(source="aceptada")
    def pagar_contado(self, instance):
        instance.side_effect = "Proforma cancelada de contado"

    @transition(source="credito")
    def dar_credito(self, instance):
        instance.side_effect = "Proforma otorgada crédito fue cancelada"


# Generating a SA class, differs from a Django model
class Proforma(Base):
    __tablename__ = "proformas"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    creation_date = Column(Date)
    total_value = Column(Double)
    state = Column(FSMField, nullable=False)
    pago = ProformaHandler

    def __init__(self, full_name, date, total_value, state="creada") -> None:
        self.full_name = full_name
        self.creation_date = date
        self.total_value = total_value
        self.state = state

    def __repr__(self) -> str:
        return f"Proforma({self.full_name},{self.creation_date},{self.total_value},{self.state})"

    # Verifying if the proforma value is greater than or equal to 200
    # in order to grant credit
    def check_value(self) -> bool:
        if self.total_value >= 200:
            return True
        return False

    @transition(source="creada", target="aceptada")
    def accept(self):
        print("Proforma aceptada")

    # Using a condition to verify it the state transition can be done
    @transition(source="aceptada", target="credito", conditions=[check_value])
    def give_credit(self):
        print("Proforma procesada a credito")

    class Meta:
        app_label = "proformas"

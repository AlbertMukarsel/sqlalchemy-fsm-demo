from sqlalchemy import Column, Integer, String, Date, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_fsm import FSMField, transition

# Create your models here.

Base = declarative_base()


# Class object with two methods, no need to call specifically its methods
# it will execute them based on the source state
@transition(target="paid")
class PurchaseOrderHandler(object):
    @transition(source="accepted")
    def pay_cash(self, instance):
        instance.side_effect = "Purchase order paid in cash"

    @transition(source="credit")
    def give_credit(self, instance):
        instance.side_effect = "Granted credit has been paid"


# Generating a SA class, differs from a Django model
class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    creation_date = Column(Date)
    total_value = Column(Double)
    state = Column(FSMField, nullable=False)
    pago = PurchaseOrderHandler

    def __init__(self, full_name, date, total_value, state="created") -> None:
        self.full_name = full_name
        self.creation_date = date
        self.total_value = total_value
        self.state = state

    def __repr__(self) -> str:
        return f"PurchaseOrder({self.full_name},{self.creation_date},{self.total_value},{self.state})"

    # Verifying if the purchase order value is greater than or equal to 200
    # in order to grant credit
    def check_value(self) -> bool:
        if self.total_value >= 200:
            return True
        return False

    @transition(source="created", target="accepted")
    def accept(self):
        print("Purchase order accepted")

    # Using a condition to verify it the state transition can be done
    @transition(source="accepted", target="credit", conditions=[check_value])
    def give_credit(self):
        print("Purchase order processed with credit")

    class Meta:
        app_label = "proformas"

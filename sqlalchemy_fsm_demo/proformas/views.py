from django.shortcuts import render
from proformas.models import Base, PurchaseOrder
from sqlalchemy_fsm_demo.settings import sa_engine, session
from datetime import datetime
import traceback

Base.metadata.create_all(sa_engine)


# Validating DB is empty or not
def is_empty():
    return session.query(PurchaseOrder).count() <= 0


# Adding initial records
def populate():
    today = datetime.now()
    initial_orders = [
        PurchaseOrder("Alberto Mucarsel", today, 150.45),
        PurchaseOrder("Juan Perez", today, 2500.20),
    ]
    session.add_all(initial_orders)
    session.commit()


# Create your views here.
def index(request):
    if is_empty():
        populate()
    orders = session.query(PurchaseOrder).order_by(PurchaseOrder.id).all()
    return render(request, "proformas/index.html", {"orders": orders})


# Adding records to DB using session.add() from SA
def create(request):
    created = False
    if request.method == "POST":
        data = request.POST
        session.add(PurchaseOrder(data["full_name"], data["date"], data["total_value"]))
        session.commit()
        created = True
    return render(request, "proformas/create.html", {"form_submitted": created})


def update(request):
    if request.method == "POST":
        data = request.POST
        current_file = session.query(PurchaseOrder).get(data["pk"])
        result = "Purchase order updated"
        if data["state"] == "approved":
            # Calling transition-decorated methods
            try:
                current_file.accept.set()
            except:
                result = "This purchase order has been already accepted"
        elif data["state"] == "credit":
            # .set() changes the state of the record object to the transitions' target state
            # (or raises an exception if it is not able to do so)
            try:
                current_file.give_credit.set()
            # Handling Exceptions when transition cannot be done
            except Exception:
                result = "Cannot grant credit to this purchase order"
                traceback.print_exc()
        elif data["state"] == "paid":
            try:
                current_file.pago.set()
            except:
                result = "Purchase order cannot be paid until accepted first"
    return render(request, "proformas/result.html", {"result": result})


def delete(request):
    if request.method == "POST":
        data = request.POST
        current_file = session.query(PurchaseOrder).get(data["pk"])
        session.delete(current_file)
        session.commit()
    return render(request, "proformas/result.html", {"result": "Purchase order marked as void"})

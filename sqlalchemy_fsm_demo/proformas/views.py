from django.shortcuts import render
from proformas.models import Base, Proforma
from sqlalchemy_fsm_demo.settings import sa_engine, session
from datetime import datetime
import traceback

Base.metadata.create_all(sa_engine)


# Validating DB is empty or not
def is_empty():
    return session.query(Proforma).count() <= 0


# Adding initial records
def populate():
    today = datetime.now()
    proformas_inciales = [
        Proforma("Alberto Mucarsel", today, 150.45),
        Proforma("Juan Perez", today, 2500.20),
    ]
    session.add_all(proformas_inciales)
    session.commit()


# Create your views here.
def index(request):
    if is_empty():
        populate()
    proformas = session.query(Proforma).order_by(Proforma.id).all()
    return render(request, "proformas/index.html", {"proformas": proformas})


# Adding records to DB using session.add() from SA
def create(request):
    created = False
    if request.method == "POST":
        data = request.POST
        session.add(Proforma(data["full_name"], data["date"], data["total_value"]))
        session.commit()
        created = True
    return render(request, "proformas/create.html", {"form_submitted": created})


def update(request):
    if request.method == "POST":
        data = request.POST
        current_file = session.query(Proforma).get(data["pk"])
        result = "Proforma actualizada"
        if data["state"] == "aprobada":
            # Calling transition-decorated methods
            try:
                current_file.accept.set()
            except:
                result = "Esta proforma ya fue aceptada"
        elif data["state"] == "credito":
            # .set() changes the state of the record object to the transitions' target state
            # (or raises an exception if it is not able to do so)
            try:
                current_file.give_credit.set()
            # Handling Exceptions when transition cannot be done
            except Exception:
                result = "No se puede otorgar crédito"
                traceback.print_exc()
        elif data["state"] == "pagada":
            try:
                current_file.pago.set()
            except:
                result = "No se puede cancelar hasta aceptarse primero"
    return render(request, "proformas/result.html", {"resultado": result})


def delete(request):
    if request.method == "POST":
        data = request.POST
        current_file = session.query(Proforma).get(data["pk"])
        session.delete(current_file)
        session.commit()
    return render(request, "proformas/result.html", {"resultado": "Proforma eliminada"})

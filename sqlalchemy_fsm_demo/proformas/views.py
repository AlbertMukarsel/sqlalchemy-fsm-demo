from django.shortcuts import render
from proformas.models import Base, Proforma
from sqlalchemy_fsm_demo.settings import sa_engine, session
from datetime import datetime

Base.metadata.create_all(sa_engine)


def is_empty():
    return session.query(Proforma).count() <= 0


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
    proformas = session.query(Proforma).all()
    return render(request, "proformas/index.html", {"proformas": proformas})

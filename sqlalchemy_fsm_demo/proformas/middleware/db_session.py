from sqlalchemy_fsm_demo import settings


class MySQLAlchemySessionMiddleware(object):
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        process_request(request)
        response = self.get_response(request)
        try:
            return process_response(request, response)
        except:
            process_exception(request)


def process_request(self, request):
    request.db_session = settings.Session()


def process_response(self, request, response):
    try:
        session = request.db_session
    except AttributeError:
        return response
    try:
        session.commit()
        return response
    except:
        session.rollback()
        raise


def process_exception(self, request, exception):
    try:
        session = request.db_session
    except AttributeError:
        return
    session.rollback()

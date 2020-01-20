from django.contrib.sessions.models import Session
from .models import User


def Token_authentigetion(request):
    try:
        if request.session.exists(request.session.session_key):
            session = Session.objects.get(session_key=request.session.session_key)
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            user_details = User.objects.get(id=uid)
            if user_details.username == str(request.user):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(e)
        return False

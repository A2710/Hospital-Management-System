from H1.models import MenuMaster,HandleLogin

def add_variable_to_context(request):

    menu  = MenuMaster.objects.all().order_by('MenuOrder').values()
    userid = request.session.get("userid","")
    superuser = request.session.get("superuser", 0)

    return {
        "menu" : menu,
        "userid":userid,
        "superuser" : superuser
    }
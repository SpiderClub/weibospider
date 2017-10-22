from django.shortcuts import redirect


def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)
    else:
        return redirect('/admin/')
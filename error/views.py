from django.shortcuts import render


# Create your views here.
def erro_403(request, exception=None):
    return render(request, 'error/403.html', status=403)
def erro_404(request, exception=None):
    return render(request, 'error/404.html', status=404)
def erro_500(request):
    return render(request, 'error/500.html', status=500)
def erro_400(request, exception=None):
    return render(request, 'error/400.html', status=400)

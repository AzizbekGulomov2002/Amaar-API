from django.shortcuts import render


def payment_success(request):
    session_id = request.GET.get('session_id', '')
    return render(request, 'payment_success.html', {'session_id': session_id})


def payment_fail(request):
    return render(request, 'payment_fail.html')

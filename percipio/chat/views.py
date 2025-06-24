from django.shortcuts import render


def chat_test_view(request):
    return render(request, 'chat/index.html')

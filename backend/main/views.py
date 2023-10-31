from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

from .forms import UserForm
from .models import Word


@login_required
@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        data = request.POST.get("data")
        Word.objects.filter(id_user=request.user).delete()
        key_words = " | ".join([word for word in set(data.split("\r\n")) if len(word.strip()) > 0])
        Word(word=key_words, id_user=request.user).save()
    user_form = UserForm(request.user)
    return render(request, "index.html", {"form": user_form})

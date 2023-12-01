from django.shortcuts import render
from Core.models import Frage, Benutzer
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.core.paginator import Paginator
from .utils import get_hot_frage, get_frage_des_tages, get_top_5_users, \
                   get_user_answer_frage_des_tages, get_statistics_frage_des_tages


@login_required(login_url='/login/')
# Leitet User zum Login, wenn nicht eingeloggt
def startseite_view(request):

    del_user = Benutzer.objects.get(username="entfernt")

    # Sortierung des QuerySets. "-" bedeutet absteigend, "" aufsteigend.
    # TruncDate von Django holt nur Date, ignoriert Time.
    frage = Frage.objects.\
        exclude(user=del_user).\
        annotate(creation_date_only=TruncDate('creation_date')).\
        order_by("-creation_date_only", "-likes")

    # Instanziierung eines Paginators
    # Damit werden Seiten von Django gemanaged
    # class Paginator(object_list, per_page, *orphans, *allow_empty_first_page)
    paginator = Paginator(frage, 10)
    page = request.GET.get('page')
    page_frage = paginator.get_page(page)

    timestamp = timezone.now()

    hot_frage = get_hot_frage()

    frage_des_tages = get_frage_des_tages(request.user,
                                          timestamp)

    answer_frage_des_tages = get_user_answer_frage_des_tages(request.user,
                                                             frage_des_tages,
                                                             timestamp)

    statistics_frage_des_tages = get_statistics_frage_des_tages(
        frage_des_tages, timestamp)

    top_5_user = get_top_5_users(timestamp)

    context = {"page_frage": page_frage,
               "hot_frage": hot_frage,
               "frage_des_tages": frage_des_tages,
               "answer_frage_des_tages": answer_frage_des_tages,
               "statistics_frage_des_tages": statistics_frage_des_tages,
               "top_5_user": top_5_user}

    return render(request, 'startseite.html', context)

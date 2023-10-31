import re

from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import Word, LastCheckedTender


def get_users():
    return User.objects.exclude(email="")


def send_message(message, to):
    send_mail("New interesting tender for Deeplace", message, "tenderfordeeplacebot@gmail.com", [to], fail_silently=False)


def get_key_words(user):
    words = list(Word.objects.filter(id_user=user).values_list("word"))
    try:
        key_words = words[0][0].split(" | ")
    except IndexError:
        key_words = []
    return key_words


def get_last_checked_tender(name_of_site):
    try:
        return list(LastCheckedTender.objects.filter(tender=name_of_site).values_list("last_checked_tender"))[0][0]
    except IndexError:
        return


def put_last_checked_tender(new_checked_tender, name_of_site):
    LastCheckedTender.objects.filter(tender=name_of_site).delete()
    LastCheckedTender(tender=name_of_site, last_checked_tender=new_checked_tender).save()


def get_needed_tenders(tender_content, needed_tenders, tender_link, key_words):
    for key_word in key_words:
        key_word = re.sub("[^A-Za-z0-9А-ЯЁа-яёĂăÂâÎîȘșȚț\\s\\w]+", "", key_word).replace("  ", "").lower()
        if key_word in tender_content:
            needed_tenders.append(tender_link)
            break
    return needed_tenders


def clear_tender_content(tender_content):
    return re.sub("[^A-Za-z0-9 ]+", "", tender_content).replace("  ", " ").lower()

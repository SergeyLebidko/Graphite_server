from django.db.models import Q


def search(queryset, string, queryset_type):
    if queryset_type == 'post':
        queryset = queryset.filter(Q(text__contains=string) | Q(account__username__contains=string))
    elif queryset_type == 'account':
        queryset = queryset.filte(username__contains=string)

    return [] if queryset is None else list(queryset)

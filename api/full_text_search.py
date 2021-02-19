import re
import itertools


# Функции этого модуля реализуют полнотекстовый поиск среди постов или имен авторов.
# Управляет типом поиска (посты или автороы) параметр queryset_type.
# Сам поиск идет без учета регистра.
# Строка поиска проходит ряд преобразований, влияющих на релевантность найденных значений.
# Чем сильнее преобразована строка - тем менее релевантны найденные значения и тем дальше от первого места они будут
# находиться в итоговом списке результатов поиска.
#
# Суть преобразований строки для поиска проста: сначала мы пытаемся найти полное совпадение текста и строки.
# Если такое совпадение найдено - оно будет самым релевантным.
# Затем отсекаем ведущие и конечные пробелы и снова ищем совпадение (такое совпадение будет вторым по релевантности).
# Затем все пробельные символы заменяем одним пробелом и снова ищем совпадения.
# И, наконец, разбиваем строку поиска на отдельные слова и ищем уже их. При этом учитываем, что слова могут
# образовываться путем добавления суффиксов и окончаний и отсекаем их, чтобы учесть еще больше возможных результатов.
# Но релевантность таких результатов обычно не очень высока, поэтому они оказываются ближе к концу итогового списка.


def search(queryset, string, queryset_type):
    temp_stages = [stage_1(string), stage_2(string), stage_3(string)]
    temp_stages.extend(stage_4(string))

    stages = []
    for stage in temp_stages:
        if stage not in stages:
            stages.append(stage)

    result = []
    src_queryset = list(queryset)
    for stage in stages:
        result.extend(_search(src_queryset, result, stage, queryset_type))
    return result


def stage_1(string):
    return [string]


def stage_2(string):
    return [string.strip()]


def stage_3(string):
    result = string.strip()
    regex = re.compile(r'\s+')
    result = regex.sub(' ', result)
    return [result]


def stage_4(string):
    regex = re.compile(r'[^0-9a-zA-Zа-яА-я]+')
    words = [e for e in regex.split(string) if e]
    result = []
    for count in range(len(words), 0, -1):
        for combination in itertools.combinations(words, count):
            result.append(list(combination))
            clip = 1
            while any([len(word) > 5 for word in result[-1]]):
                result.append([(word if len(word) <= 5 else word[:-clip]) for word in result[-1]])
                clip += 1

    return result


def _search(src_queryset, dst_queryset, strings, queryset_type):
    result = []
    for element in src_queryset:
        find_count = 0
        for string in strings:
            string = string.lower()
            if queryset_type == 'post':
                find_count += (string in element.text.lower()) or (string in element.title.lower())
            elif queryset_type == 'account':
                find_count += string in element.username.lower()

        if (find_count == len(strings)) and (element not in dst_queryset):
            result.append(element)

    return result

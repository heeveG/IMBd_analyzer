#!/usr/bin/python
# -*- coding: utf-8 -*-


def find_movies(actor):
    """
    (str) -> list

    Returns a list with a set of the tconst of most popular movies, list of \
    more info and nm
    e.g. find_movies('Tom Cruise')
    [{'tt0092099', 'tt0325710', 'tt0116695', 'tt0120755'}, \
['1962', 'actor,producer,soundtracker'], 'nm0000129']
    """

    # names.tsv - name.basics.tsv.gz

    f = open('names.tsv', encoding='utf-8')
    info = list()
    movies = set()
    general = [movies, info]
    for line in f:
        splt = line.split('\t')
        if actor in splt[1]:
            nm = splt[0]
            info.append(splt[2])
            about = splt[4].replace('soundtrack', 'soundtracker')
            info.append(about)
            best = splt[5].split(',')
            for i in best:
                i = i.replace('\n', '')
                movies.add(i)
            general.append(nm)
            break
    f.close()
    return general


def identify_movie(general):
    """
    (set) -> dict

    Returns a dict with a movie as a key, a tconst, a start year and genres \
    for this movie as a value
    >>> identify_movie({'tt0120755'})
    {'Mission: Impossible II': ['tt0120755', '', '2000', \
'Action,Adventure,Thriller']}
    """

    # title.tsv - title.basics.tsv.gz

    if type(general) != set:
        movie_set = general[0]
    else:
        movie_set = general
    f = open('title.tsv', encoding='utf-8')
    real_movies = dict()
    for line in f:
        splt = line.split('\t')
        if splt[0] in movie_set:
            var = splt[8].replace('\n', '')
            real_movies[splt[2]] = [splt[0], '', splt[5], var]
        if len(real_movies) == len(movie_set):
            break
    f.close()
    return real_movies


def find_rating_info(movies):
    """
    (dict) -> dict

    Returns a dict with a movie as a key and a list with avarage rating and\
    number of people rated as a value
    >>> print(find_rating_info({'Top Gun': \
['tt0092099', '', '1986', 'Action,Drama']}))
    {'Top Gun': ['6.9', '254510']}
    """

    counter = 0

    # counter is needed to stop iterating when found all needed data
    # rating.tsv - title.ratings.tsv.gz

    f = open('rating.tsv', encoding='utf-8')
    rating_dct = dict()
    for line in f:
        splt = line.split('\t')
        for (key, value) in movies.items():
            if splt[0] in value[0]:
                avrg = splt[1]
                total = splt[2].replace('\n', '')
                rating_dct[key] = [avrg, total]
                counter += 1
        if counter == len(movies):
            break
    f.close()
    return rating_dct


def find_all(rating, movies):
    """
    (dict, dict) -> dict

    Retuns a dictionary with a film as a key and list of year and date as value
    >>> print(find_all({'Top Gun': ['6.9', '254510']}, \
{'Top Gun': ['tt0092099', '', '1986', 'Action,Drama']}))
    {'Top Gun': ['1986', '6.9', '254510']}
    """

    all_rtng = dict()
    for (key1, value1) in rating.items():
        for (key2, value2) in movies.items():
            if key1 == key2:
                year = value2[2]
                total = value1[1]
                rate = value1[0]
                all_rtng[key1] = [year, rate, total]
    return all_rtng


def find_most_popular(all_ratings):
    """
    (dict) -> list

    Returns a list with movie, year it was filmed and rating
    >>> print(find_most_popular({'Top Gun': ['1986', '6.9', '254510']}))
    ['Top Gun', '6.9', '1986', '254510']
    """

    most = ['', 0, 0, 0]
    for (key, value) in all_ratings.items():
        if float(value[1]) > float(most[1]):
            most[0] = key
            most[1] = value[1]
            most[2] = value[0]
            most[3] = value[2]
        elif float(value[1]) == float(most[1]):

                                                 # if same ratings look at num

            if float(most[3]) < float(value[2]):
                most[0] = key
                most[1] = value[1]
                most[2] = value[0]
                most[3] = value[2]
    return most


def assosiated_genres(movie_dict):
    """
    (dict) -> list

    Returns a list with mostly assosiated genres to given actor
    >>> print(assosiated_genres({'Top Gun': ['tt0092099', '', '1986', \
'Action,Drama'], 'Jerry Maguire': ['tt0116695', '', \
'1996', 'Comedy,Drama,Romance']}))
    ['Drama']
    """

    genres = list()
    for (key, value) in movie_dict.items():
        splt = value[3].split(',')
        for i in splt:
            i = i.replace('\n', '')
            genres.append(i)
    most_common = dict()
    for i in genres:
        if i not in most_common.keys():
            most_common[i] = genres.count(i)
    output = list()
    for (key, value) in most_common.items():
        if value == max(most_common.values()):
            output.append(key)
    return output


def title_akas(title):
    """\n    (str) -> list\n\n    Returns a list with all info about a title\n    e.g. :\n    [['Jerry Maguire', 'ES'], ['Jerry Maguire', 'original'], ['Jerry Maguire', 'SI'], ['Jerry Maguire: Spiel des Lebens', 'AT'], ['Jerry Maguire - El\xc3\xa4m\xc3\xa4 on peli\xc3\xa4', 'FI'], ['Jerry Maguire - Seducci\xc3\xb3n y desaf\xc3\xado', 'AR'], ['D\xc5\xbeeri Megvajer', 'RS'], ['Jerry Maguire', 'US'], ['Jerry Maguire', 'HR'], ['Jerry Maguire', 'PT'], ['Jerry Maguire, a Grande Virada', 'BR']]\n    """

    akas_title = list()

    # akas.tsv - title.akas.tsv.gz

    f = open('akas.tsv', encoding='utf-8')
    counter = 0
    for line in f:
        splt = line.split('\t')
        if title == splt[0]:
            counter += 1
            if splt[5] != 'original':
                akas_title.append([splt[2], splt[3]])
            elif splt[5] == 'original':
                akas_title.append([splt[2], 'original'])
        if splt[1] != 'ordering':
            if counter > int(splt[1]):
                break
    f.close()
    return akas_title


def find_all_movies(actor):
    """
    (str) -> set
    Returns a set with all movies given actor has starred in

    """

    all_movies = set()

    # principals.tsv - title.principals.tsv.gz

    f = open('principals.tsv', encoding='utf-8')
    for line in f:
        splt = line.split('\t')
        if splt[2] == actor:
            all_movies.add(splt[0])
    f.close()
    return all_movies


def find_avrg_rating(all_movies):
    """
    (set) -> list
    Retuns a list with sum of all ratings and number of votes to given films
    e.g.: [59694374.900000095, 8306836.0]
    """

    avg_rating = list()
    rating = 0
    num = 0
    counter = 0

    # rating.tsv - title.ratings.tsv.gz

    f = open('rating.tsv', encoding='utf-8')
    for line in f:
        splt = line.split('\t')
        if splt[0] in all_movies:
            counter += 1
            rating += float(splt[1]) * float(splt[2])
            num += float(splt[2])
        if counter == len(all_movies):
            break
    avg_rating.append(rating)
    avg_rating.append(num)
    f.close()
    return avg_rating

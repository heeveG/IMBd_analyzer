from imdb import *
from files import *

def main():
    rating_input = dict()
    actor = input("Hey! Enter a name and a surname of an actor and get a quiz: \n")
    movies = find_movies(actor)

    while len(movies[0]) == 0 or len(actor.split()) < 2:
        actor = input("Reenter your actor please!\n")
        movies = find_movies(actor)

    real_movies = identify_movie(movies)
    rating_dct = find_rating_info(real_movies)

    lst = []
    for i in rating_dct.keys():
        lst.append(i)

    print('---')
    print("{}, born in {}, mostly known for being a/an {}.\nStarred in '{}', \
    '{}', '{}' and '{}'".format(actor, \
                                movies[1][0], \
                                movies[1][1], lst[0], lst[1], lst[2], lst[3]))
    print('---')

    num = 0
    while num < len(lst):
        film = lst[num]
        print("Have you watched {}?".format(film))
        ans = input("Answer 'yes' or 'no': \n")
        if ans == 'no':
            print("You should watch it then! Its rating is {} according to {}\
     people\n".format(rating_dct[film][0], rating_dct[film][1]))
        elif ans == 'yes':
            rating = input("Rate it from 1 to 10:\n")
            while float(rating) < 0 or float(rating) > 10:
                rating = input("Please, reenter your rating!\n")
            rating_input[film] = \
                [rating_dct[film][1], rating, rating_dct[film][0]]
            print("Your answer: {}, {} people according to IMDb rated '{}' : {}" \
                  .format(rating, rating_dct[film][1], \
                          film, rating_dct[film][0]))
        num += 1

    all_rtng = find_all(rating_dct, real_movies)
    most = find_most_popular(all_rtng)
    genres = assosiated_genres(real_movies)
    more_info = input("Choose a film, which title's translations you want:\n\
    '{}', '{}', '{}', '{}', or type 'skip'\n"\
    .format(lst[0], lst[1], lst[2], lst[3]))

    akas = []
    for key, value in real_movies.items():
        if more_info == key:
            akas = title_akas(value[0])
            break
    if len(akas) > 0:
        for list in akas:
            print("'{}' on {} would be '{}'.".format(more_info, list[1], list[0]))
    else:
        print('You have skipped the translations')
    print('\nMore info about {} is coming!\n'.format(actor))
    all_movies_tconst = find_all_movies(movies[2])
    avg_rating_actor = find_avrg_rating(all_movies_tconst)
    print('---')
    print("~ Avarage {}'s rating, for all movies he/she has starred in, is {}" \
          .format(actor, round(avg_rating_actor[0] / avg_rating_actor[1], 1)))
    print('---')
    print('~ {} is mostly assosiated with {} genre(s)' \
          .format(actor, " and ".join(genres)))
    print('---')
    print("~ {}'s most successful film is: '{}', which was filmed in {} \
    with rating {}".format(actor, most[0], most[2], most[1]))
    print('---')

    try:
        write_file(rating_input)
    except FileNotFoundError as err:
        create_a_file()
        write_file(rate)

    print("\nYou can check the rating information in 'own_ratings.txt' file")

if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-


def create_a_file():
    """
    Creates two txt files for ratings
    """

    f = open('own_ratings.txt', 'w')
    f.close()


def write_file(rating_input):
    """
    (dict) -> None

    Writes new data to a file
    """

    blank = True

    # blank boolean is used to check weather any info is already stored
    # in 'own_ratings'. If True - means no info is stored

    isIn = False

    # isIn boolean is used to check weather there is already some info about
    # certain movie.

    check_line = False

    # check_line boolean is used to make sure no data is lost. If False -
    # rewrites the data about movie from a previous version of a file.

    f = open('own_ratings.txt', 'r')
    for line in f:
        line = line.split()
        if len(line) > 0:
            blank = False
            lines = f.readlines()  # lines stores all data of previous version
            break
    f.close()
    f = open('own_ratings.txt', 'w')
    if not blank:
        f.write('Movie Title: AVG | numVotes | alteredIMDb\n')
        for (key, value) in rating_input.items():
            isIn = False
            for line in lines:
                if line.startswith(key):
                    isIn = True
                    line = line.split('|')
                    avg = float(line[1])
                    numVotes = float(line[2].replace('\n', ''))
                    newVal = (float(value[1]) + avg * numVotes) \
                        / (numVotes + 1)
                    newNum = int(numVotes + 1)
                    lt = (float(value[0]) * float(value[2]) + newVal
                          * newNum) / (float(value[0]) + newNum)
                    f.write('{}: | {} | {} | {}\n'.format(key,
                            round(newVal, 1), newNum, round(lt, 1)))
            if not isIn:
                lt = (float(value[0]) * float(value[2])
                      + float(value[1])) / (float(value[0]) + 1)
                f.write('{}: | {} | {} | {}\n'.format(key, value[1], 1,
                        round(lt, 1)))
        for line in lines:
            check_line = False
            line = line.split('|')
            for key in rating_input.keys():
                if key in line[0]:
                    check_line = True
            if not check_line:
                f.write('|'.join(line))
    else:

        f.write('Movie Title: AVG | numVotes | alteredIMDb\n')
        for (key, value) in rating_input.items():
            alt = (float(value[0]) * float(value[2]) + float(value[1])) \
                / (float(value[0]) + 1)
            f.write('{}: | {} | {} | {}\n'.format(key, value[1], 1,
                    round(alt, 1)))
    f.close()

import functools as ft
#import math as m
import re

HEADER_RE = re.compile(r'^--([0-9]+),([0-9]+)$')
LINE_RE = re.compile(r'^([0-9]+\.[0-9]*|[0-9]*\.[0-9]+|[0-9]+)$')

def parseFile(filename):
    with open(filename, 'r') as f:
        sections = []
        lines = f.readlines()
        (call, crow, cdays) = (None, None, []) # cpers, crow, cdays
        for l in lines:
            l=l.replace(' ', '').replace('\t', '')

            header_res = HEADER_RE.match(l)
            if header_res is not None:
                if call is not None and crow is not None:
                    sections.append((call, crow, cdays))
                (call, crow, cdays) = (int(header_res.group(1)), int(header_res.group(2)), [])
            else:
                line_res = LINE_RE.match(l)
                if line_res is not None:
                    cdays.append(float(line_res.group()))

        sections.append((call, crow, cdays))

        return sections

def calc_km_reduced(km_days, persons_all, persons_rowing):
    #def a(acc, c):
    #    print(f'c: {c} rounded c: {round(c)}')
    #    return acc+round(c)

    km_all = ft.reduce(lambda acc, c: acc+round(c), km_days, 0)
    #km_all = ft.reduce(a, km_days, 0)
    #print(f'km_all: {km_all}')
    km_reduced = round((persons_rowing/persons_all) * km_all)
    return km_reduced


def main():
    packets = parseFile('./km_test.txt')
    reduced = []
    i = 0
    for (all, rowing, km_days) in packets:
        print(f'Track {i}:')
        print(f'\tall:\t{all}')
        print(f'\trowing:\t{rowing}')
        print('\tkilometers on days:')
        for c in km_days:
            print(f'\t\t| {c}')

        print(f'\tsum:\t{ft.reduce(lambda acc, c: acc+c, km_days, 0)}')
        red = calc_km_reduced(km_days, all, rowing)
        print(f'\treduced:\t{red}')
        reduced.append(red)
        i += 1
        print('\n----------------------\n')

    full_trip = ft.reduce(lambda acc, c: acc+c, reduced, 0)
    print(f'km of this trip seperated by sections: {reduced}')
    print(f'km of this trip: {full_trip}')


if __name__ == '__main__':
    main()

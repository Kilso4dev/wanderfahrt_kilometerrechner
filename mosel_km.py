import functools as ft
import math as m

persons_all = 15
persons_rowing = 14

km_days = [
    46.19,
    41.73,
    21.97,
    43.89,
    40.97,
    54.41,
    47.36,
    65.05,
]

def parseFile(filename):
    with open(filename, 'w') as f:
        lines = f.readlines()
        for l in lines:
            l=l.replace(' ', '')
            l=l.replace('\t', '')

        return lines

def calc_km_reduced(km_days, persons_all, persons_rowing):
    km_all = ft.reduce(lambda acc, c: acc+m.ceil(c), km_days)
    km_reduced = m.ceil((persons_rowing/persons_all) * km_all)
    return km_reduced


def main():
    reduced = calc_km_reduced(km_days, persons_all, persons_rowing)
    print(f'km of this trip: {reduced}')


if __name__ == '__main__':
    main()

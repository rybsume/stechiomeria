"""
Autor: Łukasz Rybski
"""

# zaimportuj potrzebne biblioteki
import re
from sympy import Matrix, lcm

# funkcja balansujaca rownanie reakcji
def balansujRownanie():
    # zmienne globalne potrzebne "na pozniej"
    listaPierwiastkow = []
    macierzPierwiastkow = []

    # uzyskaj dane od uzytkownika
    print("Witaj! To narzedzie pomoze Ci dobrac wspolczynniki reakcji chemicznej.")
    print("Wprowadz SUBSTRATY reakcji. Przyklad: Cu+HNO3")
    substraty = input(
        "Substraty (Uwaga! Narzedzie czule na WIELKOSC znakow): ")
    print("Wprowadz PRODUKTY reakcji. Przyklad: Cu(NO3)2+NO2+H2O")
    produkty = input("Produkty (Uwaga! Narzedzie czule na WIELKOSC znakow): ")

    # usun spacje z inputu uzytkownika jesli je wstawil oraz utworz liste z obu inputow
    substraty = substraty.replace(' ', '').split('+')
    produkty = produkty.replace(' ', '').split('+')

    # funckcja tworzaca macierz o dlugosci 2 z pierwiastkow po prawej i lewej stronie rownania
    def dodajDoMacierzy (pierwiastek, indeks, licznik, strona):
        if (indeks == len(macierzPierwiastkow)):
            macierzPierwiastkow.append([])
            for x in listaPierwiastkow:
                macierzPierwiastkow[indeks].append(0)
        if pierwiastek not in listaPierwiastkow:
            listaPierwiastkow.append(pierwiastek)
            for i in range(len(macierzPierwiastkow)):
                macierzPierwiastkow[i].append(0)
        kolumna = listaPierwiastkow.index(pierwiastek)
        macierzPierwiastkow[indeks][kolumna] += licznik*strona

    # funkcja zajmujaca sie rozbiciem np. H2AsO4 na 2 * H, 1 * As, 4 * O
    def znajdzPierwiastki(segment, indeks, wspolczynnik, strona):
        pierwiastkiOrazLiczby = re.split('([A-Z][a-z]?)', segment)
        i = 0
        while  (i < len(pierwiastkiOrazLiczby) - 1):
            i += 1
            if (len(pierwiastkiOrazLiczby[i]) > 0):
                if (pierwiastkiOrazLiczby[i+1].isdigit()):
                    licznik = int(pierwiastkiOrazLiczby[i+1]) * wspolczynnik
                    dodajDoMacierzy(pierwiastkiOrazLiczby[i], indeks, licznik, strona)
                    i += 1
                else:
                    dodajDoMacierzy(pierwiastkiOrazLiczby[i], indeks, wspolczynnik, strona)

    # funkcja zajmujaca sie rozszyfrowaniem np. (NH4)2SO4 na 2 * NH4, 1 * SO4
    def rozszyfrujZwiazek(zwiazek, indeks, strona):
        # podziel zwiazki na te, ktore zaczynaja sie nawiasem i te ktore nie
        segmenty = re.split('(\([A-Za-z0-9]*\)[0-9]*)', zwiazek)

        #jesli dany segment zaczyna sie nawiasem chcemy go oddzielic od reszty z uwzglednieniem wspolczynnika za nawiasem
        for segment in segmenty:
            if segment.startswith('('):
                segment = re.split('\)([0-9]*)', segment)
                wspolczynnik = int(segment[1])
                segment = segment[0][1:]
            else:
                wspolczynnik = 1

            znajdzPierwiastki(segment, indeks, wspolczynnik, strona)

    # ciag funkcji, ktore koncowo z substratow i produktow tworza macierz pierwiastkow po prawej i lewej stronie
    # rozrzyfrujZwiazek -> znajdzPierwiastki -> dodajDoMacierzy
    for i in range(len(substraty)):
        rozszyfrujZwiazek(substraty[i], i, 1)
    for i in range(len(produkty)):
        rozszyfrujZwiazek(produkty[i], i+len(substraty), -1)

    # rozwiazanie rownania macierzowego za pomoca narzedzii algebry liniowej 
    macierzPierwiastkow = Matrix(macierzPierwiastkow)
    macierzPierwiastkow = macierzPierwiastkow.transpose()
    rozwiazanie = macierzPierwiastkow.nullspace()[0]

    # znalezienie najmniejszych calkowitych wspolczynnikow aby nie bylo np. 1/2 O2, tylko 1 O2
    wielokrotnosc = lcm([wartosc.q for wartosc in rozwiazanie])
    rozwiazanie = wielokrotnosc*rozwiazanie

    # przepisanie macierzy z rozwiazaniem na rownanie reakcji z dobranymi wspolczynnikami
    wspolczynnikiStech = rozwiazanie.tolist()
    output = ""
    for i in range(len(substraty)):
        output += str(wspolczynnikiStech[i][0]) + substraty[i]
        if i < len(substraty) - 1:
            output += " + "
    output += " -> "
    for i in range(len(produkty)):
        output += str(wspolczynnikiStech[i + len(substraty)][0]) + produkty[i]
        if i < len(produkty) - 1:
            output += " + "

    print(output)
    


def main():
    balansujRownanie()


if __name__ == "__main__":
    main()

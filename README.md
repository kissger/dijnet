# dijnet
Dijnet számla listázó/letöltő
előkövetelmény: [MechanicalSoup](https://pypi.org/project/MechanicalSoup/)

## használat

bejelentkezési adatok megadása a .dijnet fájlban a user home mappájában
a fájl formátuma:
```
[AUTH]
username=felhasznalonev
password=jelszo
```

súgó
```bash
python3 dijnet.py -h
usage: python3 dijnet.py [-h] [-f DATEFROM] [-t DATETO] [-d DOWNLOADPATH]

optional arguments:
  -h, --help            show this help message and exit
  -f DATEFROM, --from DATEFROM
                        datum -tol, pl.: "2021.01.01"
  -t DATETO, --to DATETO
                        datum -ig, pl.: "2021.01.31"
  -d DOWNLOADPATH, --download DOWNLOADPATH
                        celmappa letolteshez
```

## példák
lekérdezés adott intervallumból és letöltés a targetDir mappába
```bash
python3 dijnet.py -f 2020.01.01 -t 2020.12.31 -d targetDir
```
lekérdezés adott dátum után és letöltés a targetDir mappába
```bash
python3 dijnet.py --from 2021.01.01 --download targetDir
```
összes elérhető számla lekérdezése és letöltés a targetDir mappába
```bash
python3 dijnet.py -d targetDir
```

## kimenet
az oldalon megjelenő táblázat csv formátumban, a letöltött fájlok nevével kiegszítve, ha a letöltés be volt kapcsolva
```
szolgaltato;szamlakibocsatoi_azonosito;szamlaszam;kiallitas_datum;osszeg;fizetesi_hatarido;fizetendo;allapot;file
```

### more to come...
ELMŰ számla letöltő script coming soon
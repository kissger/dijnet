# dijnet
Dijnet számla letöltő

## használat
bejelentkezési adatok megadása a login metódusban
```python
    browser['username'] = ''
    browser['password'] = ''
```

opcionális letöltés, alapértelmezetten letölti a keresési eredményeket
```python
  # doDownload=True|False - True letölti a számlákat, False nem
  list_invoices(doDownload)
```

lekérdezés adott intervallumból és letöltés a targetDir mappába
```bash
python3 dijnet.py targetDir 2020.01.01 2020.12.31
```
összes elérhető számla lekérdezése és letöltés a targetDir mappába

```bash
python3 dijnet.py targetDir
```
### more to come...

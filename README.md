# Matkalaskuri
Matkalaskuri lenkkejä varten.

Graafisen käyttöliittymän laskuri, jolla on helppo pitää kirjaa esimerkiksi omista pyörälenkeistä. Kirjatuista matkoista voi pyytää kätevästi yhteenvedon tai piirtää kuvaajan. Ohjelmaan voi syöttää myös tavoitteen, jolloin ohjelma näyttää sekä puuttuvan matkan tavoitteen saavuttamiseen että jäljellä olevat päivät.

## Ominaisuudet
- Pidä kirjaa matkoista helposti lisäämällä vain kuljettu matka
- Ylläpidä useita tiedostoja samanaikaisesti. Näiden välillä vaihtelu käy ohjelman sisällä helposti
- Aseta kilometritavoite ja/tai päivämäärätavoite kullekin tiedostolle valitsemalla se helposti kalenterista
- Piirrä kirjatuista matkoistasi kuvaaja tai tarkastele näistä kompaktia yhteenvetoa

## Järjestelmävaatimukset
- Python 3.6+
- `PyQt5` versio 5.10+
- `matplotlib` versio 2.2.2+

Tarvittavien moduulien asennukset voi tarkistaa ajamalla skriptin `check_modules.py`.

## Päivitykset versioon 2.0 (29.8.2018)
- Korjattiin bugi, joka aiheutti ohjelman kaatumisen tarkastellessa listaa jossa ei ole matkoja
- Kirjattavien matkojen minimipituudeksi asetettu 0.1 km
- Siirrettiin tavoitetiedot matkatiedostoon
- Lisättiin mahdollisuus vaihtaa tiedostoa
- Lisättiin mahdollisuus luoda uusia tiedostoja matkoille

## Asennus
1. Lataa kaikki muut tiedostot paitsi cycling_trips.json, ohjelma tekee sen ajaessa automaattisesti oikeaan kansioon. Siirrä nämä haluamaasi kansioon.
2. Aja ohjelma check_modules.py jos et ole varma täyttääkö järjestelmäsi vaatimukset
3. Asenna tarvittavat lisämoduulit
4. Aja main.pyw

## Icons

### icon.ico
Original name: `Emoji_u1f6b4_200d_2642.svg`

### calendar.png
Original name: `Emoji_u1f4c6.svg`

Source: https://github.com/googlei18n/noto-emoji/

## License
GNU General Public License v3.0

Full license: [LICENSE](/LICENSE)

# BlabPrezent
Bot obsługujący loterię prezentową w pewnym serwisie mikroblogowym.

## Ogólne zasady loterii
Zasady zbliżone są do szkolnej loterii mikołajkowej:
1. Chętni zgłaszają się do zabawy pisząc odpowiednią wiadomośc do bota.
2. Drugą fazą jest losowanie kto komu kupuje prezent.
3. Powiadomienie uczestników o wynikach losowania.
4. Uczestnicy potwierdzają wysłanie/odebranie przesyłki pisząc odpowiednią wiadomośc do bota.
5. Olbrzymia radość z otrzymanych prezentów.

## Jak uruchomić?

### Program
Źródła są w katalogu `src`: `cd src`

`pip install -r requirements.txt`

Na podstawie `configuration.toml.sample` stworzyć `configuration.toml`

Uruchomić `bp.py` z odpowiednim parametrem, np `python bp.py bot`

### Testy
`cd src`

`pip install -r requirements-dev.txt`

`pytest`


## Więcej informacji
* **Język:** Python,
* **Główne zależności:** [SQLite](https://www.sqlite.org), [Dynaconf](https://www.dynaconf.com), [slixmpp](https://slixmpp.readthedocs.io/en/latest/), [mechanicalsoup](https://mechanicalsoup.readthedocs.io/en/stable/),
* **Testy**: [pytest](https://docs.pytest.org/en/stable/)
* **Jeszcze więcej** w [wiki](https://github.com/kutzowsky/BlabPrezent/wiki) i [instrukcji użytkownika](https://kutzowsky.github.io/BlabPrezent/)

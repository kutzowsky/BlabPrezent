# BlabPrezent [![Build Status](https://travis-ci.org/kucyk/BlabPrezent.svg?branch=master)](https://travis-ci.org/kucyk/BlabPrezent)
Bot obsługujący loterię prezentową w pewnym serwisie mikroblogowym.

## Ogólne zasady loterii
Zasady zbliżone są do szkolnej loterii mikołajkowej.

1. Chętni zgłaszają się do zabawy pisząc odpowiednią wiadomośc do bota (`Bot.py` w trybie zbierania danych).
2. Drugą fazą jest losowanie kto komu kupuje prezent (`giftassign.py`).
3. Powiadomienie uczestników o wynikach losowania (`GiftAssignmentSender.py`).
4. Uczestnicy potwierdzają wysłanie/odebranie przesyłki pisząc odpowiednią wiadomośc do bota. (`Bot.py` w trybie zbierania potwierdzeń).

## Trochę więcej szczegółów
* **Język:** Python 3
* **Zależności:** patrz `requirements.txt`,
* **Zasada działania:** bot XMPP parsujący wiadomości od bota mikroblogowego, zapisujący dane w bazie SQLite i wysyłający odpowiednie odpowiedzi.

## Chcę pomóc!
Świetnie. Zawsze przyda się więcej chęci, refactoringu, testów, ficzerów, owsa, marchewki i podobnych. Patrz w issues, rób pull requesty i kontaktuj się ze mną.
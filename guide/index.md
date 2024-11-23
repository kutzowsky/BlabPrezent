---
---

# BlabPrezent

## Co to takiego?

BlabPrezent to zabawa, która zapoczątkowana została jeszcze na Blipie i odbywa się na zasadach zbliżonych do loterii mikołajkowych w szkołach, 
czyli losujemy kto i komu robi prezent w tym roku. Najważniejsze róznice są takie, że forma prezentu jest wyraźnie określona i bawią się chętni,
którzy wcześniej się zapisali, a nie automatycznie cała klasa.

## Super, też chcę!

Przeczytaj najpierw całą instrukcję, przeanalizuj spokojnie zasady i zastanów się, czy na pewno chcesz wziąć udział.
**Bycie na liście w dniu jej zamknięcia zobowiązuje Cię do akceptacji zasad zabawy i kupna prezentu wylosowanej osobie.**

## Co na prezent?

BlabPrezent to **książka** (papierowa, ebook lub audiobook).

Zasady ogólne:

* **książka papierowa** może być nowa lub używana (w dobrym stanie),
* **ebook** powinien być kupiony z wykorzystaniem opcji „zrób prezent” by obdarowana osoba dostała unikatowy link do jej pobrania
w co najmniej dwóch formatach (mobi i epub);<br>
książki w wersji cyfrowej są często zabezpieczone cyfrowym znakiem wodnym i warto to sprawdzić przed zakupem,
* **audiobook** również powinien być kupiony używając opcji „zrób prezent” lub innej analogicznej, by obdarowana osoba mogła otrzymać swoją
legalną kopię.
* sugerowana cena prezentu to **70 zł** (wraz z kosztami wysyłki).

Do prezentu możesz dodać kartkę z dedykacją i życzeniami. Możesz też się podpisać lub nie ujawniać swojej tożsamości.

## Terminarz

| Co?                          | Kiedy?                       |
| ---------------------------- | ---------------------------- |
| Rozpoczęcie i zapisy         | 20.11.2024                   |
| Zamknięcie listy uczestników | 27.11.2024 (o północy)       |
| Losowanie                    | 28.11.2024                   |
| Ostateczny termin wysyłki    | 15.12.2024                   |
| Zakończenie                  | Gdy dotrą wszystkie prezenty |

## Polecenia bota

| Co?                      | Jak?                                  |
| ------------------------ | ------------------------------------- |
| Zgłoszenie się do zabawy | [dodaj](#dodanie-do-listy)            |
| Rezygnacja z zabawy      | [usun](#usunięcie-z-listy)            |
| Potwierdzenie wysyłki    | [wyslano](#potwierdzenie-wysłania)    |  
| Potwierdzenie odbioru    | [otrzymano](#potwierdzenie-odebrania) |  

## Zgłoszenia

### Dodanie do listy

Wyślij do użytkownika [blabprezent](https://blabler.pl/dash/blabprezent.html) wiadomość prywatną z komendą "dodaj" i swoimi danymi, np:

`>>blabprezent: dodaj Jan Kucowski Stajenna 2/3 42-123 Koziegłowy 543123456 (papier)`

**Uwaga:** napisz wprost, jaką formę (lub formy) prezentu preferujesz – w ten sposób unikniemy niejasności.
Dopisek może być dowolny, byle zmieścił się razem z danymi i wiadomo było o co chodzi.
Podaj też wszystkie dane potrzebne do tego, by prezent do Ciebie dotarł.

Więcej przykładów:

`>>blabprezent: dodaj janina@kucowska.pl (ebook)`

lub:

`>>blabprezent: dodaj brajaneczek2002@buziaczek.pl (audio)`

albo:

`>>blabprezent: dodaj Irena Mustangowska Aleja Przyjaźni 8/3 Kraków 31-901 eireen.m@gmail.com (wszystkie)`

Możesz dopisać swój numer telefonu. Przyda się, gdy książka będzie wysłana kurierem.

Dozwolone jest także odebranie prezentu w automacie paczkowym, a nie w domu. Warto wtedy upewnić się, czego wymaga operator danego automatu
i podać wszystkie niezbędne dane. Na przykład, oprócz imienia, nazwiska oraz symbolu automatu, może być wymagany też numer telefonu
i adres email nawet, gdy chcemy tylko książkę papierową.

Ogólnie zasada jest taka, że podajemy tyle informacji żeby nadawca nie miał wątpliwości jaką formę prezentu sobie życzymy
i nie było problemów z wysyłką.

**Bot powinien odpowiedzieć, że poprawnie zapisał dane w bazie – tylko wtedy możesz mieć pewność, że uczestniczysz w zabawie.**

Bot odpowiada po pewnej chwili (do kilku minut). Jeśli po tym czasie (i odświeżeniu strony) nie ma żadnej odpowiedzi albo jest taka,
której nie rozumiesz, skontaktuj się z [kouma](https://blabler.pl/dash/kouma.html).

### Modyfikacja danych

Swoje dane zgłoszeniowe można modyfikować póki lista uczestników jest otwarta. W tym celu, należy ponownie użyć komendy "dodaj" z pełnymi,
poprawionymi danymi. **Stary wpis zostanie w całości zastąpiony nowym, a bot powinien ponownie wysłać potwierdzenie.**

### Usunięcie z listy

**Nowość**: jeśli jednak zmienisz zdanie, to możesz usunąć się z listy uczestników poleceniem "usun".

`>>blabprezent: usun`

**Bot powinien wysłac wiadomość z potwierdzeniem usunięcia - tylko wtedy masz pewność, że jednak nie będziesz uczestniczyć w zabawie.**
Pamiętaj, że możesz zrobić to tylko i wyłącznie przed terminem zamknięcia listy uczestników podanym w sekcji [Terminarz](#terminarz).

## Losowanie i wysyłka

Po zakończeniu zbierania danych odbędzie się losowanie, a następnie każdy uczestnik/uczestniczka zostanie powiadomiony
(także za pośrednictwem bota) o tym kogo obdarowuje. W tym miejscu następuje część właściwa, czyli wybór i wysłanie prezentu do osoby,
która przypadła nam w udziale oraz oczekiwanie na swój prezent.

W wyborze prezentu może pomóc tag [biblioteczka](https://blabler.pl/tag/biblioteczka.html), na którym można opisać swoje gusta
czytelnicze oraz podejrzeć co lubi osoba, którą wylosowaliśmy.

Zalecamy wysyłkę w sposób, który pozwala na śledzenie paczki (jeśli możliwy jest wybór kilku opcji).

## Potwierdzenia wysyłki i odbioru prezentów

Jako, że przesyłki lubią czasem chodzić własnymi drogami, potrzebna jest dodatkowa weryfikacja.

### Potwierdzenie wysłania

O wysłaniu prezentu poinformuj bota wiadomością:

`>>blabprezent: wyslano`

**Nowość**: Jeśli chcesz przekazać adresatowi link do śledzenia przesyłki, możesz go dodać po "wyslano":

`>>blabprezent: wyslano https://pony-express.com/tracking/123656335423`

### Potwierdzenie odebrania

Po otrzymaniu prezentu użyj komendy "otrzymano":

`>>blabprezent: otrzymano`

### Potwierdzenia ogólnie

Potwierdzenia skutkują również powiadomieniem drugiej strony. Na przykład po „wysłano” adresat dostanie informację, że prezent ruszył w drogę.

Prezenty w formie elektronicznej również potwierdzamy.

Jeśli chcesz, to możesz pochwalić się prezentem na tagu [blabprezent](https://blabler.pl/tag/blabprezent.html).

## Informacje dodatkowe

Obserwuj tag [blabprezent](https://blabler.pl/tag/blabprezent.html) by być na bieżąco. Jeśli masz pytanie ogólne dotyczące akcji, oznacz je też tym tagiem.

Za całą akcję odpowiada [kouma](https://blabler.pl/dash/kouma.html).
(Ale pamiętajcie, Was jest trochę, on tylko jeden, a doba ma tylko 24 godziny.)

Raz na jakiś czas może zdarzyć się że jedna z przesyłek gdzieś zabłądzi albo się opóźni.
Wszystkie nietypowe sytuacje zawsze da się wyjaśnić na spokojnie. O problemach informuj [kouma](https://blabler.pl/dash/kouma.html).

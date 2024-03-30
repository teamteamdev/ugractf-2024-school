# Ugra CTF School 2024

30 марта 2024 | [Сайт](https://2023.ugractf.ru/)

## Таски

[Canep](tasks/canep/) (enhydra, ppc 200)  
[Картограф](tasks/cartographer/) (sylfn, ppc 150)  
[Выбор из двух вариантов](tasks/finestructure/) (enhydra, forensics 150)  
[Всю руку откусят](tasks/fingergiving/) (enhydra, ctb 100)  
[Просто установи это](tasks/installit/) (udn_t, reverse 250)  
[Medium](tasks/medium/) (purplesyringa, web 200)  
[Стук](tasks/portknocking/) (nsychev, crypto 200)  
[Late Stage Capitalism](tasks/skinparadox/) (purplesyringa, reverse 200)  
[Щелкапча](tasks/snapandgo/) (enhydra, web 50)

## Команда разработки

Олимпиада была подготовлена командой [team Team].

[Никита Сычев](https://github.com/nsychev) — руководитель команды, разработчик тасков и платформы  
[Калан Абе](https://github.com/enhydra) — разработчик тасков  
[Коля Амиантов](https://github.com/abbradar) — инженер по надёжности  
[Ваня Клименко](https://github.com/ksixty) — разработчик сайта и платформы, дизайнер  
[Даниил Новоселов](https://github.com/gudn) — разработчик тасков  
[Алиса Сиренева](https://github.com/purplesyringa) — разработчица тасков  
[Юлия Сиренева](https://github.com/yuki0iq) — разработчица тасков  
[Евгений Черевацкий](https://github.com/rozetkinrobot) — разработчик тасков

## Организаторы

Организаторы Ugra CTF — Югорский НИИ информационных технологий, Департамент информационных технологий и цифрового развития ХМАО–Югры и Департамент образования и науки ХМАО–Югры. Олимпиаду разрабатывает команда [team Team].

## Площадки

В этом году олимпиада прошла на 10 площадках по всей России. Благодарим организации, на базе которых работали площадки, а также всех организаторов на площадках:

* Белоярский — [Школа №3](https://86school3.gosuslugi.ru/)
* Владивосток — [IT-колледж ВВГУ (IThub Владивосток)](https://vvsu.ithub.ru)
* Екатеринбург — [Колледж цифровых технологий](https://it-college.ru/)
* Казань — [Казанский национальный исследовательский технологический университет](https://www.kstu.ru/)
* Москва — [Колледж IThub](https://ithub.ru)
* Пермь — [«Академия первых»](https://academy-1.ru/)
* Санкт-Петербург — [Университет ИТМО](https://itmo.ru/)
* Сургут — [Сургутский государственный университет](https://surgu.ru/)
* Тюмень — [Центр робототехники и автоматизированных систем управления](https://rio-centr.ru/projects/main/robotech/)
* Ханты-Мансийск — [Югорский НИИ информационных тенхологий](https://uriit.ru/)

## Генерация заданий

Некоторые таски создаются динамически — у каждого участника своя, уникальная версия задания. В таких заданиях вам необходимо запустить генератор. Путь к нему доступен в конфигурации таска — YAML-файле — в параметре `generator`.

Генератор запускается из директории задания и принимает три аргумента — уникальный идентификатор участника, директорию для сохранения файлов для участника и названия генерируемых тасков. Например, так:

```bash
../_scripts/kyzylborda-lib-generator 12345 attachments uzh,uzh2
```

Уникальный идентификатор используется для инициализации генератора псевдослучайных чисел, если такой используется. Благодаря этому, повторные запуски генератора выдают одну и ту же версию задания.

Генератор выведет на стандартный поток вывода JSON-объект, содержащий флаг к заданию и информацию для участника, а в директории `attachments` появятся вложения, если они есть.

## Лицензия

Материалы соревнования можно использовать для тренировок, сборов и других личных целей, но запрещено использовать на своих соревнованиях. Подробнее — [в лицензии](LICENSE).
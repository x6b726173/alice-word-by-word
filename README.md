
# Общие сведения
## Описание навыка
Слово за слово - игра с несколькими участниками, конечно, один из которых - бот, любезно озвучиваемый Алисой.

Суть игры в повторении последовательности слов, которая увеличивается с каждым ходом очередного игрока.
Предусмотрено два режима игры:
- А - "Игра один на один" - пользователь играет с ботом.
- Б - "Игра в компании" - компания друзей (> 2 человек) и бот.  

Игровой процесс начинается с одного слова, которое "придумывает" Алиса, пользователь повторяет сказанное слово и
добавляет свое слово и так далее, пока кто-то не допустит ошибку или не будет превышено заранее определенное значение 
максимальной длинны последовательности слов, что в свою очередь является фактом, что пользователь победил... ну вот так)

## Практическое применение
Главными качествами, позволяющими выиграть в данного рода играх является - концентрация и память.
Собственно, о направленности тренировки этих качеств и можно говорить. Игра слово за слово имеет соревновательный момент
и хорошо воспринимается в компаниях детей. 
Из личного опыта: в долгой дороге за рулем "подкидывает" работу мозгу, чтобы он не ушел в спящий режим.

## Термины и определения 
* Диалог - спроектированная последовательность текстовых и озвучиваемых фраз, которыми обменивается пользователь и бот
* Команда - информация, поступающая в форме запроса от пользователя и выраженная виде текстовой фразы и, возможно, 
дополнительных семантических данных (см. nlu)   
* Фаза/Состояние диалога - логический блок, объединяющий фразы и функции обработки Команд по некоторому смысловому признаку.   
* Action - функции, реализующие отдельные действия механики игры и всегда возвращающие булево значение - признак применимости. 
* Handlers - функции, выполняющие формирование ответа на запрос пользователя.  
* Dispatcher - единая структура приложения, в которой зарегистрированы все Handlers 

Для лучшего понимания введённых терминов, имеет смысл посмотреть прилагаемый файл: dialog-v1.xlsx
1. Содержимое этого файла - диалог
2. Выделенные блоки, начинающиеся на символ % - Фазы/состояния диалога
3. Первый столбец - возможные команды пользователя (* - любая команда)
4. text|tts - варианты фраз ответов - содержательная часть Handlers
5. action - описание бизнес-логики. 
 

# Детали реализации

## Зависимости
1. python 3.6+
2. redis - для целей хранения сессионных данных
3. pymorphy2 - для целей нормализации входящих слов и фильтрации не-существительных
4. python-Levenshtein - для целей определения схожести слов
5. aioalice - асинхронная библиотека для взаимодействия с Алисой, примеры которой послужили основой для разработки.
Поэтому выражаю благодарность автору https://github.com/surik00/aioalice - избавил от написания многой рутины.
Однако потребовалось внести изменения в механизм передачи параметров в handlers и filters, поэтому был сделан fork и
в requrements.txt внесена соответствующая запись.

## Структура проекта
* core
    * actions - функции, содержащие в себе логику игры (контроллеры).
    * models - структуры данных, использующиеся для представления информации о конкретной игровой сессии.
    * utils - как и во многих проектах, разные функции, не нашедшие более определенного пристанища.
    * stats_storage - средства работы со статистическим данными, необходимыми для функционирования навыка.
    * words_source - коллекция слов.
      
* dialog.v1.phases - пакет, держащий модули в соответствии с каждой из возможных Фаз диалога.

* dispatcher - содержит переопределяемые классы и функции библиотеки aioalice, изменения поведения которых потребовалось
при разработке данного навыка. 

* app.py - исполняемый файл навыка, инициализирует запуск aiohttp сервера навыка с параметрами, указанными в settings.py
  
# Лирическое отступление
## IDE Excel в разработке навыка "Слово за слово"
Множество редакторов позволяют проектировать диалог, более всех мне понравился dialogflow, но без дополнительной 
интеграционной прослойки он не дружит с Алисой (если сильно хочется - см. dialogflower/JustAI ), поэтому было принято решение проектировать диалог в IDE Excel ). 
Для поставленной задачи и с соблюдением определенного синтаксиса
его возможностей оказалось вполне достаточно. Большим плюсом считаю то, что сразу видно всю комбинацию вариантов запросов
и ответов - нет необходимости множественных переходов и открытий вложенных форм....
Еще одним аргументом в пользу предварительного описания диалога в структуре таблицы является то, 
что планировалась реализация скрипта автоматической генерации структуры данных для использования в Dispatcher, 
собственно который и был реализован, однако в необходимость в нем отпала.... вероятно, пояснение причин превратит данный
readme в статью, поэтому опустим. В качестве итога данного блока лирического отступления хочу зафиксировать правила,
 которые неплохо-бы было соблюсти при разработке:
1. Дизайн диалога первичен. Т.е. сначала все переходы и вариации фраз.
2. Программный код реализации навыка не должен содержать диалоговых фраз (всего того, что есть в dialog.v1)  
3. Handlers - не должны содержать бизнес-логики (условий, вычислений, обращений к сторонним ресурсам и т.д.). 
 
## Что можно доработать 
* формирование пользовательского набора слов
* поддержку английский слов (можно использовать в обучении, на пр. не правильным глаголам - повторяя последовательности)
* ведение общего рейтинга пользователей
* добавить возможность добавить своё слово отдельно после перечисления последовательности
* реализовать обработку команды "сдаюсь" в режиме игры "Игра в команде"
* реализовать возможность записи отзыва пользователя непосредственно в навыке
* исключить дубликаты в ответах бота
* расширить словарный запас бота

*- но все это в следующих версиях )*

# Да, собственно сам навык: [Слово за слово](https://alice.ya.ru/s/9d5dad53-1dd3-4f14-805a-6bc374ec579d) 

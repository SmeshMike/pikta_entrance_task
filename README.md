# pikta_entrance_task

Данный пакет состоит из 3 основных модулей: json_task, http_requests, sql_task

Каждый из модулей выполняет инструкции поставленные в оответствии с заданием.
Папка tests содержит юнит-тесты для каждого модуля.
Папка report содержит coverage report по результатам тестов.

Подробнее о запуске каждого модуля.

**json_task**

Запускается командой *python json_task.py*. Ищет json файлы в директории запуска, при наличии валидных файлов для парсинга создаёт xlsx файл, по данным из json'ов

**http_requests**

Запускается командой *python http_requests.py [ifns] [oktmns]*. Отправляет запрос на сайт ИФНС, выводит результат Платёжных реквизитов в консоль при успешном выполнении.

**sql_task**

Запускается командой *python sql_task.py*. Создаёт в директории запуска файл "sqlite_python.db", куда запиывает данные, после этого осуществляет запросы на поиск нужных элементов и выводит их в консоль.

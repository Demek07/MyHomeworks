--1 Лысые злодеи 90х годов - 94
SELECT name, FIRST_APPEARANCE, APPEARANCES FROM MarvelCharacters WHERE HAIR="Bald" and ALIGN="Bad Characters" and year BETWEEN 1990 and 1999
--2 Герои с тайной идентичностью и необычными глазами - 1080
SELECT name, FIRST_APPEARANCE, EYE FROM MarvelCharacters WHERE identify="Secret Identity" and EYE NOT in ("Blue Eyes", "Brown Eyes", "Green Eyes")
--3 Персонажи с изменяющимся цветом волос - 32
SELECT name, HAIR FROM MarvelCharacters WHERE HAIR="Variable Hair"
--4 Женские персонажи с редким цветом глаз - 5
SELECT name, EYE FROM MarvelCharacters WHERE sex="Female Characters" and EYE in ("Gold Eyes", "Amber Eyes")
--5 Персонажи без двойной идентичности, сортированные по году появления - 1788
SELECT name, FIRST_APPEARANCE FROM MarvelCharacters WHERE identify="No Dual Identity" ORDER BY Year DESC
--6 Герои и злодеи с необычными прическами - 3816
SELECT name, ALIGN, HAIR FROM MarvelCharacters WHERE HAIR NOT in ("Brown Hair", "Black Hair", "Blond Hair", "Red Hair")
--7 Персонажи, появившиеся в определённое десятилетие - 1306
SELECT name, FIRST_APPEARANCE FROM MarvelCharacters WHERE year BETWEEN 1960 and 1969
--8 Персонажи с уникальным сочетанием цвета глаз и волос - 13
SELECT name, EYE, HAIR FROM MarvelCharacters WHERE EYE="Yellow Eyes" and HAIR="Red Hair"
--9 Персонажи с ограниченным количеством появлений - 11939 - ошибка! у меня получается другое количество!
SELECT name, APPEARANCES FROM MarvelCharacters WHERE APPEARANCES<10
--10 Персонажи с наибольшим количеством появлений - 5
SELECT name, APPEARANCES FROM MarvelCharacters ORDER BY APPEARANCES DESC LIMIT 5
--11 Персонажи, появившиеся только в одном десятилетии - 3806 - ошибка! у меня получается другое количество!
SELECT name, FIRST_APPEARANCE FROM MarvelCharacters WHERE year BETWEEN 2000 and 2009
--12 Персонажи с самыми редкими цветами глаз - 34 - - ошибка! у меня получается другое количество!
SELECT name, EYE FROM MarvelCharacters WHERE EYE="Pink Eyes" or EYE="Violet Eyes"
--13 Герои с публичной идентичностью, сортированные по году - 4528
SELECT name, identify, FIRST_APPEARANCE FROM MarvelCharacters WHERE identify="Public Identity" ORDER BY Year
--14 Персонажи с конкретным цветом волос и глаз, упорядоченные по имени - 99
SELECT name, HAIR, EYE from MarvelCharacters WHERE HAIR="Black Hair" and EYE="Green Eyes" ORDER BY name
--15 Злодеи с нестандартными физическими характеристиками - 20
SELECT name, SEX FROM MarvelCharacters WHERE ALIGN="Bad Characters" and SEX NOT IN ("Male Characters", "Female Characters")
--16 Персонажи с наибольшим числом появлений по полу
SELECT name, APPEARANCES FROM MarvelCharacters WHERE sex="Male Characters" or sex="Female Characters" GROUP BY SEX
--17 Сравнение популярности персонажей по цвету волос и глаз
SELECT HAIR, EYE, SUM(APPEARANCES) as Итого FROM MarvelCharacters WHERE HAIR NOTNULL AND EYE NOTNULL GROUP BY HAIR, EYE ORDER BY Итого DESC
--18 Персонажи с максимальным количеством появлений в десятилетие
SELECT name, Year/10*10 as Десятилетие, APPEARANCES AS Появлений FROM MarvelCharacters WHERE Year NOT NULL and year>1940 GROUP BY Десятилетие
--19 Герои и злодеи 80-х
SELECT ALIGN, count(*) AS Количество_Good_Characters FROM MarvelCharacters WHERE (Year BETWEEN 1980 AND 1989) AND ALIGN IN ("Good Characters", "Bad Characters") GROUP BY ALIGN
--20 Самые популярные прически супергероев
SELECT HAIR, APPEARANCES, count(*) as Количество_появлений FROM MarvelCharacters GROUP BY HAIR HAVING HAIR NOT NULL ORDER BY Количество_появлений DESC LIMIT 3
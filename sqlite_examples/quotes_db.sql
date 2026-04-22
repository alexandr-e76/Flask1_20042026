PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS quotes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
author TEXT NOT NULL,
text TEXT NOT NULL
);
INSERT INTO quotes VALUES(1,'Rick Cook','Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы сбольшей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.')
INSERT INTO quotes VALUES(2,'Waldi Ravens','Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.')
INSERT INTO quotes VALUES(3,'Yoggi Berra','В теории, теория и практика неразделимы. На практике это не так.');
COMMIT;

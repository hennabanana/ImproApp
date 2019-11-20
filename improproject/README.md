# README.md

Hendrik Schäfer 

Entwicklung eines App-gesteuerten Improvisationstheaters


## Struktur


| Ort                  | Inhalt                                     |
| -------------------- | ------------------------------------------ |
| `/backend`           | Django Projekt & Backend Configuration     |
| `/backend/api`       | Django App (`/api`)                        |
| `/src`               | Vue App .                                  |
| `/src/main.js`       | JS Entry Point                             |
| `/public/index.html` | Html Entry Point (`/`)                     |
| `/public/static`     | Static                                     |
| `/dist/`             | generierte static files mit (`yarn build`) |

## Vorraussetzungen

 - yarn 
 - pipenv
 - python3
 - redis-server

## Nach Setup

Die Anwendug startet unter http://192.168.178.22::8080/ mit einer leeren Datenbank. Zum Testen folgende Reihenfolge ausführen:
1. Als Spielleiter registrieren und ein Spiel erstellen, dann ausloggen
2. Als Schauspieler registrieren und dem Spiel beitreten, dann ausloggen
3. Als Zuschauer dem Spiel beitreten und Aufgabe verfassen
4. In einem anderen Browser, oder private Session oder anderem Gerät als Schauspieler einloggen
5. In einem anderen Browser, oder private Session oder anderem Gerät als Spielleiter einloggen und Aufgabe abspielen

# Automatisches Setup und starten des Lokalen Servers (Vorraussetzungen erfüllt?)
```
$ bash setuprun.sh
```


# Manuelles Setup und starten des Lokalen Servers (Vorraussetzungen erfüllt?)
```
$ yarn install
$ pipenv install --dev && pipenv shell
$ python manage.py migrate
```

## Entwicklungs Server Lokales Netzwerk

Erst:
```
$ redi-server //protected mode ausgeschaltet? siehe unten
```
dann: Terminal Tab selber Ordner

```
$ python manage.py runserver 192.168.178.22:8000
```

dann neuer Terminal Tab selber Ordner

```
$ yarn serve

```

Die Anwendung wird unter [`192.168.178.22::8080`](http://192.168.178.22::8080/) und die Django Api unter [`192.168.178.22::8000`](http://192.168.178.22::8000/).

In den Dateien /vue.config.js und /src/store/game /und backend/settings/dev.py können Netzwerkeinstellungen verändert werden werden


## Redis - Protected mode?

wenn der proteced mode an ist, währen der redis-server läuft folgedes eingeben:
```
redis-cli
INFO server

CONFIG SET protected-mode no
```
# 

## Probleme

Bei Problemen die Prozesse suchen und beenden und neu versuchen
```
ps aux | grep python
ps aux | grep redis
ps aux | grep yarn
kill -9 ...
```
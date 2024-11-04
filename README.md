### Epok-API
#### Requirements
* Git
* Docker
#### Gör så här
Öppna terminalen och klona repot till din lokala maskin
```Shell
git clone https://github.com/1337adde/epok.git
```
Gå in i mappen
```Shell
cd epok/
```
Bygg containern från Dockerfile, den innehåller Python och nödvändiga bibliotek. Det kan ta en stund om det är första gången.
```Shell
docker build -t fastapi-dev .
```
Starta containern
``` Shell
docker run -d \
  -p 8000:8000 \
  -v $(pwd):/app \
  --name fastapi-app \
  fastapi-dev
```
Surfa till http://localhost:8000/docs för att testa APIet, eller öppna mappen i din IDE.
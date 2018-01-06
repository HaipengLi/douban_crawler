# douban_crawler
input the id of a user, crawl all one's photos in albums
## dependencies
pipenv is used to control the dependencies.

1. install pipenv.
```
pip install pipenv
```
2. install dependencies
```
pipenv install
```
3. enter virtual envirment
```
pipenv shell
```
## usage
```
python AlbumCrawler [user id]
```
for example
```
python AlbumCrawler captainou
```
> The user id can be found in one's main page url.
e.g. `https://www.douban.com/people/captainou/` indicates user id is `captainou`.
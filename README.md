# douban_crawler
## the structure of album in douban.com
- album main page: ‘https://www.douban.com/people/‘+username+’/photos’
    - album page: 'https://www.douban.com/photos/album/'+albumID
    - photos: 'https://img3.doubanio.com/view/photo/l/public/p'+photoID+'.webp'
```json
collectionData={
  albumID:{
    'count':0,
    'pictures':128312123
  }
}
```
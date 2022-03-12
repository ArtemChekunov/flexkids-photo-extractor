# flexkids-photo-extractor

## Motivations

My kid is in kinderopvang which hosted by flexkids.nl
So I wrote a tool for fetching photos of my kid.
If your kinderopvang is also hosted by flexkids.nl feel free to use the photo extractor.

## Usage
First, you need to install  https://pypi.org/project/pipenv/
than install dependencies and run the tool

**example:**
```shell
pipenv install
pipenv run ./main.py --url $FLEXKIDS_URL --login $FLEXKIDS_LOGIN --password $FLEXKIDS_PASSWORD

t=2022-03-12 22:34:21,033 level=INFO msg=init session: https://mykinderopvang.flexkids.nl
t=2022-03-12 22:34:21,617 level=INFO msg=fetching albums
t=2022-03-12 22:34:22,275 level=INFO msg=fetching photos from 2022/3
t=2022-03-12 22:34:25,228 level=INFO msg=fetch photo: photos/2022/3/502892.jpg
t=2022-03-12 22:34:26,449 level=INFO msg=fetch photo: photos/2022/3/502891.jpg
t=2022-03-12 22:34:27,737 level=INFO msg=fetch photo: photos/2022/3/502890.jpg
...
```

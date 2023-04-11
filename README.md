## Outdated
**The module has been fully rewritten in JavaScript, and has become an integral part of**
[shinden-client-electron](https://github.com/Tsugumik/shinden-client-electron/tree/main/src/api). 

**This module can still be used, but there is no guarantee that it will work.**

# shindenpl-master
A module that allows you to get data about anime from shinden.pl, including generating links to players.

**Requirements:**
 - Python 3
 - Internet connection
 - Headers (headersapp) of the connection with the shinden.pl website
 - Headers (headersapi) of the connection with api4.shinden.pl
 - Authkey: **X2d1ZXN0XzowLDUsMjEwMDAwMDAsMjU1LDQxNzQyOTM2NDQ%3D** - It can change

**Required modules:**
 - **BeautifulSoup** from **bs4**
 - **json**
 - **requests**
 - **sleep** from **time**

Example of use:
You must have a serieslink.
This is an example of a full link: 

> https://shinden.pl/series/12434-hunter-x-hunter-2011

And this is serieslink: 

> /series/12434-hunter-x-hunter-2011

Sample command syntax

```python
myAnime = Anime(headersapp=headersapp, headersapi=headersapi, authkey=auth, seriesurl='/series/12434-hunter-x-hunter-2011')
```
An example with all requirements
**You no longer need to add a cookie to your headersapi!**
```python


    from shindenanime import Anime
    
	auth = 'X2d1ZXN0XzowLDUsMjEwMDAwMDAsMjU1LDQxNzQyOTM2NDQ%3D'

	headersapp = {
		"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"Accept-Language": 'pl,en-US;q=0.7,en;q=0.3'
	}
	
	headersapi = {
		"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        	"accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        	"cache-control": "max-age=0",
        	"referer": "https://shinden.pl/",
        	"sec-fetch-dest": "document",
        	"sec-fetch-mode": "navigate",
        	"sec-fetch-site": "same-origin",
        	"sec-fetch-user": "?1",
		"sec-gpc": "1",
        	"upgrade-insecure-requests": "1",
        	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
	}


	myAnime = Anime(headersapp=headersapp, headersapi=headersapi, authkey=auth, seriesurl='/series/12434-hunter-x-hunter-2011')
	
	pldict = myAnime.get_players(episode=0)

	for index, item in  enumerate(pldict):
		print(f'[{index}] {pldict[item]}')

	 
	print(myAnime.gen_video_link(playerid="794697"))
	
```
Everything is counted from 0 ! For example, the first episode will be marked with 0.
Functions:

 - **get_rating**
 Returns the anime's rating as float.
 - **get_image_link**
 Returns a link to thumb as string.
 - **get_episodes_dict**
 Returns a dictionary with the structure 
	> linktoepisode: title


	The title will change to X when it is not defined on the page.
- **get_episodes_list**
Returns a link list of episodes.
- **get_pagesource_episodes**
Returns the source of the page containing the episode list. Useful for debugging.
- **get_episodes_titles**
Returns a list of episode titles.
- **get_players(episode: int)**
Returns a dictionary containing the players for the given episode.
For example
```python
myAnime = Anime(headersapp=headersapp, headersapi=headersapi, authkey=auth, seriesurl='/series/16217-0')
print(myAnime.get_players(episode=0)
```
Will give effect
```json
{"0": {"Cda": {"id": "590072", "max_res": "720p", "lang_subs": "pl"}}}
```	    
  

- **gen_video_link(playerid: str)**
Returns a link to the player that can be used in the browser.
We need the id we get from get_players.
**Generating a link takes at least 5 seconds to get the link from the API.**
For example
```python
print(myAnime.gen_video_link(playerid="590072"))
```
Will give effect

> //ebd.cda.pl/800x450/35129382c

## I wrote this just for fun, so it may contain errors !

## Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

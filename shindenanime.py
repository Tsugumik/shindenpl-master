import requests
import json
from bs4 import BeautifulSoup
from time import sleep


class Anime:
    def __init__(self, headersapp: dict, headersapi: dict, authkey: str, seriesurl: str):
        self.__seriesurl = seriesurl
        self.__authkey = authkey
        self.__headers = headersapp
        self.__headersapi = headersapi

    @property
    def get_rating(self) -> float:
        qurl = 'https://shinden.pl{}'.format(self.__seriesurl)
        page = requests.get(qurl, headers=self.__headers)
        pagesoup = BeautifulSoup(page.content, 'html.parser')
        rating = pagesoup.find('span', {'class': 'info-aside-rating-user'}).text
        rating = rating.replace(',', '.')
        rating = float(rating)
        return rating

    @property
    def get_image_link(self) -> str:
        qurl = 'https://shinden.pl{}'.format(self.__seriesurl)
        page = requests.get(qurl, headers=self.__headers)
        pagesoup = BeautifulSoup(page.content, 'html.parser')
        link = pagesoup.find('img', {'class': 'info-aside-img'})
        img_link = 'https://shinden.pl'+link.get('src')
        return img_link

    @property
    def get_episodes_dict(self) -> dict:
        qurl = 'https://shinden.pl{}'.format(self.__seriesurl) + '/all-episodes'
        page = requests.get(qurl, headers=self.__headers)
        pagesoup = BeautifulSoup(page.content, 'html.parser')
        aa = pagesoup.find_all('a', {'class': 'button active'})
        titles = pagesoup.find_all('td', {'class': 'ep-title'})
        episodes = list()
        titlesl = list()
        done_episodes = dict()
        for a in aa:
            episodes.append(a.get('href'))
        episodes.reverse()
        for title in titles:
            titlesl.append(title.text)
        titlesl.reverse()
        for index, item in enumerate(episodes):
            if len(titlesl) < 1:
                done_episodes[item] = 'X'
            elif titlesl[index] == '':
                done_episodes[item] = 'X'
            else:
                done_episodes[item] = titlesl[index]
        return done_episodes

    @property
    def get_episodes_list(self) -> list:
        # Episodes without titles
        qurl = 'https://shinden.pl{}'.format(self.__seriesurl) + '/all-episodes'
        page = requests.get(qurl, headers=self.__headers)
        pagesoup = BeautifulSoup(page.content, 'html.parser')
        aa = pagesoup.find_all('a', {'class': 'button active'})
        episodes = list()
        for a in aa:
            episodes.append(a.get('href'))
        episodes.reverse()
        return episodes

    @property
    def get_pagesource_episodes(self) -> bytes:
        qurl = 'https://shinden.pl{}'.format(self.__seriesurl)+'/all-episodes'
        page = requests.get(qurl, headers=self.__headers)
        return page.content

    @property
    def get_episodes_titles(self) -> list:
        # Dictionary title:link
        qurl = 'https://shinden.pl{}'.format(self.__seriesurl) + '/all-episodes'
        page = requests.get(qurl, headers=self.__headers)
        pagesoup = BeautifulSoup(page.content, 'html.parser')
        titles = pagesoup.find_all('td', {'class': 'ep-title'})
        titlesl = list()
        for title in titles:
            titlesl.append(title.text)
        titlesl.reverse()
        return titlesl

    def get_players(self, episode: int) -> dict:
        print('Wait...')
        episodes = self.get_episodes_list
        try:
            episode = episodes[episode]
        except IndexError:
            raise Exception("Wrong episode number!")
        qurl = 'https://shinden.pl{}'.format(episode)
        page = requests.get(qurl, headers=self.__headers)
        pagesoup = BeautifulSoup(page.content, 'html.parser')
        players = pagesoup.find_all('a', {'class': 'button AD-RC-300x250 change-video-player'})
        players_done = list()
        players_for_user = dict()
        for player in players:
            players_done.append(player.get('data-episode'))
        for index, item in enumerate(players_done):
            if not item: pass
            jsondata = json.loads(players_done[index])
            pid = jsondata['online_id']
            name = jsondata['player']
            max_res = jsondata['max_res']
            lang_subs = jsondata['lang_subs']
            players_for_user['{}'.format(index)] = dict()
            players_for_user['{}'.format(index)][name] = dict()
            players_for_user['{}'.format(index)][name]['id'] = pid
            players_for_user['{}'.format(index)][name]['max_res'] = max_res
            players_for_user['{}'.format(index)][name]['lang_subs'] = lang_subs
        return players_for_user

    def gen_video_link(self, playerid: str) -> str:
        url1 = 'https://api4.shinden.pl/xhr/{}/player_load?auth={}'.format(playerid, self.__authkey)
        url2 = 'https://api4.shinden.pl/xhr/{}/player_show?auth={}&width=0&height=-1'.format(playerid, self.__authkey)
        requests.get(url1, headers=self.__headersapi)
        print('Wait 5 seconds')
        sleep(5)
        response = requests.get(url2, headers=self.__headersapi)
        soup = BeautifulSoup(response.text, 'html.parser')
        iframe = soup.find('iframe')
        if iframe==None:
            raise Exception("Wrong headersapi or wrong episode number!")
        try:
            gen_link = iframe.get('src')
        except AttributeError:
            print("Attribute Error !")
            raise Exception("Wrong headersapi or wrong episode number!")
        return gen_link

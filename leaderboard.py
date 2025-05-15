
import pywhatkit
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import player
import json
import time

selected_players_latest_score = {}
selected_player_list = set()
players = []


def send_leaderboard():
    msg = "```player score\n"
    msg += "\n".join([f"{p.name} {p.score}" for p in sorted(players, key= lambda p: p.score)])
    msg += "```"
    print(msg)
    pywhatkit.sendwhatmsg_to_group_instantly('FNbvGgai5vQJyrsJiN1i1i', msg)


def update_leaderboard():
    [p.update_score(selected_players_latest_score) for p in players]


def parse_espn():
    req = Request('https://www.espn.com/golf/leaderboard/_/tournamentId/401703504',
                  headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, features="html.parser")
    for content in soup.find_all('td', {'class': 'tl plyr Table__TD'}):
        player_name = str(content.text)
        if player_name in selected_player_list and player_name not in selected_players_latest_score:
            selected_players_latest_score.update({player_name: content.nextSibling.text})
    print(selected_players_latest_score)


def load_players():
    global players
    global selected_player_list
    with open('player_details_masters_2025.json', 'r', encoding='utf-8') as selected_players_json:
        players_json = json.load(selected_players_json)
    for p in players_json:
        selected_player_list |= set(p['selected_five'])
    players = [player.Player(**p) for p in players_json]


if __name__ == '__main__':
    print('running leaderboard')
    while True:
        load_players()
        parse_espn()
        print(f"{"\n".join([f"{p.name} {p.score} {p.selected_five}" for p in sorted(players, key= lambda p: p.score)])}")
        print(f"selected_players={selected_player_list}")
        update_leaderboard()
        send_leaderboard()
        print('done. sleeping for 30 minutes...')
        time.sleep(10)

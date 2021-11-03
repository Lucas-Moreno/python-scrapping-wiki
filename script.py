import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
software_names = [SoftwareName.ANDROID.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MAC.value]   

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=1000)

# Get list of user agents.
user_agents = user_agent_rotator.get_user_agents()
user_agent_random = user_agent_rotator.get_random_user_agent()

header = {}
links = []
url = 'https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Rappeur_fran%C3%A7ais'
header['User-Agent'] = user_agent_rotator.get_random_user_agent()
response = requests.get(url, headers=header)

if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')
    groupeByNameArtists = soup.findAll('div', {'class' : 'mw-category-group'})
    for artist in groupeByNameArtists:
        lis = artist.findAll('li')
        for li in lis:
            a = li.find('a')
            link = a['href']
            links.append('https://fr.wikipedia.org/' + link)



with open('data.csv', 'w') as outf:
    outf.write('name\n')
    for link in links:
        response = requests.get(link, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
        nameArtists = soup.find('h1').text
        outf.write(nameArtists + '\n')

import bonobo
from bonobo.config import use
import requests
from bs4 import BeautifulSoup
import http
import re
from datetime import datetime
from db.base import Base, Session, engine
from db.event import Event
from db.program import Program
from db.artist import Artist


EVENTS_URL = 'https://www.lucernefestival.ch/en/program/summer-festival-22'

Base.metadata.create_all(engine)

session = Session()

@use('http')
def extract_links(http):
    """Placeholder, change, rename, remove... """
    res = http.get(EVENTS_URL)

    if(res.status_code != 200):
        return "Response" + res.status_code

    content = BeautifulSoup(res.content, 'html.parser').find_all("p", attrs={"class": "event-title h3"})
    event_links = [content.find('a').get('href') for content in content]
    yield from event_links

def transform_links(link):
    return EVENTS_URL.split('/en')[0] + link

def transform(*args):
    """Placeholder, change, rename, remove... """
    yield tuple(
        map(transform_links, args)
    )


def extract_information(*args):
    res = requests.get(*args)
    if res.status_code != 200:
        return 'Request error to the address: ' + args[0]
    base_url = EVENTS_URL.partition("/en")[0]
    content = BeautifulSoup(res.content, 'html.parser')
    artists = [re.sub(r'\t]*','',performer.text).strip().split('\n')[0] for performer in content.find_all('li', attrs={'class': 'cell medium-6 p'})]
    event_date = (content.find('time', attrs={'class': 'date-item h2'}).text + str(datetime.now().year)).split(' ')[-1]
    event_place = content.find_all("div",attrs={"class":"cell medium-9"})[-1].find_all('p')[-1].text
    title = content.find('h1').text
    event_time = content.find('div', attrs={'class': 'cell large-6 subtitle'}).text.split('|')[1].replace('.', ':')
    event_img = base_url + content.find("img").get('src')
    works = [re.sub(r'[\n\t]*','',work.text) for work in content.find('div', attrs={'class': 'cell medium-9'})
                                            .find_all('div', attrs={'class': 'program-item p'})]
    yield title, event_date, event_time, event_place, event_img, artists, works

def load(*args):
    print(*args)
    title, event_date, event_time, event_place, event_img, artists, works = args
    event = Event(title, event_date, event_time, event_place, event_img)
    event.artist = [Artist(artist) for artist in artists]
    event.program = [Program(program) for program in works]
    session.add(event)
    session.commit()
    session.close()




def get_graph(**options):
    """
    This function builds the graph that needs to be executed.

    :return: bonobo.Graph

    """
    graph = bonobo.Graph()
    graph.add_chain(extract_links,bonobo.Limit(20), transform, extract_information, load)

    return graph


def get_services(use_cache=False,**options):
    """
    This function builds the services dictionary, which is a simple dict of names-to-implementation used by bonobo
    for runtime injection.

    It will be used on top of the defaults provided by bonobo (fs, http, ...). You can override those defaults, or just
    let the framework define them. You can also define your own services and naming is up to you.

    :return: dict
    """
    if use_cache:
        from requests_cache import CachedSession
        http = CachedSession('http.cache')
    else:
        import requests
        http = requests.Session()
    return {
        'http': http
    }


# The __main__ block actually execute the graph.
if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    parser.add_argument('--use-cache', action='store_true', default=True)
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(**options),
            services=get_services(**options)
        )
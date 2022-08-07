import bonobo
import requests
from bs4 import BeautifulSoup
from datetime import date




EVENTS_URL = 'https://www.lucernefestival.ch/en/program/summer-festival-22'


def extract():
    """Placeholder, change, rename, remove... """
    res = requests.get(EVENTS_URL)
    if(res.status_code != 200):
        return "Response" + res.status_code
    
    soup = BeautifulSoup(res.content, 'html.parser').find_all("li", attrs={"class": "event-item fl-clr yellow"})
    yield from soup


def transform(events,*args):
    """Placeholder, change, rename, remove... """
    base_url = EVENTS_URL.partition("/en")[0]
    img_url = base_url + events.find('source').get('srcset')
    title = events.find('p', attrs={"class": "event-title h3"}).a.text.strip()
    event_date = events.find('div', attrs={"class": "cell xlarge-6 body-small"}).get_text().split()[4].strip() + str(date.today().year)
    event_time = events.find('div', attrs={"class": "cell xlarge-6 body-small"}).get_text().strip().split()[6].replace('.',':')
    event_place = events.find('div', attrs={"class": "cell xlarge-6 body-small"}).get_text().split("|")[-1].strip()
    event_program  = events.findAll('div', attrs={"class": "cell xlarge-6 body-small"})[1].text.split('Program')[-1].strip()
    yield img_url, title, event_date, event_time, event_place, event_program
    

def load(*args):
    """Placeholder, change, rename, remove... """
    print(*args)


def get_graph(**options):
    """
    This function builds the graph that needs to be executed.

    :return: bonobo.Graph

    """
    graph = bonobo.Graph()
    graph.add_chain(extract, transform, load)

    return graph


def get_services(**options):
    """
    This function builds the services dictionary, which is a simple dict of names-to-implementation used by bonobo
    for runtime injection.

    It will be used on top of the defaults provided by bonobo (fs, http, ...). You can override those defaults, or just
    let the framework define them. You can also define your own services and naming is up to you.

    :return: dict
    """
    return {}


# The __main__ block actually execute the graph.
if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(**options),
            services=get_services(**options)
        )
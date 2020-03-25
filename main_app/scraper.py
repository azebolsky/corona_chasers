import json
from urllib.request import urlopen as user_req
from bs4 import BeautifulSoup as soup
from .models import Global, Country, Province


def pop_database():
    # URL That I am scraping
    my_url = "https://coronavirus.m.pipedream.net/"

    # Saves the HTML
    user_client = user_req(my_url)
    page_html = user_client.read()
    user_client.close()

    # Turns HTML into an object/class
    page_soup = soup(page_html, "html.parser")

    # Parses data into Json
    page_dict = json.loads(page_soup.get_text())

    # Sets the values of the global stats (updates if already in database)
    if Global.objects.all().exists():
        g = Global.objects.get(name='Earth')
        g.name = 'Earth'
        g.infected = int(page_dict['summaryStats']['global']['confirmed'])
        g.recovered = int(page_dict['summaryStats']['global']['recovered'])
        g.deaths = int(page_dict['summaryStats']['global']['deaths'])
        g.last_updated = page_dict['cache']['lastUpdated']
        g.save()
    else:
        global_object = Global(
            name='Earth',
            infected=int(page_dict['summaryStats']['global']['confirmed']),
            recovered=int(page_dict['summaryStats']['global']['recovered']),
            deaths=int(page_dict['summaryStats']['global']['deaths']),
            last_updated=page_dict['cache']['lastUpdated'],
        )
        global_object.save()

    num = 0

    for c in Country.objects.all():
        c.infected = 0
        c.recovered = 0
        c.deaths = 0
        c.save()

    for p in Province.objects.all():
        p.infected = 0
        p.recovered = 0
        p.deaths = 0
        p.save()

    # Runs a loop for the amount of provinces/countries
    for all_sets in page_dict['rawData']:
        # If country has no provinces create/update country
        if page_dict['rawData'][num]['Province_State'] == '':
            if page_dict['rawData'][num]['Country_Region'] in Country.objects.all().values_list('name', flat=True):
                c = Country.objects.get(
                    name=page_dict['rawData'][num]['Country_Region'])
                c.name = page_dict['rawData'][num]['Country_Region']
                c.infected = int(page_dict['rawData'][num]['Confirmed'])
                c.recovered = int(page_dict['rawData'][num]['Recovered'])
                c.deaths = int(page_dict['rawData'][num]['Deaths'])
                c.save()
            else:
                country_object = Country(
                    name=page_dict['rawData'][num]['Country_Region'],
                    infected=int(page_dict['rawData'][num]['Confirmed']),
                    recovered=int(page_dict['rawData'][num]['Recovered']),
                    deaths=int(page_dict['rawData'][num]['Deaths']),
                )
                country_object.save()
        else:
            # If country exists update, if not create
            if page_dict['rawData'][num]['Country_Region'] in Country.objects.all().values_list('name', flat=True):
                c = Country.objects.get(
                    name=page_dict['rawData'][num]['Country_Region'])
                c.name = page_dict['rawData'][num]['Country_Region']
                c.infected += int(page_dict['rawData'][num]['Confirmed'])
                c.recovered += int(page_dict['rawData'][num]['Recovered'])
                c.deaths += int(page_dict['rawData'][num]['Deaths'])
                c.save()
            else:
                country_object = Country(
                    name=page_dict['rawData'][num]['Country_Region'],
                    infected=int(page_dict['rawData'][num]['Confirmed']),
                    recovered=int(page_dict['rawData'][num]['Recovered']),
                    deaths=int(page_dict['rawData'][num]['Deaths']),
                )
                country_object.save()

            # If province exists update, if not create
            if page_dict['rawData'][num]['Province_State'] in Province.objects.all().values_list('name', flat=True):
                p = Province.objects.get(
                    name=page_dict['rawData'][num]['Province_State'])
                p.name = page_dict['rawData'][num]['Province_State']
                p.country = Country.objects.get(
                    name=page_dict['rawData'][num]['Country_Region'])
                p.infected += int(page_dict['rawData'][num]['Confirmed'])
                p.recovered += int(page_dict['rawData'][num]['Recovered'])
                p.deaths += int(page_dict['rawData'][num]['Deaths'])
                p.save()
            else:
                if 'Princess' in page_dict['rawData'][num]['Province_State'] or page_dict['rawData'][num]['Province_State'] == 'US':
                    pass
                else:
                    province_object = Province(
                        name=page_dict['rawData'][num]['Province_State'],
                        country=Country.objects.get(
                            name=page_dict['rawData'][num]['Country_Region']),
                        infected=int(page_dict['rawData'][num]['Confirmed']),
                        recovered=int(page_dict['rawData'][num]['Recovered']),
                        deaths=int(page_dict['rawData'][num]['Deaths']),
                    )
                    province_object.save()
        num += 1

pop_database()
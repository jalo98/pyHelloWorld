from bs4 import BeautifulSoup

import ScrapBlog

url = 'https://www.santander.com.ar/banco/online/personas/inversiones/super-fondos/rendimientos'


def main():
    page_source_raw = ScrapBlog.get_page_raw_source_from_url(url)

    my_table_source = page_source_raw

    soup = BeautifulSoup(my_table_source, 'lxml')

    rendimientos = soup.find('div', id='rendimientos')

    my_table = rendimientos.find('table')

    rows = []
    for tr in my_table.find_all('tr')[2:]:
        tds = tr.find_all('td')
        if len(tds) ==8:
            row = {'name': tds[0].text.strip("\n\t").strip(), 'todayValue': tds[3].text.strip("\n\t").strip(), 'deltaDaily': tds[4].text.strip("\n\t").strip(), 'lastThirty': tds[5].text.strip("\n\t").strip(), 'lastNinety': tds[6].text.strip("\n\t").strip(), 'deltaMonth': tds[7].text.strip("\n\t").strip()}

            rows.append(row)


    for row in rows:
        print(
            'Fondo: {name:40}| ValorHoy: {todayValue:11}| VariacionDiaria: {deltaDaily:8}| Ultimos30D: {lastThirty:8}| '
            'Ultimos90D: {lastNinety:8}| VariacionMes: {deltaMonth:8}'.format(**row))

    ScrapBlog.writeToJson(rows, 'found', 'w')


if __name__ == '__main__':
    main()



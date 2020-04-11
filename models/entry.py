import sys

class Entry():

    def __init__(self, event_id, row):

        self.event_id = event_id
        self.car_number = row('td:not([class]):first').text()[1:]

        driver = row('td:not([class])').eq(1).find('a').text()
        self.driver_id = row('td:not([class])').eq(1).find('a').attr('href').split('/')[2].split('-')[0]

        codriver = row('td:not([class]):last > a').text()
        self.codriver_id = None
        if(row('td:not([class]):last > a').attr('href')):
            self.codriver_id = row('td:not([class]):last > a').attr('href').split('/')[2].split('-')[0]

        self.car = row("td.bold").clone().find('span').remove().end().text()
        self.team = row("td.bold > span").text()
        self.plate = row("td.startlist-team > span.startlist-chassis > a").text().replace('[','').replace(']','')
        # TODO TYRES
        self.category = row("td:not(.startlist-m):not(.startlist-sections):last").text()

        #self.championship = row("td.startlist-m").text()
        #self.sections = row("td.startlist-sections").text()

    def getTuple(self):
        self.tuple = (self.event_id, self.car_number, self.driver_id, self.codriver_id, self.team, self.car, self.plate, self.category)

        #print(self.tuple)

        return self.tuple

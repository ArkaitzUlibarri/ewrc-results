import datetime
import logging


def get_href_id(a_tag):
    return a_tag.attr('href').split('/')[2].split('-')[0]


class Leader:

    def __init__(self, tr, event_id, index, pyQuery):
        self.event_id = event_id
        # self.stage_number = tr("td:first > a").text()
        self.stage_number = 'SS' + str(index)
        self.stage_name = tr("td.stats-stage2 > a").text()
        self.drivers = None
        drivers = set(tr("td:last > a").map(lambda i, e: get_href_id(pyQuery(e))))
        if len(drivers):
            self.drivers = drivers
        self.set_timestamps()

    def set_timestamps(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.deleted_at = None

    def get_tuple(self, driver_id):
        self.tuple = (
            self.event_id,
            self.stage_number,
            self.stage_name,
            driver_id,
            self.created_at,
            self.updated_at,
            self.deleted_at
        )

        try:
            logging.info(self.tuple)
        except Exception as e:
            logging.error(e)

        return self.tuple

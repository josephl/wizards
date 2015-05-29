from datetime import datetime
import json
import requests


class WizardsEndpoint(object):
    """Base endpoint"""
    path = NotImplemented

    def __init__(self, base_uri):
        self.base_uri = base_uri

    def get(self, **kwargs):
        """
        :param kwargs: payload options
        """
        raise NotImplementedError()

    @property
    def uri(self):
        return '{0}/{1}'.format(self.base_uri, self.path)


class LocationDetails(WizardsEndpoint):
    path = 'GetLocationDetails'
    method = 'POST'
    headers = {'content-type': 'application/json'}

    _payload_defaults = {
        "BusinessAddressId": None,
        "EarliestEventStartDate": None,
        "EventTypeCodes": [],
        "LatestEventStartDate": None,
        "LocalTime": None,
        "OrganizationId": None,
        "PlayFormatCodes": [],
        "ProductLineCodes": []
    }

    def get(self, **kwargs):
        payload = self._payload(**kwargs)
        return requests.request(self.method, self.uri, data=payload,
                                headers=self.headers)

    def _payload(self, **kwargs):
        """
        :returns: dict params for request
        """
        payload = self._payload.copy()

        # Handle time-based defaults
        today = datetime.date(datetime.now())

        payload.update(kwargs)
        payload = dict(language='en-us', request=payload)
        return json.dumps(payload)


class Locator(object):
    base_uri = 'http://locator.wizards.com/Service/LocationService.svc'

    def __init__(self):
        self.location_details = LocationDetails(self.base_uri)


class WizardsClient(object):

    def __init__(self):
        self.locator = Locator()

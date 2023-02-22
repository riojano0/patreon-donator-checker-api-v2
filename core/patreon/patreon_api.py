import os

import urllib.parse
import requests

API_PREFIX = "https://www.patreon.com/api/oauth2/v2/{}"

DEFAULT_MEMBER_FIELDS = [
    "email",
    "full_name",
    "is_follower",
    "last_charge_date",
    "last_charge_status",
    "lifetime_support_cents",
    "currently_entitled_amount_cents",
    "patron_status"
]

DEFAULT_MEMBER_INCLUDES = [
    "user"
]


class PatreonApi:

    def __init__(self, access_token=None):
        self.access_token = os.environ.get('ACCESS_TOKEN', access_token)

    def __get_initial(self, suffix):
        response = requests.get(
            API_PREFIX.format(suffix),
            headers={
                'Authorization': "Bearer {}".format(self.access_token),
                'User-Agent': "patreon-donator-checker-api-v2",
            }
        )

        response_json = response.json()

        if response_json.get('errors'):
            return response_json

        return response_json

    def get_campaign_members(self, campaign_id, page_size=None, cursor=None, fields=[], includes=[]):
        params = {
            'page[count]': page_size if page_size is not None else 50,
        }

        if fields is not None and len(fields) > 0:
            params.update({'fields[member]': ",".join(fields)})
        else:
            params.update({'fields[member]': ",".join(DEFAULT_MEMBER_FIELDS)})

        if includes is not None and len(includes) > 0:
            params.update({'include': ",".join(includes)})
        else:
            params.update({'include': ",".join(DEFAULT_MEMBER_INCLUDES)})

        if cursor is not None:
            params.update({'page[cursor]': cursor})

        suffix = "campaigns/{}/members".format(campaign_id)

        url_suffix = suffix + "?" + urllib.parse.urlencode(params)

        return self.__get_initial(url_suffix)

    def get_all_campaign_members_responses(self, campaign_id, fields=[], includes=[]):
        responses = []
        cursor = None
        while True:
            response = self.get_campaign_members(campaign_id=campaign_id, page_size=500, cursor=cursor, fields=fields,
                                                 includes=includes)
            if response.get('data') is not None:
                responses.append(response)
                cursor = response.get('meta').get('pagination').get('cursors').get('next')
                if cursor is None:
                    break
            else:
                break

        return responses

    def get_member(self, patreon_member_id, fields=[]):
        params = {'include': ",".join(DEFAULT_MEMBER_INCLUDES)}
        if fields is not None and len(fields) > 0:
            params.update({'fields[member]': ",".join(fields)})
        else:
            params.update({'fields[member]': ",".join(DEFAULT_MEMBER_FIELDS)})

        suffix = "members/{}".format(patreon_member_id)

        url_suffix = suffix + "?" + urllib.parse.urlencode(params)

        return self.__get_initial(url_suffix)

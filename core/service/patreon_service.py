from core.domain.api.patreon_response import PatreonResponse, Status, Tier
from core.patreon.patreon_api import PatreonApi


class PatreonService:

    def __init__(self, campaign_id):
        self.campaign_id = campaign_id
        self.patreon_api = PatreonApi()

    def get_all_patreon_members(self):
        responses = self.patreon_api.get_all_campaign_members_responses(campaign_id=self.campaign_id)
        patreon_response_list = []
        for response in responses:
            data = response.get('data')
            for patreon_body in data:
                patreon_response = self.create_patreon_response(patreon_body)

                patreon_response_list.append(patreon_response)

        return patreon_response_list

    def get_patreon(self, id_uid_patreon):
        response = self.patreon_api.get_member(id_uid_patreon)
        if response is None:
            return "Not Found user {}".format(id_uid_patreon)

        return self.create_patreon_response(response.get('data'))

    @staticmethod
    def create_patreon_response(patreon_body):
        patreon_response = PatreonResponse(
            patreon_uid=patreon_body.get('id'),
            user_id=patreon_body
                .get('relationships')
                .get('user')
                .get('data')
                .get('id')
        )
        attributes = patreon_body.get('attributes')
        if attributes is not None:
            email = attributes.get('email')
            if email is None:
                return patreon_response
            patreon_response.username = email.split('@')[0]
            patreon_response.mail = email

            is_declined_or_paused = attributes.get('patron_status') != 'active_patron'

            current_tier = attributes.get('currently_entitled_amount_cents')
            if is_declined_or_paused:
                patreon_response.status = Status.INACTIVE.value
            else:
                patreon_response.status = Status.ACTIVE.value
                if current_tier == 100:
                    patreon_response.tier = Tier.TIER_1
                elif current_tier == 300:
                    patreon_response.tier = Tier.TIER_2
                elif current_tier == 500:
                    patreon_response.tier = Tier.TIER_3
        return patreon_response

import json
import logging

logger = logging.getLogger("aries_controller.models.presentation")


class Presentation():
    def __init__(self, presentation_json):
        try:
            self.json_data = json.loads(presentation_json)
        except Exception:
            logger.error("Failed to load presentation JSON")
            raise
        self.validate_presentation_json(presentation_json)
        if not self.is_verified():
            logger.error('Presentation Object Verification not verified')
            raise Exception('Presentation Object Verification not verified')

    def get_self_attested_attrs(self):
        if self.is_verified():
            data = {}
            for (name, val) in self.json_data['presentation']['requested_proof']['self_attested_attrs'].items():
                data[name] = val['raw']
            return json.dumps(data)

    def get_revealed_attrs(self):
        if self.is_verified():
            data = {}
            for (name, val) in self.json_data['presentation']['requested_proof']['revealed_attrs'].items():
                data[name] = val['raw']
            return json.dumps(data)

    def get_unrevealed_attrs(self):
        if self.is_verified():
            data = {}
            for (name, val) in self.json_data['presentation']['requested_proof']['unrevealed_attrs'].items():
                data[name] = val['raw']
            return json.dumps(data)

    def get_predicates(self):
        if self.is_verified():
            data = {}
            for (name, val) in self.json_data['presentation']['requested_proof']['predicates'].items():
                data[name] = val['raw']
            return json.dumps(data)

    def get_identifiers(self):
        if self.__has_identifiers():
            data = {}
            identifiers = []
            for index in range(len(self.json_data['presentation']['identifiers'])):
                identifiers.extend([self.json_data['presentation']['identifiers'][index]])
            data['identifiers'] = identifiers
            return json.dumps(data)

    def get_schemas(self):
        if self.__has_identifiers():
            data = {}
            creds = []
            for index in range(len(self.json_data['presentation']['identifiers'])):
                for key in self.json_data['presentation']['identifiers'][index]:
                    if key == 'schema_id':
                        creds.extend([self.json_data['presentation']['identifiers'][index][key]])
            data['schema_id'] = creds
            return json.dumps(data)

    def get_cred_def_ids(self):
        if self.__has_identifiers():
            data = {}
            creds = []
            for index in range(len(self.json_data['presentation']['identifiers'])):
                for key in self.json_data['presentation']['identifiers'][index]:
                    if key == 'cred_def_id':
                        creds.extend([self.json_data['presentation']['identifiers'][index][key]])
            data['cred_def_id'] = creds
            return json.dumps(data)

    def get_rev_reg_ids(self):
        if self.__has_identifiers():
            data = {}
            creds = []
            for index in range(len(self.json_data['presentation']['identifiers'])):
                for key in self.json_data['presentation']['identifiers'][index]:
                    if key == 'rev_reg_id':
                        creds.extend([self.json_data['presentation']['identifiers'][index][key]])
            data['rev_reg_id'] = creds
            return json.dumps(data)

    def get_role(self):
        return(self.json_data['role'])

    def get_threadid(self):
        return(self.json_data['thread_id'])

    def get_presentation_request(self):
        return(self.json_data['presentation_request'])

    def get_verified_state(self):
        return self.json_data['state']

    def get_presxid(self):
        return self.json_data['presentation_exchange_id']

    def get_from_conn_id(self):
        return self.json_data['connection_id']

    def is_verified(self):
        try:
            assert self.json_data['verified'] == "true"
        except AssertionError:
            logger.debug('Verification Failed')
            return False
        return True

    def validate_presentation_json(self, presentation_json):
        try:
            # Taken from sample response in swagger UI
            # TODO Determine whether this is the minimal set of keys
            presentation_keys = [
                "auto_present",
                "connection_id",
                "created_at",
                "error_msg",
                "initiator",
                "presentation",
                "presentation_exchange_id",
                "presentation_proposal_dict",
                "presentation_request",
                "presentation_request_dict",
                "role",
                "state",
                "thread_id",
                "trace",
                "updated_at",
                "verified"
            ]
            for key in presentation_keys:
                assert key in json.loads(presentation_json),\
                    f"Invalid presentation. Missing key {key}"
        except AssertionError:
            raise

    def __has_identifiers(self):
        try:
            assert 'identifiers' in self.json_data['presentation'],\
                "No key 'identifiers' in presentation"
            return True
        except AssertionError:
            logger.warning("No key 'identifiers' in presentation")
            raise

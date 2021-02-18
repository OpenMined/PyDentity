import json
import logging

logger = logging.getLogger("aries_controller.models.presentation")

class Presentation():
    def __init__(self, presentation_json):
        # TODO Load verify var with json.loads() and test code
        self.json_data = presentation_json
        if self.is_verified() == "false":
            logger.error('Presentation Object Verification Failed')
            # TODO raise proper PresentationVerificationFailed exception
            raise Exception('Presentation Object Verification Failed')

    def get_self_attested(self):
      if self.is_verified() == "false":
          logger.debug('Verification Failed')
      data = {}
      for (name, val) in self.json_data['presentation']['requested_proof']['self_attested_attrs'].items():
        data[name] = val['raw']
      return json.dumps(data)

    def get_revealed(self):
      if self.is_verified() == "false":
          logger.debug('Verification Failed')
      data = {}
      for (name, val) in self.json_data['presentation']['requested_proof']['revealed_attrs'].items():
          data[name] = val['raw']

      return json.dumps(data)

    def get_unrevealed_attrs(self):
      if self.is_verified() == "false":
          logger.debug('Verification Failed')
      data = {}
      for (name, val) in self.json_data['presentation']['requested_proof']['unrevealed_attrs'].items():
        data[name] = val['raw']
      return json.dumps(data)

    def get_predicates(self):
      if self.is_verified() == "false":
          logger.debug('Verification Failed')
      data = {}
      for (name, val) in self.json_data['presentation']['requested_proof']['predicates'].items():
        data[name] = val['raw']
      return json.dumps(data)

    def get_identifiers(self):
        data = {}
        identifiers = []
        for index in range(len(self.json_data['presentation']['identifiers'])):
            identifiers.extend([self.json_data['presentation']['identifiers'][index]])
        data['identifiers'] = identifiers
        return json.dumps(data)

    def get_schemas(self):
        data = {}
        creds = []
        for index in range(len(self.json_data['presentation']['identifiers'])):
            for key in self.json_data['presentation']['identifiers'][index]:
                if key == 'schema_id':
                    creds.extend([self.json_data['presentation']['identifiers'][index][key]])
        data['schema_id'] = creds
        return json.dumps(data)

    def get_cred_def_ids(self):
        data = {}
        creds = []
        for index in range(len(self.json_data['presentation']['identifiers'])):
            for key in self.json_data['presentation']['identifiers'][index]:
                if key == 'cred_def_id':
                    creds.extend([self.json_data['presentation']['identifiers'][index][key]])
        data['cred_def_id'] = creds
        return json.dumps(data)

    def get_rev_reg_ids(self):
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

    def is_verified(self):
      return self.json_data['verified']

    def from_conn_id(self):
        return self.json_data['connection_id']
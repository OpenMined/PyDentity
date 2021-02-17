import json

class Presentation():
    def __init__(self, verify):
        self.verify = verify

    def get_self_attested(self):
      if self.is_verified() == "false":
        print('Verification Failed')
      data = {}
      for (name, val) in self.verify['presentation']['requested_proof']['self_attested_attrs'].items():
        data[name] = val['raw']
      return json.dumps(data)

    def get_revealed(self):
      if self.is_verified() == "false":
        print('Verification Failed')
      data = {}
      for (name, val) in self.verify['presentation']['requested_proof']['revealed_attrs'].items():
          data[name] = val['raw']

      return json.dumps(data)

    def get_unrevealed_attrs(self):
      if self.is_verified() == "false":
        print('Verification Failed')
      data = {}
      for (name, val) in self.verify['presentation']['requested_proof']['unrevealed_attrs'].items():
        data[name] = val['raw']
      return json.dumps(data)

    def get_predicates(self):
      if self.is_verified() == "false":
        print('Verification Failed')
      data = {}
      for (name, val) in self.verify['presentation']['requested_proof']['predicates'].items():
        data[name] = val['raw']
      return json.dumps(data)

    def get_identifiers(self):
        data = {}
        identifiers = []
        for index in range(len(self.verify['presentation']['identifiers'])):
            identifiers.extend([self.verify['presentation']['identifiers'][index]])
        data['identifiers'] = identifiers
        return json.dumps(data)

    def get_schemas(self):
        data = {}
        creds = []
        for index in range(len(self.verify['presentation']['identifiers'])):
            for key in self.verify['presentation']['identifiers'][index]:
                if key == 'schema_id':
                    creds.extend([self.verify['presentation']['identifiers'][index][key]])
        data['schema_id'] = creds
        return json.dumps(data)

    def get_cred_def_ids(self):
        data = {}
        creds = []
        for index in range(len(self.verify['presentation']['identifiers'])):
            for key in self.verify['presentation']['identifiers'][index]:
                if key == 'cred_def_id':
                    creds.extend([self.verify['presentation']['identifiers'][index][key]])
        data['cred_def_id'] = creds
        return json.dumps(data)

    def get_rev_reg_ids(self):
        data = {}
        creds = []
        for index in range(len(self.verify['presentation']['identifiers'])):
            for key in self.verify['presentation']['identifiers'][index]:
                if key == 'rev_reg_id':
                    creds.extend([self.verify['presentation']['identifiers'][index][key]])
        data['rev_reg_id'] = creds
        return json.dumps(data)

    def get_role(self):
      return(self.verify['role'])

    def get_threadid(self):
      return(self.verify['thread_id'])

    def get_presentation_request(self):
      return(self.verify['presentation_request'])

    def get_verified_state(self):
      return self.verify['state']

    def get_presxid(self):
      return self.verify['presentation_exchange_id']

    def is_verified(self):
      return self.verify['verified']

    def conn_id(self):
        return self.verify['connection_id']
import json

class Presentation_Parser():
    def __init__(self, verify):
        self.verify = verify

    def get_self_attested(self):
      data = {}
      for (name, val) in self.verify['presentation']['requested_proof']['self_attested_attrs'].items():
        data[name] = val['raw']
      return json.dumps(data)

    def get_revealed(self):
      data = {}
      for (name, val) in self.verify['presentation']['requested_proof']['revealed_attrs'].items():
          data[name] = val['raw']

      return json.dumps(data)

    def get_unrevealed_attrs(self):
      data = {}
      for (name, val) in self.verify['presentation']['requested_proof']['unrevealed_attrs'].items():
        data[name] = val['raw']
      return json.dumps(data)

    def get_predicates(self):
      data = {}
      for (name, val) in self.verify['presentation']['requested_proof']['predicates'].items():
        data[name] = val['raw']
      return json.dumps(data)

    def get_identifiers(self):
      return self.verify['presentation']['identifiers']

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
      return bool(self.verify['verified'])
import json
import logging

logger = logging.getLogger("aries_controller.models.proof_request")

proof_request_template = json.loads({
  "comment": "",
  "proof_request": {
    "name": "",
    "non_revoked": {
      "to": 1618218626
    },
    "nonce": "1234567890",
    "requested_attributes": {
      "additionalProp1": {
        "name": "",
        "names": [
          ""
        ],
        "non_revoked": {
          "to": 1618218626
        },
        "restrictions": [
          {
            "additionalProp1": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "additionalProp2": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "additionalProp3": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag"
          }
        ]
      },
      "additionalProp2": {
        "name": "",
        "names": [
          ""
        ],
        "non_revoked": {
          "to": 1618218626
        },
        "restrictions": [
          {
            "additionalProp1": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "additionalProp2": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "additionalProp3": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag"
          }
        ]
      },
      "additionalProp3": {
        "name": "",
        "names": [
          ""
        ],
        "non_revoked": {
          "to": 1618218626
        },
        "restrictions": [
          {
            "additionalProp1": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "additionalProp2": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "additionalProp3": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag"
          }
        ]
      }
    },
    "requested_predicates": {
      "additionalProp1": {
        "name": "index",
        "non_revoked": {
          "to": 1618218626
        },
        "p_type": ">=",
        "p_value": 0,
        "restrictions": [
          {
            "cred_def_id": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "issuer_did": "WgWxqztrNooG92RXvxSTWv",
            "schema_id": "WgWxqztrNooG92RXvxSTWv:2:schema_name:1.0",
            "schema_issuer_did": "WgWxqztrNooG92RXvxSTWv",
            "schema_name": "transcript",
            "schema_version": "1.0"
          }
        ]
      },
      "additionalProp2": {
        "name": "index",
        "non_revoked": {
          "to": 1618218626
        },
        "p_type": ">=",
        "p_value": 0,
        "restrictions": [
          {
            "cred_def_id": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "issuer_did": "WgWxqztrNooG92RXvxSTWv",
            "schema_id": "WgWxqztrNooG92RXvxSTWv:2:schema_name:1.0",
            "schema_issuer_did": "WgWxqztrNooG92RXvxSTWv",
            "schema_name": "transcript",
            "schema_version": "1.0"
          }
        ]
      },
      "additionalProp3": {
        "name": "",
        "non_revoked": {
          "to": 1618218626
        },
        "p_type": ">=",
        "p_value": 0,
        "restrictions": [
          {
            "cred_def_id": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "issuer_did": "WgWxqztrNooG92RXvxSTWv",
            "schema_id": "WgWxqztrNooG92RXvxSTWv:2:schema_name:1.0",
            "schema_issuer_did": "WgWxqztrNooG92RXvxSTWv",
            "schema_name": "transcript",
            "schema_version": "1.0"
          }
        ]
      }
    },
    "version": "1.0"
  },
  "trace": false
})


class ProofRequest():
    def __init__(self, x):
        self.proof_request = {}
        self.proof_from_json = {}

    def proof_from_json(self, prop_json):
        try:
            self.proof_from_json = json.loads(prop_json)
            assert __verify_proof_format()
        except AssertionError as e:
            logger.error(f"Could not verify proof presentation format: {e!r}")
            raise
        except Exception:
            logger.error("Failed to load proposed JSON proof presentation.")
            raise

    def __verify_proof_format(self):
        
        return True

    # defs to pass single fields or sub dicts like
    """
     "restrictions": [
          {
            "cred_def_id": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "issuer_did": "WgWxqztrNooG92RXvxSTWv",
            "schema_id": "WgWxqztrNooG92RXvxSTWv:2:schema_name:1.0",
            "schema_issuer_did": "WgWxqztrNooG92RXvxSTWv",
            "schema_name": "transcript",
            "schema_version": "1.0"
          }
        ]
    """
    # See also presentation.py to get an idea of what we're trying to achieve


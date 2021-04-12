import pytest
import json

pytest.proof_request = json.loads({
  "comment": "string",
  "proof_request": {
    "name": "Proof request",
    "non_revoked": {
      "to": 1617957934
    },
    "nonce": "1234567890",
    "requested_attributes": {
      "additionalProp1": {
        "name": "favouriteDrink",
        "names": [
          "age"
        ],
        "non_revoked": {
          "to": 1617957934
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
        "name": "favouriteDrink",
        "names": [
          "age"
        ],
        "non_revoked": {
          "to": 1617957934
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
        "name": "favouriteDrink",
        "names": [
          "age"
        ],
        "non_revoked": {
          "to": 1617957934
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
          "to": 1617957934
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
          "to": 1617957934
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
        "name": "index",
        "non_revoked": {
          "to": 1617957934
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

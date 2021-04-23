import json
import logging

logger = logging.getLogger("aries_controller.models.proof_request")


class ProofRequest:
    def __init__(self, proof_request_json):
        try:
            self.json_data = json.loads(proof_request_json)
        except Exception:
            logger.error("Failed to load proof request JSON")
            raise
        self.validate_proof_request_json(proof_request_json)

    def get_requested_attributes(self):
        return self.json_data["requested_attributes"]

    def get_requested_predicates(self):
        return self.json_data["requested_predicates"]

    def get_connection_id(self):
        return self.json_data["connection_id"]

    def get_version(self):
        return self.json_data["version"]

    def get_name(self):
        return self.json_data["name"]

    def validate_proof_request_json(self, presentation_json):
        try:
            # Taken from sample response in swagger UI
            # TODO Determine whether this is the minimal set of keys
            presentation_keys = [
                "connection_id",
                "version",
                "name",
                "requested_attributes",
                "requested_predicates",
            ]
            for key in presentation_keys:
                assert key in json.loads(
                    presentation_json
                ), f"Invalid proof request. Missing key {key}"
        except AssertionError:
            raise

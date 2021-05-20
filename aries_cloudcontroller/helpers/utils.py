# Used to extract a DID from a schema or credential definition id
def extract_did(id):
    split = id.split(":")
    if len(split) > 3:
        return split[0]
    else:
        raise Exception(f"ID {id} is not is the correct format")


def get_schema_details(schema_id):
    details = schema_id.split(":")
    if len(details) == 4:
        return {
            "schema_id": schema_id,
            "schema_name": details[2],
            "schema_version": details[3],
            "schema_issuer_did": details[0],
        }
    else:
        raise Exception(f"ID {id} is not is the correct")

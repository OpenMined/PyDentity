from functools import singledispatchmethod
import re

import deepmerge
from inflection import camelize
import yaml


class OpenAPICleaner:
    FIX_REF_RE = re.compile(r"#/definitions")

    @singledispatchmethod
    def no_null_descriptions(self, value):
        return value

    @no_null_descriptions.register
    def _(self, value: dict):
        for child in value.values():
            self.no_null_descriptions(child)

        if "description" in value and value["description"] is None:
            value["description"] = ""

    @no_null_descriptions.register
    def _(self, value: list):
        for item in value:
            self.no_null_descriptions(item)

    @singledispatchmethod
    def no_missing_external_doc_urls(self, value):
        return value

    @no_missing_external_doc_urls.register
    def _(self, value: dict):
        for child in value.values():
            self.no_missing_external_doc_urls(child)

        if "externalDocs" in value and "url" not in value["externalDocs"]:
            value["externalDocs"]["url"] = "https://example.com/replace/me"

    @no_missing_external_doc_urls.register
    def _(self, value: list):
        for item in value:
            self.no_missing_external_doc_urls(item)

    @singledispatchmethod
    def fix_refs(self, value):
        return value

    @fix_refs.register
    def _(self, value: dict):
        for child in value.values():
            self.fix_refs(child)

        if "$ref" in value:
            value["$ref"] = self.FIX_REF_RE.sub("#/components/schemas", value["$ref"])

    @fix_refs.register
    def _(self, value: list):
        for item in value:
            self.fix_refs(item)

    @singledispatchmethod
    def fix_content_types(self, value):
        return value

    @fix_content_types.register
    def _(self, value: dict):
        for child in value.values():
            self.fix_content_types(child)

        if "*/*" in value:
            value["application/json"] = value["*/*"]
            del value["*/*"]

    @fix_content_types.register
    def _(self, value: list):
        for item in value:
            self.fix_content_types(item)

    def clean(self, value):
        self.no_null_descriptions(value)
        self.no_missing_external_doc_urls(value)
        self.fix_refs(value)
        self.fix_content_types(value)


def merge_operation_ids():
    with open("/app/openapi.yml") as openapi_file, open(
        "/app/operation-id-map.yml"
    ) as ops_file:
        openapi = yaml.load(openapi_file, Loader=yaml.FullLoader)
        ops = yaml.load(ops_file, Loader=yaml.FullLoader)

    return deepmerge.always_merger.merge(openapi, ops)


if __name__ == "__main__":
    result = merge_operation_ids()
    cleaner = OpenAPICleaner()
    cleaner.clean(result)
    with open("/app/openapi.yml", "w") as openapi_file:
        yaml.dump(result, openapi_file, sort_keys=False)

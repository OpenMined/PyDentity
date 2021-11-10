# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401


class IndyRequestedCredsRequestedAttr(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    IndyRequestedCredsRequestedAttr - a model defined in OpenAPI
        cred_id: Wallet credential identifier (typically but not necessarily a UUID).
        revealed: Whether to reveal attribute in proof (default true) [Optional].
    """

    cred_id: str
    revealed: Optional[bool] = None

    def __init__(
        self,
        *,
        cred_id: str = None,
        revealed: Optional[bool] = None,
        **kwargs,
    ):
        super().__init__(
            cred_id=cred_id,
            revealed=revealed,
            **kwargs,
        )

    class Config:
        allow_population_by_field_name = True


IndyRequestedCredsRequestedAttr.update_forward_refs()
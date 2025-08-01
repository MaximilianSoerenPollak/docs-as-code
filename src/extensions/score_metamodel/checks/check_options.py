# *******************************************************************************
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************
import re

from score_metamodel import (
    CheckLogger,
    default_options,
    local_check,
    ScoreNeedType,
)
from sphinx.application import Sphinx
from sphinx_needs.data import NeedsInfoType

FieldCheck = tuple[dict[str, str], bool]
CheckingDictType = dict[str, list[FieldCheck]]


def get_need_type(needs_types: list[ScoreNeedType], directive: str) -> ScoreNeedType:
    for need_type in needs_types:
        assert isinstance(need_type, dict), need_type
        if need_type["directive"] == directive:
            return need_type
    raise ValueError(f"Need type {directive} not found in needs_types")


def validate_fields(
    need: NeedsInfoType,
    log: CheckLogger,
    fields: dict[str, str],
    required: bool,
    field_type: str,
    allowed_prefixes: list[str],
):
    """
    Validates that fields (options or links) in a need match their expected patterns.

    :param need: The need object containing the data.
    :param log: Logger for warnings.
    :param fields: A dictionary of field names and their regex patterns.
    :param required: Whether the fields are required (True) or optional (False).
    :param field_type: A string indicating the field type ('option' or 'link').
    """

    def remove_prefix(word: str, prefixes: list[str]) -> str:
        # Memory and allocation wise better to use a generator here.
        # Removes any prefix allowed by configuration, if prefix is there.
        return [word.removeprefix(prefix) for prefix in prefixes][0]

    for field, pattern in fields.items():
        raw_value: str | list[str] | None = need.get(field, None)
        if raw_value in [None, [], ""]:
            if required:
                log.warning_for_need(
                    need, f"is missing required {field_type}: `{field}`."
                )
            continue  # Skip empty optional fields

        values: list[str]

        if isinstance(raw_value, str):
            values = [raw_value]
        elif isinstance(raw_value, list) and all(isinstance(v, str) for v in raw_value):
            values = raw_value
        else:
            values = [str(raw_value)]

        # The filter ensures that the function is only called when needed.
        for value in values:
            if allowed_prefixes:
                value = remove_prefix(value, allowed_prefixes)
            try:
                if not re.match(pattern, value):
                    log.warning_for_option(
                        need, field, f"does not follow pattern `{pattern}`."
                    )
            except TypeError:
                log.warning_for_option(
                    need,
                    field,
                    f"pattern `{pattern}` is not a valid regex pattern.",
                )


# req-#id: gd_req__req__attr_type
# req-#id: gd_req__requirements_attr_security
# req-#id: gd_req__req__attr_safety
# req-#id: gd_req__req__attr_status
# req-#id: gd_req__req__attr_rationale
# req-#id: gd_req__req__attr_mandatory
@local_check
def check_options(
    app: Sphinx,
    need: NeedsInfoType,
    log: CheckLogger,
):
    """
    Checks that required and optional options and links are present
    and follow their defined patterns.
    """
    production_needs_types = app.config.needs_types

    try:
        need_options = get_need_type(production_needs_types, need["type"])
    except ValueError:
        log.warning_for_option(need, "type", "no type info defined for semantic check.")
        return

    if not need_options.get("mandatory_options", {}):
        log.warning_for_option(need, "type", "no type info defined for semantic check.")
        return

    # Validate Options and Links
    checking_dict: CheckingDictType = {
        "option": [
            (need_options.get("mandatory_options", {}), True),
            (need_options.get("opt_opt", {}), False),
        ],
        "link": [
            (dict(need_options.get("req_link", [])), True),
            #    (dict(need_options.get("opt_link", [])), False),
        ],
    }

    # If undefined this is an empty list
    allowed_prefixes = app.config.allowed_external_prefixes

    for field_type, check_fields in checking_dict.items():
        for field_values, is_required in check_fields:
            validate_fields(
                need,
                log,
                field_values,
                required=is_required,
                field_type=field_type,
                allowed_prefixes=allowed_prefixes,
            )


@local_check
def check_extra_options(
    app: Sphinx,
    need: NeedsInfoType,
    log: CheckLogger,
):
    """
    This function checks if the user specified attributes in the need
    which are not defined for this element in the metamodel or by default
    system attributes.
    """

    production_needs_types = app.config.needs_types
    default_options_list = default_options()
    try:
        need_options = get_need_type(production_needs_types, need["type"])
    except ValueError:
        msg = "no type info defined for semantic check."
        log.warning_for_option(need, "type", msg)
        return

    required_options: dict[str, str] = need_options.get("mandatory_options", {})
    optional_options: dict[str, str] = need_options.get("opt_opt", {})
    required_links: list[str] = [x[0] for x in need_options.get("req_link", ())]
    optional_links: list[str] = [x[0] for x in need_options.get("opt_link", ())]

    allowed_options = (
        list(required_options.keys())
        + list(optional_options.keys())
        + required_links
        + optional_links
        + default_options_list
    )

    extra_options = [
        option
        for option in list(need.keys())
        if option not in allowed_options
        and need[option] not in [None, {}, "", []]
        and not option.endswith("_back")
    ]

    if extra_options:
        extra_options_str = ", ".join(f"`{option}`" for option in extra_options)
        msg = f"has these extra options: {extra_options_str}."
        log.warning_for_need(need, msg)

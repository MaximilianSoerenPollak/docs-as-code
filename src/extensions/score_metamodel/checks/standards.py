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
# from sphinx.application import Sphinx

from sphinx_needs.data import NeedsInfoType

# from score_metamodel import (
#    CheckLogger,
#    graph_check,
# )


def get_standards_needs(needs: list[NeedsInfoType]) -> dict[str, NeedsInfoType]:
    """
    Return a dictionary of all standard requirements from the Sphinx app's needs.
    """

    return {need["id"]: need for need in needs if need["type"] == "std_req"}


def get_standards_workproducts(
    needs: list[NeedsInfoType],
) -> dict[str, NeedsInfoType]:
    """
    Return a dictionary of standard workproducts from the Sphinx app's needs.
    """

    return {need["id"]: need for need in needs if need["type"] == "std_wp"}


def get_workflows(needs: list[NeedsInfoType]) -> dict[str, NeedsInfoType]:
    """
    Return a dictionary of all workflows from the Sphinx app's needs.
    """

    return {need["id"]: need for need in needs if need.get("type") == "workflow"}


def get_workproducts(needs: list[NeedsInfoType]) -> dict[str, NeedsInfoType]:
    """
    Return a dictionary of all workproducts from the Sphinx app's needs.
    """

    return {need["id"]: need for need in needs if need.get("type") == "workproduct"}


def get_compliance_req_needs(needs: list[NeedsInfoType]) -> set[str]:
    """
    Return a set of all compliance_req values from the Sphinx app's needs,
    but only if the need type is one of the specified process-related types.
    """
    return {
        compliance_req
        for need in needs
        if need.get("type", "").startswith("gd_")
        for compliance_req in need.get("complies", [])
        if compliance_req
    }


def get_compliance_wp_needs(needs: list[NeedsInfoType]) -> set[str]:
    """
    Return a set of all compliance_wp values from the Sphinx app's needs,
    but only if the need type is "workproduct".
    """
    return {
        compliance_wp
        for need in needs
        if need.get("type", "") == "workproduct"
        for compliance_wp in need.get("complies", [])
        if compliance_wp
    }


#        ╭─────────────────────────────────────────────────────────────────────────────╮
#        │                             Disabled temporarly                             │
#        ╰─────────────────────────────────────────────────────────────────────────────╯
# @graph_check
# def check_all_standard_req_linked_item_via_the_compliance_req(
#     app: Sphinx, needs: list[NeedsInfoType], log: CheckLogger
# ):
#     """
#     Checks if all standard requirements are linked to an item via the compliance_req
#     tag.
#     Logs a warning for each unlinked standard requirement.
#     """
#     standards_needs = get_standards_needs(needs)
#     compliance_req_needs = get_compliance_req_needs(needs)
#
#     for need in standards_needs.values():
#         if need["id"] not in compliance_req_needs:
#             msg = (
#                   f"Standard requirement `{need['id']}` is not linked to at least "
#                   f"one item via the complies tag. \n"
#                   )
#             log.warning_for_option(need, "id", msg)
#
# @graph_check
# def check_all_standard_workproducts_linked_item_via_the_compliance_wp(
#     app: Sphinx,needs: list[NeedsInfoType], log: CheckLogger
# ):
#     """
#     Checks if all standard work products are linked to an item via the complies tag.
#     Logs a warning for each unlinked standard work product.
#     """
#     standards_workproducts = get_standards_workproducts(needs)
#     compliance_wp_needs = get_compliance_wp_needs(needs)
#
#     for need in standards_workproducts.values():
#         if need["id"] not in compliance_wp_needs:
#             msg = (
#                 f"Standard workproduct `{need['id']}` is not linked to at least one"
#                 f" item via the complies tag. \n"
#             )
#             log.warning_for_option(need, "id", msg)
#
#
# @graph_check
# def check_workproduct_uniqueness_over_workflows(
#     app: Sphinx,needs: list[NeedsInfoType], log: CheckLogger
# ):
#     """
#     Check if all workproducts are contained in exactly one workflow.
#     Logs workflow IDs when a workproduct is contained in multiple workflows.
#     """
#     all_workflows = get_workflows(needs)
#     all_workproducts = get_workproducts(needs)
#
#     # Map to track counts for each workproduct and their associated workflows
#     workproduct_analysis = {
#         wp["id"]: {"count": 0, "workproduct": wp, "workflows": []}
#         for wp in all_workproducts.values()
#     }
#
#     # Iterate over workflows and update the counts and workflows
#     for workflow in all_workflows.values():
#         for output in workflow.get("output",[]):
#             # Increment count and add workflow_id if workproduct is in analysis
#             if output in workproduct_analysis:
#                 workproduct_analysis[output]["count"] += 1
#                 workproduct_analysis[output]["workflows"].append(workflow_id)
#
#     # Check for mismatches and log error
#     for analysis in workproduct_analysis.values():
#         count = analysis["count"]
#         workproduct = analysis["workproduct"]
#         workflows = analysis["workflows"]
#
#         if count != 1:  # Mismatch found
#             if count == 0:
#                 msg = "is not contained in any workflow, which is incorrect. \n"
#                 log.warning_for_need(workproduct, msg)
#             else:
#                 workflows_str = ", ".join(
#                     f"`{workflow}`" for workflow in workflows
#                 )  # Join workflow IDs into a string
#                 msg = (
#                       f"is contained in {count} workflows: {workflows_str},"
#                       f"which is incorrect. \n"
#                        )
#                 log.warning_for_need(workproduct, msg)
#
#
#        ╭─────────────────────────────────────────────────────────────────────────────╮
#        │                            END OF TEMP DISABLING                            │
#        ╰─────────────────────────────────────────────────────────────────────────────╯


def my_pie_linked_standard_requirements(
    needs: list[NeedsInfoType], results: list[int], **kwargs: str | int | float
) -> None:
    """
    Function to render the chart of check for standard requirements linked
    to at least an item via compliance-gd.

    Passed arguments can be accessed via kwargs['arg<position>']
    See: https://sphinx-needs.readthedocs.io/en/latest/filter.html#arguments
    """
    cnt_connected = 0
    cnt_not_connected = 0

    standard = kwargs["arg1"]

    all_standards_needs = get_standards_needs(needs)
    standards_needs = {
        k: v
        for k, v in all_standards_needs.items()
        if k.startswith(f"std_req__{standard}__")
    }
    compliance_req_needs = get_compliance_req_needs(needs)

    for need in standards_needs.values():
        if need["id"] in compliance_req_needs:
            cnt_connected += 1
        else:
            cnt_not_connected += 1

    results.append(cnt_connected)
    results.append(cnt_not_connected)


def my_pie_linked_standard_requirements_by_tag(
    needs: list[NeedsInfoType], results: list[int], **kwargs: str | int | float
) -> None:
    """
    Filter function used for 'needpie' directives.
    `Needs` and `results` are automatically passed in by sphinx-needs.
    The tag is put into `kwargs`.

    Only one(1) tag is allowed to be passed into this function

    Example usage:
    .. needpie:: Linked Requirements ASPICE 4.0 MAN.5
       :labels: Linked, Not Linked
       :legend:
       :colors: LightSeaGreen, lightgray
       :filter-func: score_metamodel.checks.standards.my_pie_linked_standard_requirements_by_tag(aspice40_man5)

    The call:
    =>  score_metamodel.checks.standards.my_pie_linked_standard_requirements_by_tag(aspice40_man5)
    would then pass 'aspice40_man5' as the arg1 and you have access to it then that way.

    NOTE:: There can not be any `.`(dots) in the tag passed into this function


    Return:
        The direct return of this function is None. Sphinx-needs will get the mutated `results`
        list, and use this to display/generate the piechart.

    """
    count_linked = 0
    count_non_linked = 0

    tag = str(kwargs["arg1"])
    assert len(kwargs) == 1, (
        "Can only provide one tag to `my_pie_linked_standard_requirements_by_tag`"
    )

    compliance_req_needs = get_compliance_req_needs(needs)
    for need in needs:
        if tag in need["tags"]:
            if need["id"] in compliance_req_needs:
                count_linked += 1
            else:
                count_non_linked += 1
    results.append(count_linked)
    results.append(count_non_linked)


def my_pie_linked_standard_workproducts(
    needs: list[NeedsInfoType], results: list[int], **kwargs: str | int | float
) -> None:
    """
    Function to render the chart of check for standar workproducts linked
    to at least an item via compliance-wp.

    Passed arguments can be accessed via kwargs['arg<position>']
    See: https://sphinx-needs.readthedocs.io/en/latest/filter.html#arguments
    """
    cwp_connected = 0
    cwp_not_connected = 0

    standard = kwargs["arg1"]

    all_standard_workproducts = get_standards_workproducts(needs)
    standard_workproducts = {
        k: v
        for k, v in all_standard_workproducts.items()
        if k.startswith(f"std_wp__{standard}__")
    }

    compliance_wp_needs = get_compliance_wp_needs(needs)

    for need in standard_workproducts.values():
        if need["id"] in compliance_wp_needs:
            cwp_connected += 1
        else:
            cwp_not_connected += 1

    results.append(cwp_connected)
    results.append(cwp_not_connected)


def my_pie_workproducts_contained_in_exactly_one_workflow(
    needs: list[NeedsInfoType], results: list[int], **kwargs: str | int | float
) -> None:
    """
    Function to render the chart of check for workproducts that are contained
    in exactly one workflow, the not connected once and the once
    that are connected to multiple workflows.
    """
    all_workflows = get_workflows(needs)
    all_workproducts = get_workproducts(needs)

    # Map to track counts for each workproduct and their associated workflows
    workproduct_analysis = {wp["id"]: {"count": 0} for wp in all_workproducts.values()}

    # Iterate over workflows and update the counts and workflows
    for workflow in all_workflows.values():
        for output in workflow.get("output", []):
            # Increment count and add workflow_id if workproduct is in analysis
            if output in workproduct_analysis:
                workproduct_analysis[output]["count"] += 1

    nb_wp_connected_to_one_workflow = nb_wp_connected_to_more_than_one_workflow = (
        not_connected_wp
    ) = 0

    for analysis in workproduct_analysis.values():
        count = analysis["count"]

        if count == 0:
            not_connected_wp += 1
        elif count == 1:
            nb_wp_connected_to_one_workflow += 1
        else:
            nb_wp_connected_to_more_than_one_workflow += 1

    results.append(not_connected_wp)
    results.append(nb_wp_connected_to_one_workflow)
    results.append(nb_wp_connected_to_more_than_one_workflow)

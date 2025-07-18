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
load("@aspect_rules_py//py:defs.bzl", "py_binary", "py_library")
load("@pip_process//:requirements.bzl", "all_requirements")
load("@score_python_basics//:defs.bzl", "score_py_pytest")

#exports_files(["parse_source_files.py"])

py_library(
    name = "score_source_code_linker",
    srcs = glob(
        ["**/*.py"],
        exclude = ["tests/*.py"],
    ),
    imports = ["."],
    visibility = ["//visibility:public"],
)

score_py_pytest(
    name = "score_source_code_linker_test",
    size = "small",
    srcs = glob([
        "tests/*.py",
    ]),
    args = [
        "-s",
        "-vv",
    ],
    data = glob(["**/*.json"]),
    imports = ["."],
    deps = [
        ":score_source_code_linker",
        "@score_docs_as_code//src/extensions/score_metamodel",
    ] + all_requirements,
)

..
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

Getting Started
###############

.. doc_getstrt:: Verification Get Started
   :id: doc_getstrt__verification__process
   :status: valid
   :tags: verification

   This document guides you through the initial steps of the software verification process,
   from creating test cases to executing and analyzing results.
   It leverages the :need:`doc_concept__verification__process` and :need:`gd_guidl__verification_guide`.

Relevant Documents
******************

* **Concept Document:** :need:`doc_concept__verification__process` provides a high-level overview of the verification concept.
* **Verification Guideline:** :need:`gd_guidl__verification_guide` details test case development, execution, and reporting procedures.
* **Verification Plan:** :need:`wp__verification__plan` implementation outlines the overall verification strategy and objectives.

Tooling Support
***************

The following tools support the verification process:

* **Bazel:** For building the software and running tests.
* **Google Test:** For unit testing in C++.
* **Rust's built-in testing framework:** For unit testing in Rust.
* **Pytest:** For component to integration testing in Python.
* **ITF (Integration Test Framework):** As framework for integration testing based on pytest.
  [TODO: Add link to ITF documentation once available]

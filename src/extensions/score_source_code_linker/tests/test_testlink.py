import json
from pathlib import Path
from src.extensions.score_source_code_linker.testlink import (
    TestLink,
    TestLink_JSON_Encoder,
    TestLink_JSON_Decoder,
    TestCaseNeed,
    store_test_xml_parsed_json,
    load_test_xml_parsed_json,
)


def test_testlink_serialization_roundtrip():
    link = TestLink(
        name="my_test",
        file=Path("some/file.py"),
        line=123,
        need="REQ_001",
        verify_type="fully",
        result="passed",
        result_text="All good",
    )
    dumped = json.dumps(link, cls=TestLink_JSON_Encoder)
    loaded = json.loads(dumped, object_hook=TestLink_JSON_Decoder)

    assert isinstance(loaded, TestLink)
    assert loaded == link


def test_testlink_encoder_handles_path():
    data = {
        "file": Path("some/thing.py")
    }
    encoded = json.dumps(data, cls=TestLink_JSON_Encoder)
    assert '"file": "some/thing.py"' in encoded


def test_decoder_ignores_irrelevant_dicts():
    input_data = {"foo": "bar"}
    result = TestLink_JSON_Decoder(input_data)
    assert result == input_data


def test_clean_text_removes_ansi_and_html_unescapes():
    raw = "\x1b[31m&lt;b&gt;Warning&lt;/b&gt;\x1b[0m\nExtra line"
    cleaned = TestCaseNeed.clean_text(raw)
    assert cleaned == "<b>Warning</b> Extra line"


def test_testcaseneed_to_dict_multiple_links():
    case = TestCaseNeed(
        name="TC_01",
        file="src/test.py",
        lineNr="10",
        result="failed",
        TestType="unit",
        DerivationTechnique="manual",
        result_text="Something went wrong",
        PartiallyVerifies="REQ-1, REQ-2",
        FullyVerifies="REQ-3"
    )

    links = case.to_dict()

    assert len(links) == 3
    need_ids = [link.need for link in links]
    assert set(need_ids) == {"REQ-1", "REQ-2", "REQ-3"}

    for link in links:
        assert link.file == Path("src/test.py")
        assert link.line == 10
        assert link.name == "TC_01"
        assert link.result == "failed"


def test_store_and_load_testlinks_roundtrip(tmp_path):
    file = tmp_path / "testlinks.json"

    links = [
        TestLink(
            name="L1",
            file=Path("abc.py"),
            line=1,
            need="REQ_A",
            verify_type="partially",
            result="passed",
            result_text="Looks good"
        ),
        TestLink(
            name="L2",
            file=Path("def.py"),
            line=2,
            need="REQ_B",
            verify_type="fully",
            result="failed",
            result_text="Needs work"
        )
    ]

    store_test_xml_parsed_json(file, links)
    assert file.exists()

    reloaded = load_test_xml_parsed_json(file)

    assert reloaded == links
    for link in reloaded:
        assert isinstance(link, TestLink)

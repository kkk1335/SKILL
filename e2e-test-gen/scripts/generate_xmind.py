#!/usr/bin/env python3
"""
E2E Test Case Generator - XMind Output
Reads a JSON test case specification and generates an XMind (.xmind) mind map.

XMind 8 format: a ZIP containing content.xml with the mind map structure.

Usage:
    python3 generate_xmind.py <input_json> <output_xmind>

Input JSON format:
{
    "title": "项目名称 - E2E测试用例",
    "modules": [
        {
            "name": "模块名称",
            "test_cases": [
                {
                    "id": "TC-001",
                    "test_point": "测试点描述",
                    "precondition": "前置条件",
                    "steps": ["步骤1", "步骤2", "步骤3"],
                    "expected": "预期结果"
                }
            ]
        }
    ]
}
"""

import json
import sys
import os
import uuid
import zipfile
from xml.sax.saxutils import escape


def _uid():
    return str(uuid.uuid4())


def _esc(text):
    """Escape text for XML content."""
    return escape(str(text), entities={'\n': '&#10;', '\t': '&#9;'})


def build_topic_xml(parent_id, topic_id, title, children=None, structure_class=None):
    """Build XML string for a single topic element."""
    attrs = f'id="{topic_id}" timestamp="{_uid()}"'
    sc = ""
    if structure_class:
        sc = f'<structure-class>{_esc(structure_class)}</structure-class>'
    
    title_xml = f"<title>{_esc(title)}</title>"
    
    children_xml = ""
    if children:
        children_xml = "<children>" + "".join(children) + "</children>"
    
    return (
        f'<topic {attrs}>'
        f'{sc}'
        f'{title_xml}'
        f'{children_xml}'
        f'</topic>'
    )


def build_case_xml(case):
    """Build XML for a single test case with its details."""
    case_id = _uid()
    case_label = f"{case['id']}: {case['test_point']}"
    
    children = []
    
    # 前置条件
    if case.get("precondition"):
        pc_id = _uid()
        children.append(build_topic_xml(case_id, pc_id, f"前置条件: {case['precondition']}"))
    
    # 测试步骤
    steps_children = []
    for i, step in enumerate(case.get("steps", []), 1):
        step_id = _uid()
        steps_children.append(build_topic_xml(case_id, step_id, f"{i}. {step}"))
    
    if steps_children:
        steps_id = _uid()
        steps_xml = (
            f'<topic id="{steps_id}" timestamp="{_uid()}">'
            f'<title>{_esc("测试步骤")}</title>'
            f'<children>' + "".join(steps_children) + '</children>'
            f'</topic>'
        )
        children.append(steps_xml)
    
    # 预期结果
    if case.get("expected"):
        er_id = _uid()
        children.append(build_topic_xml(case_id, er_id, f"预期结果: {case['expected']}"))
    
    return build_topic_xml("parent", case_id, case_label, children=children)


def build_module_xml(module):
    """Build XML for a module and its test cases."""
    module_id = _uid()
    children = []
    for case in module.get("test_cases", []):
        children.append(build_case_xml(case))
    return build_topic_xml("root", module_id, module["name"], children=children)


def generate_xmind(spec, output_path):
    """Generate XMind (.xmind) file from test case specification."""
    title = spec.get("title", "E2E测试用例")
    root_id = _uid()
    sheet_id = _uid()
    
    # Build module topics
    module_xmls = []
    for module in spec.get("modules", []):
        module_xmls.append(build_module_xml(module))
    
    # Root topic with all modules as children
    root_topic_xml = (
        f'<topic id="{root_id}" timestamp="{_uid()}">'
        f'<title>{_esc(title)}</title>'
        f'<children type="attached">' + "".join(module_xmls) + '</children>'
        f'</topic>'
    )
    
    # Full content.xml
    content_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        '<xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0" '
        'xmlns:fo="http://www.w3.org/1999/XSL/Format" '
        'xmlns:svg="http://www.w3.org/2000/svg" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'timestamp="" version="2.0">'
        f'<sheet id="{sheet_id}" timestamp="{_uid()}">'
        f'<title>{_esc(title[:50])}</title>'
        f'{root_topic_xml}'
        '</sheet>'
        '</xmap-content>'
    )
    
    # Write XMind zip file
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.xml", content_xml)
        # XMind requires a manifest
        manifest = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
            '<manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0">'
            '<file-entry full-path="content.xml" media-type="text/xml"/>'
            '<file-entry full-path="META-INF/" media-type=""/>'
            '</manifest>'
        )
        zf.writestr("META-INF/manifest.xml", manifest)
    
    return output_path


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.json> <output.xmind>", file=sys.stderr)
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    with open(input_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    
    result = generate_xmind(spec, output_path)
    print(f"XMind file generated: {result}")


if __name__ == "__main__":
    main()

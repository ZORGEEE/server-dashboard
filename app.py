from pathlib import Path

import yaml
from flask import Flask, render_template

app = Flask(__name__)

CONFIG_PATH = Path(__file__).parent / "config" / "tools.yaml"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
MAX_COLS_SOLO = 8
MAX_ICONS_GROUPED_ROW = 7
COL_WIDTH = 96
GRID_GAP = 18
CARD_SIZE = 94
GROUP_PADDING_X = 32
ROW_WIDTH = MAX_COLS_SOLO * COL_WIDTH + (MAX_COLS_SOLO - 1) * GRID_GAP


def layout_context():
    return {
        "col_width": COL_WIDTH,
        "grid_gap": GRID_GAP,
        "card_size": CARD_SIZE,
        "row_width": ROW_WIDTH,
    }


def _enrich_tool(tool):
    icon = tool.get("icon", "")
    tool["icon_is_image"] = Path(icon).suffix.lower() in IMAGE_EXTENSIONS
    return tool


def _grid_layout(tool_count, max_cols):
    cols = min(tool_count, max_cols)
    width = cols * COL_WIDTH + (cols - 1) * GRID_GAP
    return {
        "grid_cols": cols,
        "grid_width": width,
        "max_cols": max_cols,
    }


def _apply_solo_layout(sections):
    for section in sections:
        section.update(_grid_layout(len(section["tools"]), MAX_COLS_SOLO))
    return sections


def _apply_grouped_layout(sections):
    counts = [len(section["tools"]) for section in sections]

    block_widths = []
    for section, count in zip(sections, counts):
        layout = _grid_layout(count, count)
        layout["block_width"] = layout["grid_width"] + GROUP_PADDING_X
        section.update(layout)
        block_widths.append(layout["block_width"])

    total_block_width = sum(block_widths)
    gap_count = len(sections) - 1
    if gap_count > 0 and total_block_width <= ROW_WIDTH:
        group_gap = (ROW_WIDTH - total_block_width) / gap_count
    else:
        group_gap = GRID_GAP

    grid_template = " ".join(f"{width}px" for width in block_widths)
    return sections, group_gap


def _enrich_section(section):
    section["tools"] = [_enrich_tool(tool) for tool in section["tools"]]
    return section


def load_sections():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        sections = yaml.safe_load(f)["sections"]

    return [_enrich_section(section) for section in sections]


def flatten_tools(sections):
    return [tool for section in sections for tool in section["tools"]]


def group_sections(sections):
    groups = []
    index = 0

    while index < len(sections):
        section = sections[index]
        row_key = section.get("row")

        if not row_key:
            groups.append(
                {
                    "layout": "solo",
                    "row_width": ROW_WIDTH,
                    "sections": _apply_solo_layout([section]),
                }
            )
            index += 1
            continue

        row_sections = [section]
        next_index = index + 1
        while next_index < len(sections) and sections[next_index].get("row") == row_key:
            row_sections.append(sections[next_index])
            next_index += 1

        if len(row_sections) == 1:
            groups.append(
                {
                    "layout": "solo",
                    "row_width": ROW_WIDTH,
                    "sections": _apply_solo_layout(row_sections),
                }
            )
        else:
            grouped_sections, group_gap = _apply_grouped_layout(row_sections)
            groups.append(
                {
                    "layout": "grouped",
                    "row_width": ROW_WIDTH,
                    "group_gap": group_gap,
                    "sections": grouped_sections,
                }
            )

        index = next_index

    return groups


@app.route("/")
def index():
    sections = load_sections()
    return render_template(
        "index.html",
        section_groups=group_sections(sections),
        tools=flatten_tools(sections),
        **layout_context(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8095, debug=True)

#!/usr/bin/env python3
"""README visuals for dsh-eia-guide-check — drawn from what the package ships.

Outputs (docs/assets/, idempotent overwrite):

  dsh-eia-guide-check-hero-{zh,en}-{light,dark}.webp   1440x576
  dsh-eia-guide-check-flow-v5-{light,dark}.svg         1100x660

Every label below is read off this package, not off a generic checker template:

  * `rules/eia-guide-check.yaml` — pack `2026.1`, exactly seven rules. Their
    `basis.kind` values are six `derived-from-principle` and one
    `institutional-configuration` (EG-003); no rule claims `direct`, which is
    why the hero's top tier is drawn as an empty slot rather than a count.
  * `src/shared/ruleset.ts` — `MAX_SEVERITY_BY_KIND`: direct -> error,
    derived-from-principle -> warn, institutional-configuration -> info. The
    hero's tier ceilings are those three constants, and the loader *throws* at
    load time when a rule exceeds its ceiling; the cap is enforced, not advised.
  * `src/model.ts` — the reader's contract: 12 canonical row columns and 5
    optional header fields, matched through Chinese/English aliases. Only eight
    of those fields are read by this pack's rules: guideName + guideCode
    (EG-001), guideCode (EG-002), guideStatus (EG-003), method + standard
    (EG-004), element (EG-005), project + reportType (EG-006), standard
    (EG-007). The flow draws those eight columns and says the other four are
    kept untouched.
  * `src/shared/rows.ts` — the check kinds drawn on the rule nodes
    (presenceAny, pattern, enum, unique, headerPresence, containsAny) and the
    two exits: a finding enters `issues[]`, a rule that cannot run enters
    `skipped[]` with its own reason, and a rule that ran clean enters neither.
    EG-003 ships `values: []`, so it always enters `skipped[]` until configured.
  * `samples/quickstart/input/EG-001-unsafe.json` + `expected/result.json` —
    the numbers quoted in both figures: issueCount 1, summary warn 1, skipped 1;
    the finding is row 1 with guideName and guideCode both blank.

Hero: the left column is the copy block (kicker / wordmark / two value lines /
one two-line subtitle / meta / footer). The right side is this plugin's own
evidence model: three basis-kind tiers, the severity ceiling each one permits,
the six rules that sit on the derived tier, and EG-003 alone on the
institutional tier with its shipped `values: []` and its `skipped` outcome.

Flow: grammar = FIELD→RULE WIRING BOARD with two exits, not a row of nodes and
not a single pipeline. Eight material columns sit on the left, the seven rules
on the right, and each line means "this rule reads that column" (guideCode and
standard each feed two rules). The rule column carries the severity ceiling on
every node; the output sits under it as `issues[]` / `skipped[]`, and the
bottom-left note states the reading rule (an empty issue list is not a pass and
the verdict stays with the reviewer). No node is a step in a chain.

Text sizes: hero title 54px, value lines 38px, subtitle >=15px, meta/footer
>=12px. Flow node text 13-13.5px (figure title 27px), annotations >=11px.
Every label is measured before drawing: a label that would overflow its box
aborts the run instead of shipping clipped text.

Old single-skin assets (--flow-{light,dark}.svg, --hero.png, --demo.*,
quickstart.*) stay on disk so existing deep links resolve; the READMEs
reference only the new hero and flow-v5 pair.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow + Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf /
           consolab.ttf (missing font = hard error, never tofu).
"""
from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")
NAME = "dsh-eia-guide-check"

FONT_FILES = {
    "cjk": r"C:\Windows\Fonts\msyh.ttc",
    "cjk_bold": r"C:\Windows\Fonts\msyhbd.ttc",
    "mono": r"C:\Windows\Fonts\consola.ttf",
    "mono_bold": r"C:\Windows\Fonts\consolab.ttf",
}
for _kind, _path in FONT_FILES.items():
    if not os.path.exists(_path):
        raise SystemExit(f"FATAL: font missing: {_path}")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------
# palette — family accent #4B67B4 (dark #8496f5) on the light/dark grounds
# ---------------------------------------------------------------------------
HERO = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", card_edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", ok="#15803d", warn="#b45309", info="#4B67B4",
        error="#b3261e",
        band="#f5f2fb", chip="#ffffff", chip_edge="#e6e2ef",
        pill="#ece7f9", hair="#e7e4f0",
        shadow=(43, 35, 80), shadow_alpha=54, glow_alpha=26,
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", card_edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", ok="#3fb950", warn="#d9a441", info="#8496f5",
        error="#f0776a",
        band="#202839", chip="#1f2739", chip_edge="#313b52",
        pill="#242d42", hair="#2b3348",
        shadow=(0, 0, 0), shadow_alpha=165, glow_alpha=42,
    ),
}

FLOW = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        panel="#ffffff", edge="#e6e2ef", node="#ffffff", node_edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", warn="#b45309", info="#4B67B4", error="#b3261e",
        band="#f5f2fb", pill="#ece7f9", hair="#e7e4f0",
        wire="#4B67B4", wire_op="0.38", warn_bg="#fbf1e4", info_bg="#ece7f9",
        shadow="#2b2440", shadow_op="0.10",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        panel="#1b2231", edge="#2e374b", node="#1b2231", node_edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", warn="#d9a441", info="#8496f5", error="#f0776a",
        band="#202839", pill="#242d42", hair="#2b3348",
        wire="#8496f5", wire_op="0.46", warn_bg="#2a2419", info_bg="#242d42",
        shadow="#000000", shadow_op="0.5",
    ),
}

# ---------------------------------------------------------------------------
# fonts + measuring
# ---------------------------------------------------------------------------
_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}
_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def font(size: float, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    key = (kind, int(round(size)))
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_FILES[kind], key[1])
    return _font_cache[key]


def measure(text: str, size: float, kind: str = "cjk") -> float:
    return _MEASURE.textlength(text, font=font(size, kind))


def tracked_width(text: str, size: float, kind: str, tracking: float) -> float:
    fnt = font(size, kind)
    return sum(fnt.getlength(ch) for ch in text) + tracking * max(0, len(text) - 1)


def fit(text: str, kind: str, max_w: float, start: float, minimum: float) -> float:
    size = float(start)
    while size >= minimum:
        if measure(text, size, kind) <= max_w:
            return size
        size -= 0.5
    raise SystemExit(f"FATAL: {text[:40]!r} needs {measure(text, minimum, kind):.1f}px "
                     f"> {max_w:.0f}px even at {minimum:.1f}px")


def fit_all(lines: list[str], kind: str, max_w: float, start: float,
            minimum: float) -> float:
    return min(fit(line, kind, max_w, start, minimum) for line in lines)


def hx(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def mix(fg: str, bg: str, alpha: float) -> tuple[int, int, int]:
    a, b = hx(fg), hx(bg)
    return tuple(int(p + (q - p) * alpha) for p, q in zip(b, a))


# ---------------------------------------------------------------------------
# raster primitives
# ---------------------------------------------------------------------------
def gradient(w: int, h: int, top: str, bottom: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    a, b = hx(top), hx(bottom)
    for y in range(h):
        t = 0.14 * (y / h) + 0.86 * (y / h) ** 1.25
        draw.line([(0, y), (w, y)],
                  fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base.convert("RGBA")


def glow(img: Image.Image, cx: int, cy: int, r: int, color: str,
         alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    rgb = hx(color)
    for i in range(10, 0, -1):
        rr = r * i / 10
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                     fill=rgb + (int(alpha * (1 - i / 11)),))
    return Image.alpha_composite(
        img, layer.filter(ImageFilter.GaussianBlur(28)))


def drop_shadow(img: Image.Image, box: tuple[int, int, int, int], radius: int,
                color: tuple[int, int, int], alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([box[0], box[1] + 10, box[2], box[3] + 12],
                        radius=radius, fill=color + (alpha,))
    return Image.alpha_composite(img, layer.filter(ImageFilter.GaussianBlur(20)))


def tracked_text(draw: ImageDraw.ImageDraw, xy, text: str, size: float,
                 kind: str, fill, tracking: float) -> None:
    x, y = xy
    fnt = font(size, kind)
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="ls")
        x += fnt.getlength(ch) + tracking


def text_width_tracked(text: str, size: float, kind: str, tracking: float) -> float:
    return tracked_width(text, size, kind, tracking)


# ---------------------------------------------------------------------------
# copy — every string here is grounded in this repository
# ---------------------------------------------------------------------------
COPY = {
    "zh": dict(
        kicker="DEEPSEEK HARNESS 插件 · 环评导则适用性核对 · 只读",
        value=["把导则适用性核对表", "读成一张可追溯的差异清单"],
        sub=["七条随包规则只列材料内能指认的差异：要素是否指明适用导则、",
             "编号是否写成通用形式、方法与标准是否填写；不判合规，结论留给审核人。"],
        meta="eia_guide_check · EG-001..EG-007 · rules/eia-guide-check.yaml",
        foot="Apache-2.0 · 只读材料 · 不联网 · 不调用模型",
        panel_title="规则包 · 证据分级",
        panel_title_right="rules/eia-guide-check.yaml · 2026.1",
        panel_sub="依据类别决定严重级上限：上限跟着证据走",
        tiers=[
            ("direct", "直接条文", "上限 ≤ error",
             "0 条 —— 本包没有逐字条文，excerpt 如实写明"),
            ("derived-from-principle", "由原则推导", "上限 ≤ warn", None),
            ("institutional-configuration", "本机构口径", "上限 ≤ info", None),
        ],
        chips=[["EG-001", "指明适用导则"], ["EG-002", "编号通用形式"],
               ["EG-004", "方法或标准"], ["EG-005", "要素不重复"],
               ["EG-006", "表头声明"], ["EG-007", "无模板占位符"]],
        tier3_chip=["EG-003", "状态取值"],
        tier3_note="skipped · values = []",
        panel_foot_l="示例：issues[] 1 条（warn）· skipped[] 1 条",
        panel_foot_r="空清单 ≠ 通过",
    ),
    "en": dict(
        kicker="DEEPSEEK HARNESS PLUGIN · EIA GUIDELINE CHECK · READ-ONLY",
        value=["Turn the applicability sheet", "into a traceable difference list"],
        sub=["Seven bundled rules point only at differences inside the sheet: a missing",
             "guideline, a malformed number, an empty method. The reviewer decides."],
        meta="eia_guide_check · EG-001..EG-007 · rules/eia-guide-check.yaml",
        foot="Apache-2.0 · read-only material · no network · no model calls",
        panel_title="RULE PACK · EVIDENCE TIERS",
        panel_title_right="rules/eia-guide-check.yaml · 2026.1",
        panel_sub="The basis kind sets the severity ceiling — the cap follows the evidence",
        tiers=[
            ("direct", "verbatim clause", "ceiling ≤ error",
             "0 rules — no verbatim clause in the pack; every excerpt says so"),
            ("derived-from-principle", "from a principle", "ceiling ≤ warn", None),
            ("institutional-configuration", "local rule", "ceiling ≤ info", None),
        ],
        chips=[["EG-001", "names guide"], ["EG-002", "code form"],
               ["EG-004", "method / std"], ["EG-005", "unique element"],
               ["EG-006", "header stated"], ["EG-007", "placeholder"]],
        tier3_chip=["EG-003", "status values"],
        tier3_note="skipped · values = []",
        panel_foot_l="Sample: issues[] 1 (warn) · skipped[] 1",
        panel_foot_r="an empty list is not a pass",
    ),
}


# ---------------------------------------------------------------------------
# hero
# ---------------------------------------------------------------------------
W, H = 1440, 576
LEFT_X = 64
LEFT_MAX = 636           # 64 .. 700, panel starts at 748
PANEL = (748, 56, 1376, 520)
PAD = 26


def draw_hero(lang: str, skin: str) -> Image.Image:
    s = HERO[skin]
    c = COPY[lang]
    img = gradient(W, H, s["bg_from"], s["bg_to"])
    img = glow(img, 1160, 90, 380, s["accent"], s["glow_alpha"])
    img = glow(img, 220, 560, 300, s["accent"], int(s["glow_alpha"] * 0.6))

    draw = ImageDraw.Draw(img)

    # --- kicker pill ---------------------------------------------------------
    kick = c["kicker"]
    kick_size, kick_track = 12.5, 1.4
    kick_w = text_width_tracked(kick, kick_size, "cjk_bold", kick_track)
    pk = [LEFT_X, 62, LEFT_X + kick_w + 32, 94]
    draw.rounded_rectangle(pk, radius=16, fill=s["pill"])
    tracked_text(draw, (LEFT_X + 16, 84), kick, kick_size, "cjk_bold",
                 s["accent"], kick_track)

    # --- wordmark ------------------------------------------------------------
    title = NAME
    title_size = 54.0
    if measure(title, title_size, "mono_bold") > LEFT_MAX:
        title_size = fit(title, "mono_bold", LEFT_MAX, 54, 48)
    draw.text((LEFT_X, 152), title, font=font(title_size, "mono_bold"),
              fill=s["text"], anchor="ls")

    # --- two value lines -----------------------------------------------------
    v_size = fit_all(c["value"], "cjk_bold", LEFT_MAX, 38, 34)
    for i, line in enumerate(c["value"]):
        draw.text((LEFT_X, 232 + i * 54), line, font=font(v_size, "cjk_bold"),
                  fill=s["text"], anchor="ls")

    # --- subtitle ------------------------------------------------------------
    sub_size = fit_all(c["sub"], "cjk", LEFT_MAX, 16.5, 15)
    for i, line in enumerate(c["sub"]):
        draw.text((LEFT_X, 340 + i * 26), line, font=font(sub_size, "cjk"),
                  fill=s["sub"], anchor="ls")

    # --- meta + footer -------------------------------------------------------
    meta_size = fit(c["meta"], "mono", LEFT_MAX, 13.5, 12)
    draw.text((LEFT_X, 416), c["meta"], font=font(meta_size, "mono"),
              fill=s["faint"], anchor="ls")
    draw.text((LEFT_X, 496), c["foot"], font=font(13, "cjk"),
              fill=s["faint"], anchor="ls")

    # --- panel ---------------------------------------------------------------
    img = drop_shadow(img, PANEL, 22, s["shadow"], s["shadow_alpha"])
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = PANEL
    draw.rounded_rectangle(PANEL, radius=22, fill=s["card"],
                           outline=s["card_edge"], width=1)
    px0, px1 = x0 + PAD, x1 - PAD

    # panel heading
    draw.text((px0, 98), c["panel_title"],
              font=font(18, "cjk_bold"), fill=s["text"], anchor="ls")
    right_size = fit(c["panel_title_right"], "mono", 300, 12, 12)
    draw.text((px1, 96), c["panel_title_right"],
              font=font(right_size, "mono"), fill=s["faint"], anchor="rs")
    draw.text((px0, 122), c["panel_sub"], font=font(12.5, "cjk"),
              fill=s["sub"], anchor="ls")

    tier_boxes = [(136, 210), (222, 390), (402, 482)]
    caps = [s["error"], s["warn"], s["info"]]
    pills = [("error", s["error"]), ("warn", s["warn"]), ("info", s["info"])]

    for index, ((kind, gloss, cap, note), (ty0, ty1)) in enumerate(
            zip(c["tiers"], tier_boxes)):
        draw.rounded_rectangle([px0, ty0, px1, ty1], radius=16,
                               fill=s["band"], outline=s["card_edge"], width=1)
        cap_color = caps[index]

        # kind label (mono) + translated gloss (sans)
        kind_size = fit(kind, "mono_bold", px1 - px0 - 180, 14, 11.5)
        kw = measure(kind, kind_size, "mono_bold")
        draw.text((px0 + 16, ty0 + 28), kind,
                  font=font(kind_size, "mono_bold"), fill=s["text"],
                  anchor="ls")
        gloss_size = 12
        if measure(gloss, gloss_size, "cjk") > px1 - px0 - kw - 200:
            gloss_size = fit(gloss, "cjk", px1 - px0 - kw - 200, 12, 11)
        draw.text((px0 + 16 + kw + 10, ty0 + 28), gloss,
                  font=font(gloss_size, "cjk"), fill=s["sub"], anchor="ls")

        # severity-ceiling pill, right aligned
        cap_size = 12
        cap_w = measure(cap, cap_size, "cjk") + 22
        pill = [px1 - 16 - cap_w, ty0 + 12, px1 - 16, ty0 + 36]
        draw.rounded_rectangle(pill, radius=12,
                               fill=mix(cap_color, s["band"], 0.14))
        draw.text(((pill[0] + pill[2]) / 2, (pill[1] + pill[3]) / 2), cap,
                  font=font(cap_size, "cjk"), fill=cap_color, anchor="mm")

        if index == 0:
            slot = [px0 + 16, ty0 + 42, px1 - 16, ty0 + 66]
            draw.rounded_rectangle(slot, radius=12, outline=cap_color,
                                   width=1)
            # dashed effect: short segments along the top and bottom edges
            for sx in range(slot[0] + 12, slot[2] - 12, 12):
                draw.line([(sx, slot[1]), (sx + 6, slot[1])],
                          fill=s["band"], width=2)
                draw.line([(sx, slot[3]), (sx + 6, slot[3])],
                          fill=s["band"], width=2)
            note_size = fit(note, "cjk", slot[2] - slot[0] - 24, 12, 11)
            draw.text((slot[0] + 12, slot[1] + 17), note,
                      font=font(note_size, "cjk"), fill=s["sub"], anchor="ls")

        if index == 1:
            for i, (rid, token) in enumerate(c["chips"]):
                col, row = i % 3, i // 3
                cx = px0 + 16 + col * 184
                cy = ty0 + 46 + row * 54
                chip = [cx, cy, cx + 172, cy + 46]
                draw.rounded_rectangle(chip, radius=12, fill=s["chip"],
                                       outline=s["chip_edge"], width=1)
                draw.text((cx + 12, cy + 19), rid,
                          font=font(13, "mono_bold"), fill=s["text"],
                          anchor="ls")
                token_size = fit(token, "cjk", 148, 12, 11)
                draw.text((cx + 12, cy + 35), token,
                          font=font(token_size, "cjk"), fill=s["sub"],
                          anchor="ls")

        if index == 2:
            rid, token = c["tier3_chip"]
            chip = [px0 + 16, ty0 + 42, px0 + 16 + 226, ty0 + 74]
            draw.rounded_rectangle(chip, radius=12, fill=s["chip"],
                                   outline=s["chip_edge"], width=1)
            draw.text((chip[0] + 12, ty0 + 64), rid,
                      font=font(13, "mono_bold"), fill=s["text"], anchor="ls")
            draw.text((chip[0] + 12 + measure(rid, 13, "mono_bold") + 14,
                       ty0 + 64), token, font=font(11.5, "cjk"),
                      fill=s["sub"], anchor="ls")
            draw.text((chip[2] + 16, ty0 + 64), c["tier3_note"],
                      font=font(12, "cjk"), fill=s["faint"], anchor="ls")

    # panel footer
    draw.line([(px0, 494), (px1, 494)], fill=s["hair"], width=1)
    foot_l_size = fit(c["panel_foot_l"], "cjk", 360, 12, 11.5)
    draw.text((px0, 512), c["panel_foot_l"],
              font=font(foot_l_size, "cjk"), fill=s["faint"], anchor="ls")
    foot_r_size = fit(c["panel_foot_r"], "cjk", 220, 12, 11.5)
    draw.text((px1, 512), c["panel_foot_r"],
              font=font(foot_r_size, "cjk"), fill=s["accent"], anchor="rs")

    return img.convert("RGB")


# ---------------------------------------------------------------------------
# flow — field→rule wiring board, 1100x660, hand-written SVG
# ---------------------------------------------------------------------------
FW, FH = 1100, 660
FX, FY, FWID, FHE, FGAP = 40, 118, 260, 40, 5
RX, RY, RWID, RHE, RGAP = 510, 118, 320, 48, 6
CX1, CX2, CY, CW, CH = 510, 795, 520, 265, 100

FIELDS = [
    ("guideName", "导则名称", "行"),
    ("guideCode", "导则编号代码", "行"),
    ("guideStatus", "导则状态", "行"),
    ("method", "评价方法", "行"),
    ("standard", "执行标准", "行"),
    ("element", "评价要素", "行"),
    ("project", "项目名称", "表头"),
    ("reportType", "环评文件类型", "表头"),
]
RULES = [
    ("EG-001", "warn", "presenceAny · guideName | guideCode"),
    ("EG-002", "warn", "pattern · guideCode 的通用形式"),
    ("EG-003", "info", "enum · guideStatus · values = []"),
    ("EG-004", "warn", "presenceAny · method | standard"),
    ("EG-007", "warn", "containsAny · standard · terms"),
    ("EG-005", "warn", "unique · element"),
    ("EG-006", "warn", "headerPresence · project | reportType"),
]
# field index -> rule indices (guideCode and standard each feed two rules)
WIRES = {0: [0], 1: [0, 1], 2: [2], 3: [3], 4: [3, 4], 5: [5], 6: [6], 7: [6]}


def sans_css() -> str:
    return ("'Microsoft YaHei','Segoe UI','PingFang SC',"
            "'Noto Sans CJK SC',sans-serif")


def mono_css() -> str:
    return "Consolas,'Microsoft YaHei',ui-monospace,monospace"


def tw(text: str, size: float, mono: bool = False) -> float:
    """Conservative text-width estimate for pre-flight overflow checks."""
    total = 0.0
    for ch in text:
        if ord(ch) > 0x2E80:
            total += size
        else:
            total += size * (0.6 if mono else 0.53)
    return total


def checked(label: str, size: float, max_w: float, where: str,
            mono: bool = False) -> str:
    got = tw(label, size, mono)
    if got > max_w + 0.5:
        raise SystemExit(f"FATAL: flow label overflows {where}: {label!r} "
                         f"needs {got:.1f}px > {max_w:.0f}px")
    return label


def svg_text(x: float, y: float, s: str, size: float, fill: str,
             mono: bool = False, weight: str | None = None,
             anchor: str | None = None, spacing: float | None = None,
             opacity: float | None = None) -> str:
    attrs = [f'x="{x:g}"', f'y="{y:g}"', f'fill="{fill}"',
             f'font-family="{mono_css() if mono else sans_css()}"',
             f'font-size="{size:g}"']
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if spacing is not None:
        attrs.append(f'letter-spacing="{spacing:g}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity:g}"')
    return (f'<text {" ".join(attrs)}>{escape(s)}</text>')


def svg_pill(x: float, y: float, w: float, h: float, fill: str,
             stroke: str | None = None) -> str:
    edge = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" '
            f'rx="{h / 2:g}" fill="{fill}"{edge}/>')


def flow_svg(skin: str) -> str:
    s = FLOW[skin]
    parts: list[str] = []
    add = parts.append

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{FW}" height="{FH}" '
        f'viewBox="0 0 {FW} {FH}" role="img" '
        f'aria-label="{NAME}: field-to-rule wiring board with two exits">')
    add(f'<title>{NAME} — field → rule wiring board</title>')
    add('<defs>'
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
        f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>'
        f'<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{s["accent"]}" stop-opacity="0.16"/>'
        f'<stop offset="1" stop-color="{s["accent"]}" stop-opacity="0"/>'
        '</radialGradient>'
        f'<filter id="soft" x="-24%" y="-24%" width="148%" height="148%">'
        f'<feDropShadow dx="0" dy="6" stdDeviation="9" '
        f'flood-color="{s["shadow"]}" flood-opacity="{s["shadow_op"]}"/>'
        '</filter>'
        '</defs>')
    add(f'<rect width="{FW}" height="{FH}" rx="22" fill="url(#bg)"/>')
    add('<circle cx="930" cy="80" r="280" fill="url(#glow)"/>')

    # ---- header -------------------------------------------------------------
    add(svg_text(40, 52, NAME, 27, s["text"], mono=True, weight="700"))
    add(svg_text(40, 78, "一份核对表 → 8 个规范栏目 → 7 条规则；"
                 "每条规则只读它声明的栏，出口只有两个",
                 13, s["sub"]))
    tag = "rules/eia-guide-check.yaml · pack 2026.1"
    tag_w = tw(tag, 11.5, mono=True) + 26
    add(svg_pill(FW - 40 - tag_w, 34, tag_w, 28, s["pill"]))
    add(svg_text(FW - 40 - tag_w / 2, 52.5, tag, 11.5, s["accent"],
                 mono=True, anchor="middle"))
    add(f'<line x1="40" y1="92" x2="{FW - 40}" y2="92" '
        f'stroke="{s["hair"]}" stroke-width="1"/>')

    # ---- zone labels --------------------------------------------------------
    add(svg_text(40, 112, "IN · 核对表 · JSON / YAML · 8 栏", 12, s["accent"],
                 weight="700", spacing=0.4))
    add(svg_text(300, 112, "两列按所读栏目排列", 11.5, s["faint"]))
    add(svg_text(RX, 112, "RULES · 7 条 · derived 6 / institutional 1",
                 12, s["accent"], weight="700", spacing=0.4))

    # ---- field column -------------------------------------------------------
    field_mid: list[float] = []
    for i, (name, alias, tag_) in enumerate(FIELDS):
        y = FY + i * (FHE + FGAP)
        field_mid.append(y + FHE / 2)
        add(f'<g><rect x="{FX}" y="{y}" width="{FWID}" height="{FHE}" rx="14" '
            f'fill="{s["panel"]}" stroke="{s["node_edge"]}" stroke-width="1"/>')
        add(svg_text(FX + 14, y + 18, name, 13.5, s["text"],
                     mono=True, weight="700"))
        tag_fill = s["accent"] if tag_ == "表头" else s["faint"]
        add(svg_text(FX + FWID - 14, y + 18, tag_, 11, tag_fill,
                     anchor="end"))
        add(svg_text(FX + 14, y + 33, alias, 11.5, s["sub"]))
        add('</g>')
        checked(name, 13.5, FWID - 90, "field name", mono=True)
        checked(alias, 11.5, FWID - 90, "field alias")

    # ---- rule column --------------------------------------------------------
    rule_mid: list[float] = []
    for j, (rid, sev, detail) in enumerate(RULES):
        y = RY + j * (RHE + RGAP)
        rule_mid.append(y + RHE / 2)
        cap = s[sev]
        cap_bg = s["warn_bg"] if sev == "warn" else s["info_bg"]
        add(f'<g><rect x="{RX}" y="{y}" width="{RWID}" height="{RHE}" rx="14" '
            f'fill="{s["panel"]}" stroke="{s["node_edge"]}" stroke-width="1"/>')
        add(f'<rect x="{RX + 1}" y="{y + 10}" width="3" height="{RHE - 20}" '
            f'rx="1.5" fill="{cap}"/>')
        add(svg_text(RX + 16, y + 20, rid, 13.5, s["text"],
                     mono=True, weight="700"))
        pill_w = tw(sev, 11, mono=True) + 18
        add(svg_pill(RX + RWID - 14 - pill_w, y + 9, pill_w, 20, cap_bg))
        add(svg_text(RX + RWID - 14 - pill_w / 2, y + 23.5, sev, 11, cap,
                     mono=True, anchor="middle"))
        add(svg_text(RX + 16, y + 38, detail, 13, s["sub"], mono=False))
        add('</g>')
        checked(rid, 13.5, 80, "rule id", mono=True)
        checked(detail, 13, RWID - 32, "rule detail")

    # ---- wiring -------------------------------------------------------------
    for fi, targets in WIRES.items():
        for ri in targets:
            x1, y1 = FX + FWID, field_mid[fi]
            x2, y2 = RX, rule_mid[ri]
            add(f'<path d="M{x1:g} {y1:g} C {x1 + 76:g} {y1:g}, '
                f'{x2 - 76:g} {y2:g}, {x2:g} {y2:g}" fill="none" '
                f'stroke="{s["wire"]}" stroke-opacity="{s["wire_op"]}" '
                f'stroke-width="1.6"/>')
            add(f'<circle cx="{x1:g}" cy="{y1:g}" r="2.6" '
                f'fill="{s["wire"]}" fill-opacity="0.55"/>')
            add(f'<circle cx="{x2:g}" cy="{y2:g}" r="2.6" fill="{s["wire"]}" '
                f'fill-opacity="0.75"/>')

    # ---- output bus ---------------------------------------------------------
    bus_y = 508
    add(f'<path d="M670 {RY + 7 * (RHE + RGAP) - RGAP:g} V{bus_y}" '
        f'fill="none" stroke="{s["faint"]}" stroke-width="1.4"/>')
    add(f'<path d="M{CX1 + CW / 2:g} {bus_y} H{CX2 + CW / 2:g}" fill="none" '
        f'stroke="{s["faint"]}" stroke-width="1.4"/>')
    for cx in (CX1 + CW / 2, CX2 + CW / 2):
        add(f'<path d="M{cx:g} {bus_y} V{CY - 4}" fill="none" '
            f'stroke="{s["faint"]}" stroke-width="1.4"/>')
        add(f'<path d="M{cx - 5:g} {CY - 6} L{cx:g} {CY - 1} L{cx + 5:g} '
            f'{CY - 6}" fill="none" stroke="{s["faint"]}" stroke-width="1.4" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')

    # ---- exits --------------------------------------------------------------
    cards = [
        (CX1, "issues[]", "1 条 warn", s["warn"], s["warn_bg"],
         ["EG-001 · 第 1 行", "guideName、guideCode 都为空",
          "→ 补填适用导则名称与编号"]),
        (CX2, "skipped[]", "1 条", s["info"], s["info_bg"],
         ["EG-003 · values 未配置", "状态取值口径由本机构规定",
          "→ 本条不执行，不是静默通过"]),
    ]
    for cx, title, count, tone, tone_bg, body in cards:
        add(f'<g filter="url(#soft)"><rect x="{cx}" y="{CY}" width="{CW}" '
            f'height="{CH}" rx="18" fill="{s["panel"]}" '
            f'stroke="{s["node_edge"]}" stroke-width="1"/></g>')
        add(svg_text(cx + 16, CY + 26, title, 13, s["text"], mono=True,
                     weight="700"))
        pill_w = tw(count, 11, mono=False) + 18
        add(svg_pill(cx + CW - 16 - pill_w, CY + 12, pill_w, 20, tone_bg))
        add(svg_text(cx + CW - 16 - pill_w / 2, CY + 26.5, count, 11, tone,
                     anchor="middle"))
        add(svg_text(cx + 16, CY + 50, body[0], 12.5, s["text"],
                     mono=True, weight="700"))
        add(svg_text(cx + 16, CY + 70, body[1], 11.5, s["sub"]))
        add(svg_text(cx + 16, CY + 89, body[2], 11.5, s["faint"]))
        checked(body[1], 11.5, CW - 32, "exit line")

    # ---- reading note + footer ---------------------------------------------
    add(svg_text(40, 552, "空清单 ≠ 没问题", 14, s["accent"], weight="700"))
    add(svg_text(40, 576, "跑不了的检查逐条进 skipped[] 并写明原因；",
                 12, s["sub"]))
    add(svg_text(40, 598, "跑过而未命中的规则，两栏都不进。",
                 12, s["sub"]))
    add(svg_text(40, 620, "结论留给审核人：不判合规、不认定责任。",
                 12, s["sub"]))
    add(svg_text(40, 486, "行栏目 12 个、表头字段 5 个，本包只读这 8 栏；",
                 11.5, s["faint"]))
    add(svg_text(40, 502, "列名别名忽略大小写、空格、_ 与 -，其余照原样保留。",
                 11.5, s["faint"]))
    add(svg_text(40, 644, "Apache-2.0 · 只读材料 · 不联网 · 不调用模型 · "
                 "本图为结构说明，不构成合规结论", 11.5, s["faint"]))

    add('</svg>')
    svg = "\n".join(parts) + "\n"
    ET.fromstring(svg)  # well-formedness gate
    return svg


# ---------------------------------------------------------------------------
def main() -> None:
    written: list[str] = []
    for lang in ("zh", "en"):
        for skin in ("light", "dark"):
            path = os.path.join(OUT, f"{NAME}-hero-{lang}-{skin}.webp")
            draw_hero(lang, skin).save(path, "WEBP", quality=90, method=6)
            written.append(os.path.basename(path))
    for skin in ("light", "dark"):
        path = os.path.join(OUT, f"{NAME}-flow-v5-{skin}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin))
        written.append(os.path.basename(path))
    print("wrote " + str(len(written)) + " assets to docs/assets/:")
    for name in written:
        print("  " + name)


if __name__ == "__main__":
    main()

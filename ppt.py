"""
ppt.py — Pitch Deck Generator for ThynxAI
Takes slide JSON from Gemini → builds .pptx file
No API calls here — just slide building.
"""

import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN


# ─── Theme Colors (Midnight Blue) ────────────────────────────────────────────

BG_DARK    = RGBColor(0x1E, 0x27, 0x61)   # Navy — main background
BG_CARD    = RGBColor(0x16, 0x1D, 0x4E)   # Darker navy — card background
ACCENT     = RGBColor(0xCA, 0xDC, 0xFC)   # Ice blue — titles and highlights
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)   # White — body text
MUTED      = RGBColor(0x8A, 0x9A, 0xCC)   # Muted blue — subtitles
HIGHLIGHT  = RGBColor(0x4A, 0x6C, 0xF7)   # Bright blue — accent bar


# ─── Slide Dimensions (16x9) ─────────────────────────────────────────────────

W = 10.0   # inches
H = 5.625  # inches


# ─── Helper Functions ─────────────────────────────────────────────────────────

def add_background(slide):
    """Fills entire slide with dark navy background."""
    bg = slide.shapes.add_shape(
        1,  # RECTANGLE
        Inches(0), Inches(0), Inches(W), Inches(H)
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()


def add_accent_bar(slide, y=0.55, width=1.2):
    """Adds a small bright blue horizontal bar under the title."""
    bar = slide.shapes.add_shape(
        1,
        Inches(0.5), Inches(y), Inches(width), Inches(0.04)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = HIGHLIGHT
    bar.line.fill.background()


def add_title(slide, text, y=0.25, size=32):
    """Adds a slide title in ice blue."""
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(y), Inches(9), Inches(0.6))
    tf = txBox.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = ACCENT
    run.font.name = "Calibri"


def add_subtitle(slide, text, y=0.85, size=14):
    """Adds subtitle or small label text in white."""
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(y), Inches(9), Inches(0.4))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = WHITE
    run.font.name = "Calibri"


def add_bullets(slide, bullets, y_start=1.2, size=15):
    """Adds bullet points in white text."""
    txBox = slide.shapes.add_textbox(Inches(0.7), Inches(y_start), Inches(8.8), Inches(H - y_start - 0.3))
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, bullet in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(10)
        run = p.add_run()
        run.text = f"→  {bullet}"
        run.font.size = Pt(size)
        run.font.color.rgb = WHITE
        run.font.name = "Calibri"


def add_stat_box(slide, stat_text):
    """Adds a big highlighted stat box on the right side."""
    box = slide.shapes.add_shape(
        1,
        Inches(6.8), Inches(1.3), Inches(2.8), Inches(1.4)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = HIGHLIGHT
    box.line.fill.background()

    txBox = slide.shapes.add_textbox(Inches(6.85), Inches(1.35), Inches(2.7), Inches(1.3))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = stat_text
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = WHITE
    run.font.name = "Calibri"


def add_footer(slide, text="ThynxAI Idea Lab"):
    """Adds a small footer at the bottom."""
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(5.2), Inches(9), Inches(0.3))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = text
    run.font.size = Pt(9)
    run.font.color.rgb = ACCENT
    run.font.name = "Calibri"


# ─── Slide Builders ───────────────────────────────────────────────────────────

def build_cover_slide(prs, data):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)

    # Center vertical line accent
    line = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.08), Inches(H))
    line.fill.solid()
    line.fill.fore_color.rgb = HIGHLIGHT
    line.line.fill.background()

    # Title
    txBox = slide.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(9), Inches(1.2))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = data.get("title", "Startup Idea")
    run.font.size = Pt(40)
    run.font.bold = True
    run.font.color.rgb = ACCENT
    run.font.name = "Calibri"

    # Subtitle
    txBox2 = slide.shapes.add_textbox(Inches(0.6), Inches(2.9), Inches(9), Inches(0.6))
    tf2 = txBox2.text_frame
    p2 = tf2.paragraphs[0]
    run2 = p2.add_run()
    run2.text = data.get("subtitle", "")
    run2.font.size = Pt(16)
    run2.font.color.rgb = WHITE
    run2.font.name = "Calibri"

    # Founder name
    txBox3 = slide.shapes.add_textbox(Inches(0.6), Inches(4.4), Inches(9), Inches(0.4))
    tf3 = txBox3.text_frame
    p3 = tf3.paragraphs[0]
    run3 = p3.add_run()
    run3.text = f"Founder: {data.get('founder', '')}"
    run3.font.size = Pt(12)
    run3.font.color.rgb = ACCENT
    run3.font.name = "Calibri"

    add_footer(slide)


def build_content_slide(prs, data):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)
    add_title(slide, data.get("title", ""))
    add_accent_bar(slide)
    add_bullets(slide, data.get("bullets", []))

    # Add stat box if present
    if data.get("stat"):
        add_stat_box(slide, data["stat"])

    # Add gap/advantage label if present (competition slide)
    if data.get("gap"):
        add_subtitle(slide, f"Our Edge: {data['gap']}", y=4.8, size=12)

    add_footer(slide)


def build_closing_slide(prs, data):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide)

    # Bottom accent bar
    bar = slide.shapes.add_shape(1, Inches(0), Inches(H - 0.08), Inches(W), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = HIGHLIGHT
    bar.line.fill.background()

    # Big closing title
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(9), Inches(1.0))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = data.get("title", "Let's Build Together")
    run.font.size = Pt(36)
    run.font.bold = True
    run.font.color.rgb = ACCENT
    run.font.name = "Calibri"

    # Subtitle
    txBox2 = slide.shapes.add_textbox(Inches(0.5), Inches(3.0), Inches(9), Inches(0.6))
    tf2 = txBox2.text_frame
    p2 = tf2.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    run2.text = data.get("subtitle", "")
    run2.font.size = Pt(15)
    run2.font.color.rgb = WHITE
    run2.font.name = "Calibri"

    add_footer(slide)


# ─── Main Generator ───────────────────────────────────────────────────────────

def generate_ppt(slides_data: list) -> bytes:
    """
    Takes list of slide dicts from Gemini.
    Returns .pptx file as bytes for Streamlit download.
    """
    prs = Presentation()
    prs.slide_width  = Inches(W)
    prs.slide_height = Inches(H)

    for slide_data in slides_data:
        slide_type = slide_data.get("slide", "")

        if slide_type == "cover":
            build_cover_slide(prs, slide_data)
        elif slide_type == "closing":
            build_closing_slide(prs, slide_data)
        else:
            build_content_slide(prs, slide_data)

    # Save to bytes (for Streamlit in-memory download)
    buffer = io.BytesIO()
    prs.save(buffer)
    buffer.seek(0)
    return buffer.read()
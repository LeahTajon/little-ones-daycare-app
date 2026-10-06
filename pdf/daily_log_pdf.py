from datetime import datetime, time
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Flowable,
)


# =========================================================
# DAILY LOG PDF
# =========================================================

def create_daily_log_pdf(file_path, daily_log):

    child = daily_log.child

    # ---------------------------------------------------------
    # PAGE
    # ---------------------------------------------------------

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=34,
        leftMargin=34,
        topMargin=32,
        bottomMargin=38,
    )

    PAGE_WIDTH = 612 - 34 - 34
    COLUMN_GAP = 12
    CARD_WIDTH = (PAGE_WIDTH - COLUMN_GAP) / 2

    elements = []

    # ---------------------------------------------------------
    # COLORS - GRAYSCALE ONLY
    # ---------------------------------------------------------

    PAGE_BG = colors.white
    CARD_BG = colors.white
    TABLE_BG = colors.white
    HEADER_BG = colors.HexColor("#E2E6EA")

    TEXT = colors.HexColor("#18212B")
    MUTED = colors.HexColor("#59636E")
    BORDER = colors.HexColor("#CDD3D9")
    GRID = colors.HexColor("#DDE2E7")
    WHITE = colors.white
    ICON = colors.HexColor("#1F2933")

    # ---------------------------------------------------------
    # STYLES
    # ---------------------------------------------------------

    styles = getSampleStyleSheet()

    brand_style = ParagraphStyle(
        "BrandStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        textColor=TEXT,
        spaceAfter=2,
    )

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        textColor=TEXT,
        spaceBefore=0,
        spaceAfter=3,
    )

    child_style = ParagraphStyle(
        "ChildStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
        textColor=TEXT,
        spaceBefore=0,
        spaceAfter=2,
    )

    date_style = ParagraphStyle(
        "DateStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        textColor=MUTED,
        spaceBefore=0,
        spaceAfter=0,
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=12,
        textColor=TEXT,
        spaceBefore=0,
        spaceAfter=0,
    )

    table_header_style = ParagraphStyle(
        "TableHeaderStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=6.2,
        leading=7.2,
        textColor=TEXT,
        spaceBefore=0,
        spaceAfter=0,
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=6.5,
        leading=7.8,
        textColor=TEXT,
        spaceBefore=0,
        spaceAfter=0,
        splitLongWords=True,
    )

    empty_style = ParagraphStyle(
        "EmptyStyle",
        parent=normal_style,
        fontSize=7,
        textColor=MUTED,
        alignment=TA_CENTER,
    )

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------

    def format_time(value):
        if not value:
            return "--"

        if isinstance(value, datetime):
            value = value.time()

        return value.strftime("%I:%M %p").lstrip("0")

    def format_datetime(value):
        if not value:
            return "--"

        return value.strftime("%I:%M %p").lstrip("0")

    def format_text(value):
        if value is None or str(value).strip() == "":
            return "--"

        return escape(str(value))

    def display_choice(value):
        """Make database choice values more readable in the PDF."""
        if value is None or str(value).strip() == "":
            return "--"

        value = str(value)

        special = {
            "wet": "Wet",
            "bm": "BM",
            "wet_bm": "Wet + BM",
            "toilet": "Toilet",
            "diaper": "Diaper",
            "pull_up": "Pull-Up",
            "training_potty": "Training Potty",
            "used_independently": "Used Independently",
            "used_with_assistance": "Used With Assistance",
            "sat_on_potty": "Sat on Potty",
            "tried_no_result": "Tried - No Result",
            "refused": "Refused",
            "had_an_accident": "Had an Accident",
        }

        return escape(special.get(value, value.replace("_", " ").title()))

    def sorted_logs(logs, attribute):
        return sorted(
            logs or [],
            key=lambda x: getattr(x, attribute, None)
            or time.min
        )

    class DaycareLogo(Flowable):
        """Small monochrome sun/rainbow logo for the PDF header."""

        def __init__(self, width=72, height=44):
            super().__init__()
            self.width = width
            self.height = height

        def draw(self):
            c = self.canv
            w = self.width
            h = self.height

            c.saveState()
            c.setStrokeColor(ICON)
            c.setFillColor(colors.transparent)
            c.setLineWidth(1.4)

            # Sun
            cx = w * 0.50
            cy = h * 0.78
            r = h * 0.16
            c.circle(cx, cy, r, stroke=1, fill=0)

            for angle in range(0, 360, 45):
                import math
                a = math.radians(angle)
                c.line(
                    cx + math.cos(a) * r * 1.35,
                    cy + math.sin(a) * r * 1.35,
                    cx + math.cos(a) * r * 1.75,
                    cy + math.sin(a) * r * 1.75,
                )

            # Rainbow arcs
            for offset in (0, 5, 10):
                c.arc(
                    w * 0.10 + offset / 2,
                    h * 0.03 + offset / 2,
                    w * 0.90 - offset / 2,
                    h * 0.75 - offset / 2,
                    0,
                    180,
                )

            # Clouds
            c.circle(w * 0.14, h * 0.13, h * 0.10, stroke=1, fill=0)
            c.circle(w * 0.23, h * 0.17, h * 0.14, stroke=1, fill=0)
            c.circle(w * 0.32, h * 0.13, h * 0.10, stroke=1, fill=0)

            c.circle(w * 0.68, h * 0.13, h * 0.10, stroke=1, fill=0)
            c.circle(w * 0.77, h * 0.17, h * 0.14, stroke=1, fill=0)
            c.circle(w * 0.86, h * 0.13, h * 0.10, stroke=1, fill=0)

            c.restoreState()


    # ---------------------------------------------------------
    # SIMPLE VECTOR ICONS
    # ---------------------------------------------------------

    class LogIcon(Flowable):
        """
        Small line-style icons drawn directly by ReportLab.
        This avoids depending on an external icon/font package.
        """

        def __init__(self, icon_name, size=23, stroke_color=TEXT):
            super().__init__()
            self.icon_name = icon_name
            self.size = size
            self.stroke_color = stroke_color
            self.width = size
            self.height = size

        def draw(self):
            c = self.canv
            s = self.size
            c.saveState()

            c.setStrokeColor(self.stroke_color)
            c.setFillColor(colors.transparent)
            c.setLineWidth(1.5)
            c.setLineCap(1)
            c.setLineJoin(1)

            # Bottle
            if self.icon_name == "bottle":
                c.roundRect(s * .30, s * .08, s * .40, s * .62, 3, stroke=1, fill=0)
                c.line(s * .38, s * .70, s * .38, s * .88)
                c.line(s * .62, s * .70, s * .62, s * .88)
                c.line(s * .38, s * .88, s * .62, s * .88)
                c.line(s * .43, s * .76, s * .57, s * .76)

            # Meal / utensils
            elif self.icon_name == "meal":
                c.line(s * .25, s * .12, s * .25, s * .88)
                c.line(s * .17, s * .88, s * .17, s * .68)
                c.line(s * .25, s * .88, s * .25, s * .68)
                c.line(s * .33, s * .88, s * .33, s * .68)
                c.line(s * .58, s * .12, s * .58, s * .88)
                c.arc(s * .43, s * .62, s * .73, s * .94, 0, 180)
                c.line(s * .73, s * .78, s * .73, s * .12)

            # Diaper
            elif self.icon_name == "diaper":
                p = c.beginPath()
                p.moveTo(s * .12, s * .72)
                p.lineTo(s * .88, s * .72)
                p.lineTo(s * .80, s * .20)
                p.curveTo(
                    s * .68, s * .10,
                    s * .56, s * .12,
                    s * .50, s * .30
                )
                p.curveTo(
                    s * .44, s * .12,
                    s * .32, s * .10,
                    s * .20, s * .20
                )
                p.close()
                c.drawPath(p, stroke=1, fill=0)
                c.line(s * .20, s * .60, s * .35, s * .43)
                c.line(s * .80, s * .60, s * .65, s * .43)

            # Potty
            elif self.icon_name == "potty":
                c.roundRect(s * .22, s * .28, s * .56, s * .30, 5, stroke=1, fill=0)
                c.arc(s * .30, s * .52, s * .70, s * .88, 0, 180)
                c.line(s * .30, s * .28, s * .25, s * .10)
                c.line(s * .70, s * .28, s * .75, s * .10)
                c.line(s * .25, s * .10, s * .75, s * .10)

            # Nap
            elif self.icon_name == "nap":
                c.setFont("Helvetica-Bold", s * .42)
                c.drawString(s * .18, s * .30, "Z")
                c.setFont("Helvetica-Bold", s * .27)
                c.drawString(s * .50, s * .55, "Z")
                c.setFont("Helvetica-Bold", s * .18)
                c.drawString(s * .70, s * .72, "Z")

            # Activity / running person
            elif self.icon_name == "activity":
                c.circle(s * .64, s * .76, s * .11, stroke=1, fill=0)
                c.line(s * .58, s * .65, s * .43, s * .43)
                c.line(s * .43, s * .43, s * .25, s * .45)
                c.line(s * .43, s * .43, s * .58, s * .22)
                c.line(s * .43, s * .43, s * .31, s * .17)
                c.line(s * .55, s * .58, s * .75, s * .52)

            # Health heart / pulse
            elif self.icon_name == "health":
                p = c.beginPath()
                p.moveTo(s * .50, s * .15)
                p.curveTo(
                    s * .42, s * .25,
                    s * .15, s * .42,
                    s * .15, s * .62
                )
                p.curveTo(
                    s * .15, s * .84,
                    s * .38, s * .88,
                    s * .50, s * .72
                )
                p.curveTo(
                    s * .62, s * .88,
                    s * .85, s * .84,
                    s * .85, s * .62
                )
                p.curveTo(
                    s * .85, s * .42,
                    s * .58, s * .25,
                    s * .50, s * .15
                )
                c.drawPath(p, stroke=1, fill=0)
                c.line(s * .22, s * .54, s * .38, s * .54)
                c.line(s * .38, s * .54, s * .43, s * .42)
                c.line(s * .43, s * .42, s * .52, s * .65)
                c.line(s * .52, s * .65, s * .58, s * .54)
                c.line(s * .58, s * .54, s * .78, s * .54)

            c.restoreState()

    # ---------------------------------------------------------
    # TABLE CREATOR
    # ---------------------------------------------------------

    def create_table(data, col_widths, available_width=None):
        formatted_data = []

        # Keep the table inside the card. The supplied widths are treated
        # as proportions when their total is larger than the available width.
        if available_width is not None:
            total_width = sum(col_widths)
            if total_width > available_width and total_width > 0:
                scale = available_width / total_width
                col_widths = [width * scale for width in col_widths]

            # Never allow rounding or a manually edited width list to make
            # the table wider than the card.
            total_width = sum(col_widths)
            if total_width > available_width and total_width > 0:
                scale = available_width / total_width
                col_widths = [width * scale for width in col_widths]

        for row_index, row in enumerate(data):
            formatted_row = []

            for cell in row:
                if row_index == 0:
                    formatted_row.append(
                        Paragraph(str(cell), table_header_style)
                    )
                else:
                    formatted_row.append(
                        Paragraph(format_text(cell), normal_style)
                    )

            formatted_data.append(formatted_row)

        table = Table(
            formatted_data,
            colWidths=col_widths,
            repeatRows=1,
            hAlign="LEFT",
        )

        table_style = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E6EA")),
            ("LINEBELOW", (0, 0), (-1, 0), 0.6, BORDER),
            ("LINEBELOW", (0, 1), (-1, -1), 0.35, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
        ]

        for row_index in range(1, len(formatted_data)):
            if row_index % 2 == 0:
                table_style.append(
                    (
                        "BACKGROUND",
                        (0, row_index),
                        (-1, row_index),
                        colors.HexColor("#FFFFFF"),
                    )
                )

        table.setStyle(TableStyle(table_style))

        return table

    # ---------------------------------------------------------
    # LOG CARD
    # ---------------------------------------------------------

    def create_log_card(
        title,
        icon_name,
        data,
        col_widths,
        background,
        accent,
    ):
        inner_width = CARD_WIDTH - 14

        icon = LogIcon(
            icon_name,
            size=22,
            stroke_color=accent,
        )

        header = Table(
            [
                [
                    Paragraph(title, section_style),
                ]
            ],
            colWidths=[inner_width],
            hAlign="LEFT",
        )

        header.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )

        data_table = create_table(
            data,
            col_widths,
            available_width=inner_width,
        )

        card = Table(
            [
                [header],
                [data_table],
            ],
            colWidths=[inner_width],
            hAlign="LEFT",
        )

        card.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), background),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, 0), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
                    ("TOPPADDING", (0, 1), (-1, 1), 0),
                    ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
                ]
            )
        )

        return card

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    elements.append(Spacer(1, 2))

    brand_name_style = ParagraphStyle(
        "BrandNameStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16,
        textColor=TEXT,
        alignment=TA_LEFT,
    )

    brand_sub_style = ParagraphStyle(
        "BrandSubStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_LEFT,
    )

    tagline_style = ParagraphStyle(
        "TaglineStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_RIGHT,
    )

    brand_table = Table(
        [
            [
                Paragraph(
                    "<b>LITTLE ONES TOO</b><br/>"
                    "<font size='8'>D A Y C A R E</font>",
                    brand_name_style,
                ),
                Paragraph(
                    "Little Steps. Big Futures.",
                    tagline_style,
                ),
            ]
        ],
        colWidths=[PAGE_WIDTH * 0.62, PAGE_WIDTH * 0.38],
    )

    brand_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    elements.append(brand_table)
    elements.append(Spacer(1, 7))

    # Main title block
    title_block = Table(
        [
            [
                Paragraph("Daily Log Report", title_style),
            ],
            [
                Paragraph(
                    f"{escape(child.first_name)} {escape(child.last_name)}",
                    child_style,
                )
            ],
            [
                Paragraph(
                    daily_log.log_date.strftime("%B %d, %Y"),
                    date_style,
                )
            ],
        ],
        colWidths=[PAGE_WIDTH],
    )

    title_block.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HEADER_BG),
                ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 3),
                ("TOPPADDING", (0, 1), (-1, 1), 0),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 2),
                ("TOPPADDING", (0, 2), (-1, 2), 0),
                ("BOTTOMPADDING", (0, 2), (-1, 2), 9),
            ]
        )
    )

    elements.append(title_block)

    elements.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # DETERMINE CLASS
    # ---------------------------------------------------------

    child_class = child.determine_class()

    # ---------------------------------------------------------
    # BUILD LOG CARDS
    # ---------------------------------------------------------

    cards = []

    # =========================================================
    # INFANT
    # =========================================================

    if child_class == "Infant":

        bottles = sorted(
            daily_log.bottle_logs or [],
            key=lambda x: x.time or time.min,
        )

        if bottles:
            data = [["Time", "Bottle Type", "Amount", "Notes"]]

            for bottle in bottles:
                amount = (
                    f"{bottle.amount_offered:g} oz"
                    if bottle.amount_offered is not None
                    else "--"
                )

                data.append(
                    [
                        format_time(bottle.time),
                        display_choice(bottle.bottle_type),
                        amount,
                        format_text(bottle.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Bottle",
                    "bottle",
                    data,
                    [48, 62, 48, 94],
                    CARD_BG,
                    ICON,
                )
            )

        meals = sorted(
            daily_log.meal_logs or [],
            key=lambda x: x.time or time.min,
        )

        if meals:
            data = [["Time", "Meal", "Food", "Amount", "Notes"]]

            for meal in meals:
                data.append(
                    [
                        format_time(meal.time),
                        display_choice(meal.meal_type),
                        format_text(meal.food),
                        format_text(meal.amount),
                        format_text(meal.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Meals",
                    "meal",
                    data,
                    [38, 45, 62, 42, 65],
                    CARD_BG,
                    ICON,
                )
            )

        diapers = sorted(
            daily_log.diaper_logs or [],
            key=lambda x: x.time or time.min,
        )

        if diapers:
            data = [["Time", "Type", "Description", "Notes"]]

            for diaper in diapers:
                data.append(
                    [
                        format_time(diaper.time),
                        display_choice(diaper.diaper_type),
                        format_text(diaper.diaper_desc),
                        format_text(diaper.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Diaper",
                    "diaper",
                    data,
                    [45, 50, 62, 95],
                    CARD_BG,
                    ICON,
                )
            )

        naps = sorted(
            daily_log.nap_logs or [],
            key=lambda x: x.start_time or time.min,
        )

        if naps:
            data = [["Start Time", "End Time", "Notes"]]

            for nap in naps:
                data.append(
                    [
                        format_time(nap.start_time),
                        format_time(nap.end_time),
                        format_text(nap.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Nap",
                    "nap",
                    data,
                    [60, 60, 132],
                    CARD_BG,
                    ICON,
                )
            )

    # =========================================================
    # TODDLER / PRE-K
    # =========================================================

    elif child_class in ["Toddler", "Pre-K"]:

        meals = sorted(
            daily_log.meal_logs or [],
            key=lambda x: x.time or time.min,
        )

        if meals:
            data = [["Time", "Meal", "Food", "Amount", "Notes"]]

            for meal in meals:
                data.append(
                    [
                        format_time(meal.time),
                        display_choice(meal.meal_type),
                        format_text(meal.food),
                        format_text(meal.amount),
                        format_text(meal.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Meals",
                    "meal",
                    data,
                    [38, 45, 62, 42, 65],
                    CARD_BG,
                    ICON,
                )
            )

        potty_logs = sorted(
            daily_log.potty_logs or [],
            key=lambda x: x.time or datetime.min,
        )

        if potty_logs:
            data = [["Time", "Status", "Method", "Progress", "Notes"]]

            for potty in potty_logs:
                data.append(
                    [
                        format_datetime(potty.time),
                        display_choice(potty.potty_status),
                        display_choice(potty.potty_method),
                        display_choice(potty.potty_progress),
                        format_text(potty.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Potty",
                    "potty",
                    data,
                    [38, 45, 48, 62, 59],
                    CARD_BG,
                    ICON,
                )
            )

        naps = sorted(
            daily_log.nap_logs or [],
            key=lambda x: x.start_time or time.min,
        )

        if naps:
            data = [["Start Time", "End Time", "Notes"]]

            for nap in naps:
                data.append(
                    [
                        format_time(nap.start_time),
                        format_time(nap.end_time),
                        format_text(nap.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Nap",
                    "nap",
                    data,
                    [60, 60, 132],
                    CARD_BG,
                    ICON,
                )
            )

        activities = sorted(
            daily_log.activity_logs or [],
            key=lambda x: x.time or time.min,
        )

        if activities:
            data = [["Time", "Activity", "Notes"]]

            for activity in activities:
                data.append(
                    [
                        format_time(activity.time),
                        format_text(activity.activity),
                        format_text(activity.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Activity",
                    "activity",
                    data,
                    [48, 95, 109],
                    CARD_BG,
                    ICON,
                )
            )

    # =========================================================
    # AFTER SCHOOL
    # =========================================================

    elif child_class == "After School":

        meals = sorted(
            daily_log.meal_logs or [],
            key=lambda x: x.time or time.min,
        )

        if meals:
            data = [["Time", "Meal", "Food", "Amount", "Notes"]]

            for meal in meals:
                data.append(
                    [
                        format_time(meal.time),
                        display_choice(meal.meal_type),
                        format_text(meal.food),
                        format_text(meal.amount),
                        format_text(meal.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Meals",
                    "meal",
                    data,
                    [38, 45, 62, 42, 65],
                    CARD_BG,
                    ICON,
                )
            )

        naps = sorted(
            daily_log.nap_logs or [],
            key=lambda x: x.start_time or time.min,
        )

        if naps:
            data = [["Start Time", "End Time", "Notes"]]

            for nap in naps:
                data.append(
                    [
                        format_time(nap.start_time),
                        format_time(nap.end_time),
                        format_text(nap.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Nap",
                    "nap",
                    data,
                    [60, 60, 132],
                    CARD_BG,
                    ICON,
                )
            )

        activities = sorted(
            daily_log.activity_logs or [],
            key=lambda x: x.time or time.min,
        )

        if activities:
            data = [["Time", "Activity", "Notes"]]

            for activity in activities:
                data.append(
                    [
                        format_time(activity.time),
                        format_text(activity.activity),
                        format_text(activity.notes),
                    ]
                )

            cards.append(
                create_log_card(
                    "Activity",
                    "activity",
                    data,
                    [48, 95, 109],
                    CARD_BG,
                    ICON,
                )
            )

    # ---------------------------------------------------------
    # TWO-COLUMN LAYOUT
    # ---------------------------------------------------------

    if cards:
        rows = []

        for index in range(0, len(cards), 2):
            left = cards[index]
            right = cards[index + 1] if index + 1 < len(cards) else ""

            rows.append([left, right])

        log_grid = Table(
            rows,
            colWidths=[CARD_WIDTH, CARD_WIDTH],
            hAlign="CENTER",
        )

        log_grid.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elements.append(log_grid)

    # ---------------------------------------------------------
    # HEALTH CHECK - FULL WIDTH
    # ---------------------------------------------------------

    health = daily_log.health_check

    if health:
        data = [
            ["Temperature", "Symptoms", "Notes"],
            [
                (
                    f"{health.temperature:.1f} °F"
                    if health.temperature is not None
                    else "--"
                ),
                format_text(health.symptoms),
                format_text(health.notes),
            ],
        ]

        health_card = create_full_width_card(
            title="Health Check",
            icon_name="health",
            data=data,
            col_widths=[90, 165, 277],
            background=CARD_BG,
            accent=ICON,
        )

        elements.append(health_card)
        elements.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # DAILY NOTES - FULL WIDTH
    # ---------------------------------------------------------

    if daily_log.notes and str(daily_log.notes).strip():

        notes_data = [
            [
                Paragraph(
                    format_text(daily_log.notes),
                    normal_style,
                )
            ]
        ]

        notes_table = Table(
            notes_data,
            colWidths=[PAGE_WIDTH],
        )

        notes_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                ]
            )
        )

        notes_header = Table(
            [
                [
                    LogIcon("health", 20, ICON),
                    Paragraph("Daily Notes", section_style),
                ]
            ],
            colWidths=[28, PAGE_WIDTH - 28],
        )

        notes_header.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )

        elements.append(notes_header)
        elements.append(notes_table)

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------

    def draw_footer(canvas, doc):
        canvas.saveState()

        # Gray paper background
        canvas.setFillColor(PAGE_BG)
        canvas.rect(
            0,
            0,
            letter[0],
            letter[1],
            stroke=0,
            fill=1,
        )

        # Keep content areas visually white/gray through their tables.
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.6)
        canvas.line(
            55,
            25,
            557,
            25,
        )

        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(
            55,
            13,
            "Thank you for being a part of our daycare family!",
        )

        canvas.drawRightString(
            557,
            13,
            f"Page {doc.page}",
        )

        canvas.restoreState()

    # ---------------------------------------------------------
    # BUILD
    # ---------------------------------------------------------

    doc.build(
        elements,
        onFirstPage=draw_footer,
        onLaterPages=draw_footer,
    )


# =========================================================
# FULL-WIDTH CARD HELPER
# =========================================================

def create_full_width_card(
    title,
    icon_name,
    data,
    col_widths,
    background,
    accent,
):
    PAGE_WIDTH = 612 - 34 - 34

    styles = getSampleStyleSheet()

    section_style = ParagraphStyle(
        "FullWidthSectionStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        textColor=colors.HexColor("#18212B"),
    )

    table_header_style = ParagraphStyle(
        "FullWidthHeaderStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=6.2,
        leading=7.2,
        textColor=colors.HexColor("#18212B"),
    )

    normal_style = ParagraphStyle(
        "FullWidthNormalStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=6.5,
        leading=7.8,
        textColor=colors.HexColor("#18212B"),
    )

    def clean(value):
        if value is None or str(value).strip() == "":
            return "--"
        return escape(str(value))

    formatted = []

    for row_index, row in enumerate(data):
        formatted.append(
            [
                Paragraph(
                    str(cell) if row_index == 0 else clean(cell),
                    table_header_style if row_index == 0 else normal_style,
                )
                for cell in row
            ]
        )

    inner = Table(
        formatted,
        colWidths=col_widths,
        repeatRows=1,
    )

    inner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E6EA")),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#CDD3D9")),
                ("LINEBELOW", (0, 1), (-1, -1), 0.35, colors.HexColor("#CDD3D9")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 3.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
            ]
        )
    )

    header = Table(
        [[Paragraph(title, section_style)]],
        colWidths=[PAGE_WIDTH],
    )

    header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    card = Table(
        [
            [header],
            [inner],
        ],
        colWidths=[PAGE_WIDTH],
    )

    card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, 0), 0),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
                ("TOPPADDING", (0, 1), (-1, 1), 0),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
            ]
        )
    )

    return card


from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether
)

from datetime import date


# =========================================================
# STUDENT DIRECTORY PDF
# =========================================================

def create_student_directory_pdf(file_path, children):

    today = date.today()

    # ---------------------------------------------------------
    # PAGE
    # ---------------------------------------------------------

    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(letter),
        rightMargin=34,
        leftMargin=34,
        topMargin=32,
        bottomMargin=38,
    )

    PAGE_WIDTH = 792 - 34 - 34

    elements = []

    # ---------------------------------------------------------
    # COLORS
    # Matches the Daily Log PDF
    # ---------------------------------------------------------

    PAGE_BG = colors.white
    HEADER_BG = colors.HexColor("#E2E6EA")

    TEXT = colors.HexColor("#18212B")
    MUTED = colors.HexColor("#59636E")
    BORDER = colors.HexColor("#CDD3D9")
    GRID = colors.HexColor("#DDE2E7")

    # ---------------------------------------------------------
    # STYLES
    # ---------------------------------------------------------

    styles = getSampleStyleSheet()

    brand_name_style = ParagraphStyle(
        "StudentDirectoryBrandName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16,
        textColor=TEXT,
        alignment=TA_LEFT,
    )

    tagline_style = ParagraphStyle(
        "StudentDirectoryTagline",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_RIGHT,
    )

    title_style = ParagraphStyle(
        "StudentDirectoryTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=21,
        alignment=TA_CENTER,
        textColor=TEXT,
        spaceBefore=0,
        spaceAfter=3,
    )

    subtitle_style = ParagraphStyle(
        "StudentDirectorySubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=MUTED,
        spaceBefore=0,
        spaceAfter=0,
    )

    section_style = ParagraphStyle(
        "StudentDirectorySection",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=12,
        textColor=TEXT,
    )

    table_header_style = ParagraphStyle(
        "StudentDirectoryTableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=8.2,
        textColor=TEXT,
        spaceBefore=0,
        spaceAfter=0,
    )

    normal_style = ParagraphStyle(
        "StudentDirectoryNormal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=8.8,
        textColor=TEXT,
        spaceBefore=0,
        spaceAfter=0,
        splitLongWords=True,
    )

    student_name_style = ParagraphStyle(
        "StudentDirectoryStudentName",
        parent=normal_style,
        fontName="Helvetica-Bold",
    )

    summary_style = ParagraphStyle(
        "StudentDirectorySummary",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9,
        textColor=MUTED,
        alignment=TA_RIGHT,
    )

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------

    def clean(value):
        if value is None or str(value).strip() == "":
            return "--"

        return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def calculate_age(dob):

        if not dob:
            return "—"

        return (
            today.year
            - dob.year
            - (
                (today.month, today.day)
                < (dob.month, dob.day)
            )
        )

    # ---------------------------------------------------------
    # BRAND HEADER
    # Matches Daily Log PDF
    # ---------------------------------------------------------

    elements.append(Spacer(1, 2))

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
        colWidths=[
            PAGE_WIDTH * 0.62,
            PAGE_WIDTH * 0.38,
        ],
    )

    brand_table.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
            ]
        )
    )

    elements.append(brand_table)

    elements.append(Spacer(1, 7))

    # ---------------------------------------------------------
    # TITLE BLOCK
    # ---------------------------------------------------------

    title_block = Table(
        [
            [
                Paragraph(
                    "Student Directory",
                    title_style,
                )
            ],
            [
                Paragraph(
                    (
                        f"Complete list of registered students"
                        f"<br/>"
                        f"Generated {today.strftime('%B %d, %Y')}"
                    ),
                    subtitle_style,
                )
            ],
        ],
        colWidths=[PAGE_WIDTH],
    )

    title_block.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    HEADER_BG,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    BORDER,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, 0),
                    9,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    3,
                ),
                (
                    "TOPPADDING",
                    (0, 1),
                    (-1, 1),
                    0,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 1),
                    (-1, 1),
                    9,
                ),
            ]
        )
    )

    elements.append(title_block)

    elements.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # REPORT SUMMARY
    # ---------------------------------------------------------

    summary_table = Table(
        [
            [
                Paragraph(
                    "REGISTERED STUDENTS",
                    table_header_style,
                ),
                Paragraph(
                    f"{len(children)} "
                    f"{'student' if len(children) == 1 else 'students'}",
                    summary_style,
                ),
            ]
        ],
        colWidths=[
            PAGE_WIDTH * 0.60,
            PAGE_WIDTH * 0.40,
        ],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    BORDER,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    elements.append(summary_table)

    elements.append(Spacer(1, 7))

    # ---------------------------------------------------------
    # TABLE DATA
    # ---------------------------------------------------------

    data = [
        [
            Paragraph("Student", table_header_style),
            Paragraph("Age", table_header_style),
            Paragraph("Gender", table_header_style),
            Paragraph("Class", table_header_style),
            Paragraph("Program", table_header_style),
            Paragraph("Days Attending", table_header_style),
            Paragraph("Enrolled", table_header_style),
        ]
    ]

    for child in children:

        # Student name
        student_name = (
            f"{clean(child.first_name)} "
            f"{clean(child.last_name)}"
        )

        # Gender
        gender = (
            child.gender.title()
            if child.gender
            else "—"
        )

        # Class
        class_name = (
            clean(child.class_name)
            if child.class_name
            else "—"
        )

        # Program
        program = (
            clean(child.program_type)
            if child.program_type
            else "—"
        )

        # Days attending
        days = (
            clean(child.days_attending)
            if child.days_attending
            else "—"
        )

        # Enrollment date
        enrolled = (
            child.enrolled_date.strftime("%b %d, %Y")
            if child.enrolled_date
            else "—"
        )

        data.append(
            [
                Paragraph(
                    student_name,
                    student_name_style,
                ),
                Paragraph(
                    str(calculate_age(child.date_of_birth)),
                    normal_style,
                ),
                Paragraph(
                    clean(gender),
                    normal_style,
                ),
                Paragraph(
                    class_name,
                    normal_style,
                ),
                Paragraph(
                    program,
                    normal_style,
                ),
                Paragraph(
                    days,
                    normal_style,
                ),
                Paragraph(
                    enrolled,
                    normal_style,
                ),
            ]
        )

    # ---------------------------------------------------------
    # STUDENT TABLE
    # ---------------------------------------------------------

    table = Table(
        data,
        colWidths=[
            1.85 * inch,   # Student
            0.55 * inch,   # Age
            0.75 * inch,   # Gender
            1.05 * inch,   # Class
            1.05 * inch,   # Program
            1.55 * inch,   # Days
            1.05 * inch,   # Enrolled
        ],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                # Header
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HEADER_BG,
                ),
                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, 0),
                    0.6,
                    BORDER,
                ),

                # Body grid
                (
                    "LINEBELOW",
                    (0, 1),
                    (-1, -1),
                    0.35,
                    GRID,
                ),

                # Vertical alignment
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                # Padding
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
            ]
        )
    )

    elements.append(table)

    # ---------------------------------------------------------
    # FOOTER
    # Matches Daily Log PDF
    # ---------------------------------------------------------

    def draw_footer(canvas, doc):

        canvas.saveState()

        # White page background
        canvas.setFillColor(PAGE_BG)

        canvas.rect(
            0,
            0,
            landscape(letter)[0],
            landscape(letter)[1],
            stroke=0,
            fill=1,
        )

        # Footer line
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.6)

        canvas.line(
            34,
            25,
            landscape(letter)[0] - 34,
            25,
        )

        # Footer text
        canvas.setFont(
            "Helvetica",
            7.5,
        )

        canvas.setFillColor(MUTED)

        canvas.drawString(
            34,
            13,
            "Thank you for being a part of our daycare family!",
        )

        canvas.drawRightString(
            landscape(letter)[0] - 34,
            13,
            f"Page {doc.page}",
        )

        canvas.restoreState()

    # ---------------------------------------------------------
    # BUILD PDF
    # ---------------------------------------------------------

    doc.build(
        elements,
        onFirstPage=draw_footer,
        onLaterPages=draw_footer,
    )

# =========================================================
# STUDENTS BY CLASS PDF
# =========================================================

def create_students_by_class_pdf(file_path, classes):

    today = date.today()

    # ---------------------------------------------------------
    # PAGE
    # ---------------------------------------------------------

    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(letter),
        rightMargin=34,
        leftMargin=34,
        topMargin=32,
        bottomMargin=38,
    )

    PAGE_WIDTH = 792 - 34 - 34

    elements = []

    # ---------------------------------------------------------
    # COLORS
    # Matches Student Directory / Daily Log
    # ---------------------------------------------------------

    PAGE_BG = colors.white
    HEADER_BG = colors.HexColor("#E2E6EA")

    TEXT = colors.HexColor("#18212B")
    MUTED = colors.HexColor("#59636E")
    BORDER = colors.HexColor("#CDD3D9")
    GRID = colors.HexColor("#DDE2E7")

    # ---------------------------------------------------------
    # STYLES
    # ---------------------------------------------------------

    styles = getSampleStyleSheet()

    brand_name_style = ParagraphStyle(
        "ClassReportBrandName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16,
        textColor=TEXT,
        alignment=TA_LEFT,
    )

    tagline_style = ParagraphStyle(
        "ClassReportTagline",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_RIGHT,
    )

    title_style = ParagraphStyle(
        "ClassReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=21,
        alignment=TA_CENTER,
        textColor=TEXT,
        spaceBefore=0,
        spaceAfter=3,
    )

    subtitle_style = ParagraphStyle(
        "ClassReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=MUTED,
        spaceBefore=0,
        spaceAfter=0,
    )

    class_header_style = ParagraphStyle(
        "ClassReportClassHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        textColor=TEXT,
    )

    table_header_style = ParagraphStyle(
        "ClassReportTableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=8.2,
        textColor=TEXT,
    )

    normal_style = ParagraphStyle(
        "ClassReportNormal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=8.8,
        textColor=TEXT,
        splitLongWords=True,
    )

    student_name_style = ParagraphStyle(
        "ClassReportStudentName",
        parent=normal_style,
        fontName="Helvetica-Bold",
    )

    summary_style = ParagraphStyle(
        "ClassReportSummary",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9,
        textColor=MUTED,
        alignment=TA_RIGHT,
    )

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------

    def clean(value):

        if value is None or str(value).strip() == "":
            return "--"

        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    def calculate_age(dob):

        if not dob:
            return "—"

        return (
            today.year
            - dob.year
            - (
                (today.month, today.day)
                < (dob.month, dob.day)
            )
        )

    # ---------------------------------------------------------
    # BRAND HEADER
    # ---------------------------------------------------------

    elements.append(Spacer(1, 2))

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
        colWidths=[
            PAGE_WIDTH * 0.62,
            PAGE_WIDTH * 0.38,
        ],
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

    # ---------------------------------------------------------
    # TITLE BLOCK
    # ---------------------------------------------------------

    title_block = Table(
        [
            [
                Paragraph(
                    "Students by Class",
                    title_style,
                )
            ],
            [
                Paragraph(
                    (
                        "Students grouped by classroom"
                        "<br/>"
                        f"Generated {today.strftime('%B %d, %Y')}"
                    ),
                    subtitle_style,
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

                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),

                ("TOPPADDING", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 3),

                ("TOPPADDING", (0, 1), (-1, 1), 0),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
            ]
        )
    )

    elements.append(title_block)

    elements.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    summary_table = Table(
        [
            [
                Paragraph(
                    "CLASSROOMS",
                    table_header_style,
                ),
                Paragraph(
                    f"{len(classes)} "
                    f"{'class' if len(classes) == 1 else 'classes'}"
                    f"  •  "
                    f"{sum(len(group) for group in classes.values())} "
                    f"students",
                    summary_style,
                ),
            ]
        ],
        colWidths=[
            PAGE_WIDTH * 0.60,
            PAGE_WIDTH * 0.40,
        ],
    )

    summary_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LINEBELOW", (0, 0), (-1, -1), 0.6, BORDER),

                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(summary_table)

    elements.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # CLASS SECTIONS
    # ---------------------------------------------------------

    for class_name, students in classes.items():

        # Class heading
        class_title = Table(
            [
                [
                    Paragraph(
                        clean(class_name),
                        class_header_style,
                    ),
                    Paragraph(
                        f"{len(students)} "
                        f"{'student' if len(students) == 1 else 'students'}",
                        summary_style,
                    ),
                ]
            ],
            colWidths=[
                PAGE_WIDTH * 0.60,
                PAGE_WIDTH * 0.40,
            ],
        )

        class_title.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), HEADER_BG),
                    ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        elements.append(class_title)

        elements.append(Spacer(1, 4))

        # Student table
        data = [
            [
                Paragraph("Student", table_header_style),
                Paragraph("Age", table_header_style),
                Paragraph("Gender", table_header_style),
                Paragraph("Program", table_header_style),
                Paragraph("Days Attending", table_header_style),
                Paragraph("Enrolled", table_header_style),
            ]
        ]

        for child in students:

            student_name = (
                f"{clean(child.first_name)} "
                f"{clean(child.last_name)}"
            )

            gender = (
                child.gender.title()
                if child.gender
                else "—"
            )

            program = (
                clean(child.program_type)
                if child.program_type
                else "—"
            )

            days = (
                clean(child.days_attending)
                if child.days_attending
                else "—"
            )

            enrolled = (
                child.enrolled_date.strftime("%b %d, %Y")
                if child.enrolled_date
                else "—"
            )

            data.append(
                [
                    Paragraph(
                        student_name,
                        student_name_style,
                    ),
                    Paragraph(
                        str(calculate_age(child.date_of_birth)),
                        normal_style,
                    ),
                    Paragraph(
                        clean(gender),
                        normal_style,
                    ),
                    Paragraph(
                        program,
                        normal_style,
                    ),
                    Paragraph(
                        days,
                        normal_style,
                    ),
                    Paragraph(
                        enrolled,
                        normal_style,
                    ),
                ]
            )

        student_table = Table(
            data,
            colWidths=[
                2.35 * inch,
                0.60 * inch,
                0.85 * inch,
                1.25 * inch,
                1.70 * inch,
                1.15 * inch,
            ],
            repeatRows=1,
        )

        student_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                    ("LINEBELOW", (0, 0), (-1, 0), 0.6, BORDER),

                    ("LINEBELOW", (0, 1), (-1, -1), 0.35, GRID),

                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        elements.append(student_table)

        elements.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # EMPTY STATE
    # ---------------------------------------------------------

    if not classes:

        empty_table = Table(
            [
                [
                    Paragraph(
                        "No students are currently registered.",
                        normal_style,
                    )
                ]
            ],
            colWidths=[PAGE_WIDTH],
        )

        empty_table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        elements.append(empty_table)

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------

    def draw_footer(canvas, doc):

        canvas.saveState()

        canvas.setFillColor(PAGE_BG)

        canvas.rect(
            0,
            0,
            landscape(letter)[0],
            landscape(letter)[1],
            stroke=0,
            fill=1,
        )

        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.6)

        canvas.line(
            34,
            25,
            landscape(letter)[0] - 34,
            25,
        )

        canvas.setFont(
            "Helvetica",
            7.5,
        )

        canvas.setFillColor(MUTED)

        canvas.drawString(
            34,
            13,
            "Thank you for being a part of our daycare family!",
        )

        canvas.drawRightString(
            landscape(letter)[0] - 34,
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
# ENROLLMENT SUMMARY PDF
# =========================================================

def create_enrollment_summary_pdf(
    file_path,
    total_students,
    male_count,
    female_count,
    class_counts,
    program_counts,
    enrollment_years
):
    
    # -----------------------------------------
    # Page setup
    # -----------------------------------------

    PAGE_WIDTH, PAGE_HEIGHT = landscape(letter)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(letter),
        rightMargin=38,
        leftMargin=38,
        topMargin=34,
        bottomMargin=38
    )

    # -----------------------------------------
    # Colors
    # -----------------------------------------

    HEADER_BG = colors.HexColor("#E2E6EA")
    TEXT = colors.HexColor("#18212B")
    MUTED = colors.HexColor("#59636E")
    BORDER = colors.HexColor("#CDD3D9")
    GRID = colors.HexColor("#DDE2E7")
    WHITE = colors.white

    # -----------------------------------------
    # Styles
    # -----------------------------------------

    styles = getSampleStyleSheet()

    brand_style = ParagraphStyle(
        "Brand",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        textColor=TEXT,
        alignment=TA_LEFT,
        spaceAfter=2
    )

    brand_subtitle_style = ParagraphStyle(
        "BrandSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=MUTED,
        alignment=TA_LEFT
    )

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=TEXT,
        alignment=TA_CENTER,
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=MUTED,
        alignment=TA_CENTER
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=TEXT,
        alignment=TA_LEFT
    )

    section_count_style = ParagraphStyle(
        "SectionCount",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_LEFT
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9,
        textColor=TEXT,
        alignment=TA_LEFT
    )

    table_text_style = ParagraphStyle(
        "TableText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=TEXT,
        alignment=TA_LEFT
    )

    table_number_style = ParagraphStyle(
        "TableNumber",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=TEXT,
        alignment=TA_LEFT
    )

    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9,
        textColor=MUTED,
        alignment=TA_LEFT
    )

    # -----------------------------------------
    # Story
    # -----------------------------------------

    story = []

    # -----------------------------------------
    # Branding
    # -----------------------------------------

    branding = Table(
        [
            [
                Paragraph("LITTLE ONES TOO", brand_style),
                Paragraph("D A Y C A R E", brand_subtitle_style)
            ]
        ],
        colWidths=[3.0 * inch, 2.0 * inch]
    )

    branding.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    story.append(branding)
    story.append(Spacer(1, 18))

    # -----------------------------------------
    # Title
    # -----------------------------------------

    story.append(
        Paragraph(
            "Enrollment Summary",
            title_style
        )
    )

    story.append(
        Paragraph(
            "A summary of student enrollment across Little Ones",
            subtitle_style
        )
    )

    story.append(Spacer(1, 7))

    story.append(
        Paragraph(
            f"Generated {date.today().strftime('%B %d, %Y')}",
            subtitle_style
        )
    )

    story.append(Spacer(1, 18))

    # -----------------------------------------
    # Overall Summary
    # -----------------------------------------

    classroom_count = len(class_counts)

    summary_data = [
        [
            Paragraph("TOTAL STUDENTS", table_header_style),
            Paragraph("CLASSROOMS", table_header_style),
            Paragraph("FEMALE", table_header_style),
            Paragraph("MALE", table_header_style),
        ],
        [
            Paragraph(str(total_students), table_number_style),
            Paragraph(str(classroom_count), table_number_style),
            Paragraph(str(female_count), table_number_style),
            Paragraph(str(male_count), table_number_style),
        ]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            1.75 * inch,
            1.75 * inch,
            1.75 * inch,
            1.75 * inch
        ]
    )

    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("BACKGROUND", (0, 1), (-1, 1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, GRID),

                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, 0), 7),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
                ("TOPPADDING", (0, 1), (-1, 1), 9),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
            ]
        )
    )

    story.append(summary_table)
    story.append(Spacer(1, 20))

    # -----------------------------------------
    # Class + Program Summary
    # -----------------------------------------

    class_rows = [
        [
            Paragraph("Classroom", table_header_style),
            Paragraph("Students", table_header_style)
        ]
    ]

    for class_name, count in class_counts.items():

        class_rows.append(
            [
                Paragraph(str(class_name), table_text_style),
                Paragraph(str(count), table_number_style)
            ]
        )

    if not class_counts:
        class_rows.append(
            [
                Paragraph("No class data available", table_text_style),
                Paragraph("—", table_text_style)
            ]
        )

    class_table = Table(
        class_rows,
        colWidths=[3.0 * inch, 1.0 * inch],
        repeatRows=1
    )

    class_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, GRID),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    program_rows = [
        [
            Paragraph("Program", table_header_style),
            Paragraph("Students", table_header_style)
        ]
    ]

    for program, count in program_counts.items():

        program_rows.append(
            [
                Paragraph(str(program), table_text_style),
                Paragraph(str(count), table_number_style)
            ]
        )

    if not program_counts:
        program_rows.append(
            [
                Paragraph("No program data available", table_text_style),
                Paragraph("—", table_text_style)
            ]
        )

    program_table = Table(
        program_rows,
        colWidths=[3.0 * inch, 1.0 * inch],
        repeatRows=1
    )

    program_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, GRID),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    section_tables = Table(
        [
            [
                [
                    Paragraph(
                        "Students by Class",
                        section_style
                    ),
                    Spacer(1, 4),
                    class_table
                ],
                [
                    Paragraph(
                        "Students by Program",
                        section_style
                    ),
                    Spacer(1, 4),
                    program_table
                ]
            ]
        ],
        colWidths=[4.0 * inch, 4.0 * inch]
    )

    section_tables.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    story.append(section_tables)
    story.append(Spacer(1, 20))

    # -----------------------------------------
    # Enrollment History
    # -----------------------------------------

    story.append(
        Paragraph(
            "Enrollment History",
            section_style
        )
    )

    story.append(
        Paragraph(
            "Students grouped by enrollment year",
            section_count_style
        )
    )

    story.append(Spacer(1, 7))

    history_rows = [
        [
            Paragraph("Enrollment Year", table_header_style),
            Paragraph("Students Enrolled", table_header_style)
        ]
    ]

    for year, count in enrollment_years.items():

        student_label = (
            "student"
            if count == 1
            else "students"
        )

        history_rows.append(
            [
                Paragraph(str(year), table_number_style),
                Paragraph(
                    f"{count} {student_label}",
                    table_text_style
                )
            ]
        )

    if not enrollment_years:

        history_rows.append(
            [
                Paragraph(
                    "No enrollment history available",
                    table_text_style
                ),
                Paragraph("—", table_text_style)
            ]
        )

    history_table = Table(
        history_rows,
        colWidths=[2.0 * inch, 2.0 * inch],
        repeatRows=1
    )

    history_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, GRID),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(history_table)

    # -----------------------------------------
    # Footer
    # -----------------------------------------

    def draw_footer(canvas, doc):

        canvas.saveState()

        width, height = landscape(letter)

        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.6)

        canvas.line(
            38,
            27,
            width - 38,
            27
        )

        canvas.setFont(
            "Helvetica",
            7.5
        )

        canvas.setFillColor(MUTED)

        canvas.drawString(
            38,
            15,
            "Thank you for being a part of our daycare family!"
        )

        page_text = f"Page {doc.page}"

        canvas.drawRightString(
            width - 38,
            15,
            page_text
        )

        canvas.restoreState()

    # -----------------------------------------
    # Build PDF
    # -----------------------------------------

    doc.build(
        story,
        onFirstPage=draw_footer,
        onLaterPages=draw_footer
    )

# =========================================================
# ENROLLMENT SUMMARY PDF
# =========================================================

def create_daily_log_report_pdf(
        file_path,
        children,
        daily_logs,
        selected_date
):
    
# -----------------------------------------
    # Page setup
    # -----------------------------------------

    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(letter),
        rightMargin=34,
        leftMargin=34,
        topMargin=34,
        bottomMargin=38
    )

    # -----------------------------------------
    # Colors
    # -----------------------------------------

    HEADER_BG = colors.HexColor("#E2E6EA")
    SECTION_BG = colors.HexColor("#F1F3F5")
    TEXT = colors.HexColor("#18212B")
    MUTED = colors.HexColor("#59636E")
    BORDER = colors.HexColor("#CDD3D9")
    GRID = colors.HexColor("#DDE2E7")
    WHITE = colors.white

    # -----------------------------------------
    # Styles
    # -----------------------------------------

    styles = getSampleStyleSheet()

    brand_style = ParagraphStyle(
        "DailyBrand",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        textColor=TEXT,
        alignment=TA_LEFT
    )

    brand_subtitle_style = ParagraphStyle(
        "DailyBrandSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=MUTED,
        alignment=TA_LEFT
    )

    title_style = ParagraphStyle(
        "DailyTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=23,
        textColor=TEXT,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        "DailySubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=MUTED,
        alignment=TA_CENTER
    )

    child_style = ParagraphStyle(
        "DailyChild",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=TEXT,
        alignment=TA_LEFT
    )

    child_class_style = ParagraphStyle(
        "DailyChildClass",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_LEFT
    )

    section_style = ParagraphStyle(
        "DailySection",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=TEXT,
        alignment=TA_LEFT
    )

    table_header_style = ParagraphStyle(
        "DailyTableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=9,
        textColor=TEXT,
        alignment=TA_LEFT
    )

    table_text_style = ParagraphStyle(
        "DailyTableText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=TEXT,
        alignment=TA_LEFT
    )

    empty_style = ParagraphStyle(
        "DailyEmpty",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=MUTED,
        alignment=TA_LEFT
    )

    # -----------------------------------------
    # Helpers
    # -----------------------------------------

    def display_time(value):

        if value is None:
            return "—"

        if hasattr(value, "strftime"):

            try:
                return value.strftime(
                    "%I:%M %p"
                ).lstrip("0")
            except Exception:
                pass

        return str(value)

    def display_value(value):

        if value is None:
            return "—"

        if isinstance(value, str):

            value = value.strip()

            if not value:
                return "—"

        return str(value)

    def make_table(
        headers,
        rows,
        widths
    ):

        data = [
            [
                Paragraph(
                    str(header),
                    table_header_style
                )
                for header in headers
            ]
        ]

        for row in rows:

            data.append(
                [
                    Paragraph(
                        display_value(value),
                        table_text_style
                    )
                    for value in row
                ]
            )

        table = Table(
            data,
            colWidths=widths,
            repeatRows=1
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HEADER_BG
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.6,
                        BORDER
                    ),
                    (
                        "INNERGRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        GRID
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE"
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                ]
            )
        )

        return table

    # -----------------------------------------
    # Story
    # -----------------------------------------

    story = []

    # -----------------------------------------
    # Branding
    # -----------------------------------------

    branding = Table(
        [
            [
                Paragraph(
                    "LITTLE ONES TOO",
                    brand_style
                ),
                Paragraph(
                    "D A Y C A R E",
                    brand_subtitle_style
                )
            ]
        ],
        colWidths=[
            3.0 * 72,
            2.0 * 72
        ]
    )

    branding.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),
            ]
        )
    )

    story.append(branding)
    story.append(Spacer(1, 16))

    # -----------------------------------------
    # Report title
    # -----------------------------------------

    story.append(
        Paragraph(
            "Daily Log Report",
            title_style
        )
    )

    story.append(
        Paragraph(
            selected_date.strftime("%B %d, %Y"),
            subtitle_style
        )
    )

    story.append(Spacer(1, 18))

    # -----------------------------------------
    # Student count
    # -----------------------------------------

    story.append(
        Paragraph(
            f"<b>{len(children)}</b> students",
            subtitle_style
        )
    )

    story.append(Spacer(1, 16))

    # -----------------------------------------
    # Student reports
    # -----------------------------------------

    if not children:

        story.append(
            Spacer(1, 30)
        )

        story.append(
            Paragraph(
                "No students are currently registered.",
                empty_style
            )
        )

    else:

        for index, child in enumerate(children):

            daily_log = daily_logs.get(
                child.id
            )

            # ---------------------------------
            # Child heading
            # ---------------------------------

            child_name = (
                f"{child.first_name} "
                f"{child.last_name}"
            )

            child_class = (
                child.class_name
                if child.class_name
                else "Unassigned"
            )

            child_header = Table(
                [
                    [
                        Paragraph(
                            child_name,
                            child_style
                        ),
                        Paragraph(
                            child_class,
                            child_class_style
                        )
                    ]
                ],
                colWidths=[
                    5.5 * 72,
                    2.5 * 72
                ]
            )

            child_header.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, -1),
                            SECTION_BG
                        ),
                        (
                            "BOX",
                            (0, 0),
                            (-1, -1),
                            0.6,
                            BORDER
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE"
                        ),
                        (
                            "ALIGN",
                            (1, 0),
                            (1, 0),
                            "RIGHT"
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            9
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            9
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            7
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            7
                        ),
                    ]
                )
            )

            story.append(
                child_header
            )

            story.append(
                Spacer(1, 8)
            )

            # ---------------------------------
            # No daily log
            # ---------------------------------

            if not daily_log:

                story.append(
                    Paragraph(
                        "No daily log recorded for this date.",
                        empty_style
                    )
                )

                story.append(
                    Spacer(1, 12)
                )

                continue

            # ---------------------------------
            # Health Check
            # ---------------------------------

            if daily_log.health_check:

                health = daily_log.health_check

                story.append(
                    Paragraph(
                        "Health Check",
                        section_style
                    )
                )

                health_rows = [
                    [
                        display_value(
                            health.temperature
                        ) + (
                            " °F"
                            if health.temperature
                            else ""
                        ),
                        display_value(
                            health.symptoms
                        ),
                        display_value(
                            health.notes
                        )
                    ]
                ]

                story.append(
                    make_table(
                        [
                            "Temperature",
                            "Symptoms",
                            "Notes"
                        ],
                        health_rows,
                        [
                            1.4 * 72,
                            2.4 * 72,
                            4.2 * 72
                        ]
                    )
                )

                story.append(
                    Spacer(1, 9)
                )

            # ---------------------------------
            # Bottle Logs
            # ---------------------------------

            if daily_log.bottle_logs:

                story.append(
                    Paragraph(
                        "Bottles",
                        section_style
                    )
                )

                rows = []

                for bottle in daily_log.bottle_logs:

                    amount = (
                        f"{bottle.amount_offered} oz"
                        if bottle.amount_offered
                        is not None
                        else "—"
                    )

                    rows.append(
                        [
                            display_time(
                                bottle.time
                            ),
                            display_value(
                                bottle.bottle_type
                            ),
                            amount,
                            display_value(
                                bottle.notes
                            )
                        ]
                    )

                story.append(
                    make_table(
                        [
                            "Time",
                            "Bottle",
                            "Amount",
                            "Notes"
                        ],
                        rows,
                        [
                            1.0 * 72,
                            1.8 * 72,
                            1.0 * 72,
                            4.2 * 72
                        ]
                    )
                )

                story.append(
                    Spacer(1, 9)
                )

            # ---------------------------------
            # Meal Logs
            # ---------------------------------

            if daily_log.meal_logs:

                story.append(
                    Paragraph(
                        "Meals",
                        section_style
                    )
                )

                rows = []

                for meal in daily_log.meal_logs:

                    rows.append(
                        [
                            display_time(
                                meal.time
                            ),
                            display_value(
                                meal.meal_type
                            ),
                            display_value(
                                meal.food
                            ),
                            display_value(
                                meal.amount
                            ),
                            display_value(
                                meal.notes
                            )
                        ]
                    )

                story.append(
                    make_table(
                        [
                            "Time",
                            "Meal",
                            "Food",
                            "Amount",
                            "Notes"
                        ],
                        rows,
                        [
                            0.9 * 72,
                            1.1 * 72,
                            2.6 * 72,
                            1.0 * 72,
                            2.4 * 72
                        ]
                    )
                )

                story.append(
                    Spacer(1, 9)
                )

            # ---------------------------------
            # Diaper Logs
            # ---------------------------------

            if daily_log.diaper_logs:

                story.append(
                    Paragraph(
                        "Diaper",
                        section_style
                    )
                )

                rows = []

                for diaper in daily_log.diaper_logs:

                    rows.append(
                        [
                            display_time(
                                diaper.time
                            ),
                            display_value(
                                diaper.diaper_type
                            ),
                            display_value(
                                diaper.diaper_desc
                            ),
                            display_value(
                                diaper.notes
                            )
                        ]
                    )

                story.append(
                    make_table(
                        [
                            "Time",
                            "Type",
                            "Description",
                            "Notes"
                        ],
                        rows,
                        [
                            1.0 * 72,
                            1.5 * 72,
                            3.0 * 72,
                            2.5 * 72
                        ]
                    )
                )

                story.append(
                    Spacer(1, 9)
                )

            # ---------------------------------
            # Potty Logs
            # ---------------------------------

            if daily_log.potty_logs:

                story.append(
                    Paragraph(
                        "Potty",
                        section_style
                    )
                )

                rows = []

                for potty in daily_log.potty_logs:

                    rows.append(
                        [
                            display_time(
                                potty.time
                            ),
                            display_value(
                                potty.potty_status
                            ),
                            display_value(
                                potty.potty_method
                            ),
                            display_value(
                                potty.potty_progress
                            ),
                            display_value(
                                potty.notes
                            )
                        ]
                    )

                story.append(
                    make_table(
                        [
                            "Time",
                            "Status",
                            "Method",
                            "Progress",
                            "Notes"
                        ],
                        rows,
                        [
                            0.9 * 72,
                            1.1 * 72,
                            1.5 * 72,
                            2.2 * 72,
                            2.3 * 72
                        ]
                    )
                )

                story.append(
                    Spacer(1, 9)
                )

            # ---------------------------------
            # Nap Logs
            # ---------------------------------

            if daily_log.nap_logs:

                story.append(
                    Paragraph(
                        "Nap",
                        section_style
                    )
                )

                rows = []

                for nap in daily_log.nap_logs:

                    rows.append(
                        [
                            display_time(
                                nap.start_time
                            ),
                            display_time(
                                nap.end_time
                            ),
                            display_value(
                                nap.notes
                            )
                        ]
                    )

                story.append(
                    make_table(
                        [
                            "Start Time",
                            "End Time",
                            "Notes"
                        ],
                        rows,
                        [
                            1.5 * 72,
                            1.5 * 72,
                            5.0 * 72
                        ]
                    )
                )

                story.append(
                    Spacer(1, 9)
                )

            # ---------------------------------
            # Activity Logs
            # ---------------------------------

            if daily_log.activity_logs:

                story.append(
                    Paragraph(
                        "Activities",
                        section_style
                    )
                )

                rows = []

                for activity in daily_log.activity_logs:

                    rows.append(
                        [
                            display_time(
                                activity.time
                            ),
                            display_value(
                                activity.activity
                            ),
                            display_value(
                                activity.notes
                            )
                        ]
                    )

                story.append(
                    make_table(
                        [
                            "Time",
                            "Activity",
                            "Notes"
                        ],
                        rows,
                        [
                            1.2 * 72,
                            2.6 * 72,
                            4.2 * 72
                        ]
                    )
                )

                story.append(
                    Spacer(1, 9)
                )

            # ---------------------------------
            # If daily log exists but no entries
            # ---------------------------------

            has_entries = (
                bool(daily_log.health_check)
                or bool(daily_log.bottle_logs)
                or bool(daily_log.meal_logs)
                or bool(daily_log.diaper_logs)
                or bool(daily_log.potty_logs)
                or bool(daily_log.nap_logs)
                or bool(daily_log.activity_logs)
            )

            if not has_entries:

                story.append(
                    Paragraph(
                        "No activities or care entries recorded for this date.",
                        empty_style
                    )
                )

                story.append(
                    Spacer(1, 9)
                )

            # ---------------------------------
            # Separate students
            # ---------------------------------

            if index < len(children) - 1:

                story.append(
                    Spacer(1, 8)
                )

    # -----------------------------------------
    # Footer
    # -----------------------------------------

    def draw_footer(canvas, doc):

        canvas.saveState()

        width, height = landscape(letter)

        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.6)

        canvas.line(
            34,
            27,
            width - 34,
            27
        )

        canvas.setFont(
            "Helvetica",
            7.5
        )

        canvas.setFillColor(MUTED)

        canvas.drawString(
            34,
            15,
            "Thank you for being a part of our daycare family!"
        )

        canvas.drawRightString(
            width - 34,
            15,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    # -----------------------------------------
    # Build
    # -----------------------------------------

    doc.build(
        story,
        onFirstPage=draw_footer,
        onLaterPages=draw_footer
    )

# =========================================================
# BIRTHDAY PDF
# =========================================================

def create_birthday_report_pdf (
        file_path,
        children,
        selected_month,
        month_name
):
    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'BirthdayTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#18212B'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'BirthdaySubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#59636E'),
        spaceAfter=18
    )

    table_header_style = ParagraphStyle(
        'BirthdayTableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.HexColor('#18212B')
    )

    table_text_style = ParagraphStyle(
        'BirthdayTableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#18212B')
    )

    story = []

    # -----------------------------
    # Header
    # -----------------------------

    story.append(
        Paragraph(
            'LITTLE ONES TOO',
            ParagraphStyle(
                'Brand',
                parent=styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=9,
                textColor=colors.HexColor('#59636E'),
                spaceAfter=5
            )
        )
    )

    story.append(
        Paragraph(
            'Birthday Report',
            title_style
        )
    )

    story.append(
        Paragraph(
            f'{month_name} Birthdays',
            subtitle_style
        )
    )

    # -----------------------------
    # Birthday table
    # -----------------------------

    data = [
        [
            Paragraph('Date', table_header_style),
            Paragraph('Child Name', table_header_style),
            Paragraph('Age', table_header_style),
            Paragraph('Class', table_header_style)
        ]
    ]

    for child in children:

        if not child.date_of_birth:
            continue

        birthday_this_year = child.date_of_birth.replace(
            year=date.today().year
        )

        age = date.today().year - child.date_of_birth.year

        # If birthday has not happened yet this year
        if birthday_this_year > date.today():
            age -= 1

        birthday_date = child.date_of_birth.strftime(
            '%B %d'
        )

        child_name = (
            f'{child.first_name} {child.last_name}'
        )

        class_name = child.class_name or 'Unassigned'

        data.append(
            [
                Paragraph(
                    birthday_date,
                    table_text_style
                ),
                Paragraph(
                    child_name,
                    table_text_style
                ),
                Paragraph(
                    str(age),
                    table_text_style
                ),
                Paragraph(
                    class_name,
                    table_text_style
                )
            ]
        )

    # No birthdays
    if len(data) == 1:

        data.append(
            [
                Paragraph(
                    'No birthdays this month.',
                    table_text_style
                ),
                '',
                '',
                ''
            ]
        )

    table = Table(
        data,
        colWidths=[
            1.25 * inch,
            2.65 * inch,
            0.75 * inch,
            1.75 * inch
        ],
        repeatRows=1
    )

    table.setStyle(
        TableStyle(
            [
                (
                    'BACKGROUND',
                    (0, 0),
                    (-1, 0),
                    colors.HexColor('#E2E6EA')
                ),
                (
                    'TEXTCOLOR',
                    (0, 0),
                    (-1, 0),
                    colors.HexColor('#18212B')
                ),
                (
                    'GRID',
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor('#DDE2E7')
                ),
                (
                    'VALIGN',
                    (0, 0),
                    (-1, -1),
                    'MIDDLE'
                ),
                (
                    'LEFTPADDING',
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    'RIGHTPADDING',
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    'TOPPADDING',
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    'BOTTOMPADDING',
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            'Thank you for being a part of our daycare family!',
            ParagraphStyle(
                'FooterText',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=8,
                textColor=colors.HexColor('#59636E'),
                alignment=TA_CENTER
            )
        )
    )

    doc.build(story)

# =========================================================
# PARENT CONTACT / AUTHORIZED PICKUP PDF
# =========================================================

def create_parent_contact_report_pdf(
        file_path,
        children
):
    
    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'ParentContactTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#18212B'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'ParentContactSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#59636E'),
        spaceAfter=18
    )

    section_style = ParagraphStyle(
        'ParentContactSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#18212B'),
        spaceBefore=10,
        spaceAfter=7
    )

    table_header_style = ParagraphStyle(
        'ParentContactHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        textColor=colors.HexColor('#18212B')
    )

    table_text_style = ParagraphStyle(
        'ParentContactText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#18212B')
    )

    child_style = ParagraphStyle(
        'ParentContactChild',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#18212B'),
        spaceAfter=2
    )

    class_style = ParagraphStyle(
        'ParentContactClass',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        textColor=colors.HexColor('#59636E'),
        spaceAfter=8
    )

    story = []

    # -----------------------------
    # Report Header
    # -----------------------------

    story.append(
        Paragraph(
            'LITTLE ONES TOO',
            ParagraphStyle(
                'Brand',
                parent=styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=9,
                textColor=colors.HexColor('#59636E'),
                spaceAfter=5
            )
        )
    )

    story.append(
        Paragraph(
            'Parent & Authorized Pickup Directory',
            title_style
        )
    )

    story.append(
        Paragraph(
            f'Contact information for {len(children)} students',
            subtitle_style
        )
    )

    # -----------------------------
    # Child Sections
    # -----------------------------

    for index, child in enumerate(children):

        child_name = (
            f'{child.first_name} {child.last_name}'
        )

        class_name = (
            child.class_name
            or 'Unassigned'
        )

        story.append(
            Paragraph(
                child_name,
                child_style
            )
        )

        story.append(
            Paragraph(
                f'Class: {class_name}',
                class_style
            )
        )

        # -------------------------
        # Parents
        # -------------------------

        story.append(
            Paragraph(
                'Parents / Guardians',
                section_style
            )
        )

        parent_data = [
            [
                Paragraph('Role', table_header_style),
                Paragraph('Name', table_header_style),
                Paragraph('Phone', table_header_style),
                Paragraph('Email', table_header_style),
                Paragraph('Occupation', table_header_style)
            ]
        ]

        if child.parents:

            for parent in child.parents:

                parent_data.append(
                    [
                        Paragraph(
                            parent.role or '—',
                            table_text_style
                        ),
                        Paragraph(
                            parent.full_name or '—',
                            table_text_style
                        ),
                        Paragraph(
                            parent.phone_number or '—',
                            table_text_style
                        ),
                        Paragraph(
                            parent.email or '—',
                            table_text_style
                        ),
                        Paragraph(
                            parent.occupation or '—',
                            table_text_style
                        )
                    ]
                )

        else:

            parent_data.append(
                [
                    Paragraph(
                        'No parent information available.',
                        table_text_style
                    ),
                    '',
                    '',
                    '',
                    ''
                ]
            )

        parent_table = Table(
            parent_data,
            colWidths=[
                0.75 * inch,
                1.45 * inch,
                1.15 * inch,
                2.15 * inch,
                1.20 * inch
            ],
            repeatRows=1
        )

        parent_table.setStyle(
            TableStyle(
                [
                    (
                        'BACKGROUND',
                        (0, 0),
                        (-1, 0),
                        colors.HexColor('#E2E6EA')
                    ),
                    (
                        'GRID',
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor('#DDE2E7')
                    ),
                    (
                        'VALIGN',
                        (0, 0),
                        (-1, -1),
                        'MIDDLE'
                    ),
                    (
                        'LEFTPADDING',
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        'RIGHTPADDING',
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        'TOPPADDING',
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        'BOTTOMPADDING',
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ]
            )
        )

        story.append(parent_table)

        # -------------------------
        # Authorized Pickup
        # -------------------------

        story.append(
            Paragraph(
                'Authorized Pickup',
                section_style
            )
        )

        pickup_data = [
            [
                Paragraph('Name', table_header_style),
                Paragraph('Relationship', table_header_style),
                Paragraph('Phone', table_header_style)
            ]
        ]

        if child.pickups:

            for pickup in child.pickups:

                pickup_data.append(
                    [
                        Paragraph(
                            pickup.full_name or '—',
                            table_text_style
                        ),
                        Paragraph(
                            pickup.relationship or '—',
                            table_text_style
                        ),
                        Paragraph(
                            pickup.phone or '—',
                            table_text_style
                        )
                    ]
                )

        else:

            pickup_data.append(
                [
                    Paragraph(
                        'No authorized pickup information available.',
                        table_text_style
                    ),
                    '',
                    ''
                ]
            )

        pickup_table = Table(
            pickup_data,
            colWidths=[
                2.70 * inch,
                2.00 * inch,
                2.00 * inch
            ],
            repeatRows=1
        )

        pickup_table.setStyle(
            TableStyle(
                [
                    (
                        'BACKGROUND',
                        (0, 0),
                        (-1, 0),
                        colors.HexColor('#E2E6EA')
                    ),
                    (
                        'GRID',
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor('#DDE2E7')
                    ),
                    (
                        'VALIGN',
                        (0, 0),
                        (-1, -1),
                        'MIDDLE'
                    ),
                    (
                        'LEFTPADDING',
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        'RIGHTPADDING',
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        'TOPPADDING',
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        'BOTTOMPADDING',
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ]
            )
        )

        story.append(pickup_table)

        # Separator between children
        if index < len(children) - 1:
            story.append(
                Spacer(1, 18)
            )

    # -----------------------------
    # Empty state
    # -----------------------------

    if not children:

        story.append(
            Paragraph(
                'No students are currently registered.',
                table_text_style
            )
        )

    # -----------------------------
    # Footer
    # -----------------------------

    story.append(
        Spacer(1, 24)
    )

    story.append(
        Paragraph(
            'Thank you for being a part of our daycare family!',
            ParagraphStyle(
                'FooterText',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=8,
                textColor=colors.HexColor('#59636E'),
                alignment=TA_CENTER
            )
        )
    )

    doc.build(story)


# =========================================================
# CHILD PROFILE PDF
# =========================================================

def create_child_profile_pdf(file_path, child):

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # ---------------------------------------------------------
    # COLORS
    # ---------------------------------------------------------

    TEXT = colors.HexColor("#18212B")
    MUTED = colors.HexColor("#59636E")
    BORDER = colors.HexColor("#CDD3D9")
    GRID = colors.HexColor("#DDE2E7")
    HEADER_BG = colors.HexColor("#E2E6EA")

    # ---------------------------------------------------------
    # STYLES
    # ---------------------------------------------------------

    brand_style = ParagraphStyle(
        "ChildProfileBrand",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16,
        textColor=TEXT
    )

    tagline_style = ParagraphStyle(
        "ChildProfileTagline",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_RIGHT
    )

    title_style = ParagraphStyle(
        "ChildProfileTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=TEXT,
        alignment=TA_CENTER,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        "ChildProfileSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=MUTED,
        alignment=TA_CENTER
    )

    section_style = ParagraphStyle(
        "ChildProfileSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=TEXT,
        spaceBefore=4,
        spaceAfter=7
    )

    label_style = ParagraphStyle(
        "ChildProfileLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9,
        textColor=MUTED
    )

    value_style = ParagraphStyle(
        "ChildProfileValue",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=TEXT
    )

    name_style = ParagraphStyle(
        "ChildProfileName",
        parent=value_style,
        fontName="Helvetica-Bold",
        fontSize=10
    )

    empty_style = ParagraphStyle(
        "ChildProfileEmpty",
        parent=value_style,
        textColor=MUTED
    )

    story = []

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------

    def clean(value):
        if value is None or str(value).strip() == "":
            return "--"

        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    def display_date(value):
        if not value:
            return "--"

        return value.strftime("%B %d, %Y")

    def calculate_age(dob):
        if not dob:
            return "--"

        today = date.today()

        years = today.year - dob.year

        if (today.month, today.day) < (
            dob.month,
            dob.day
        ):
            years -= 1

        return f"{years} year{'s' if years != 1 else ''} old"

    def display_phone(phone):
        if not phone:
            return "--"

        phone = str(phone)

        if len(phone) == 10:
            return (
                f"({phone[:3]}) "
                f"{phone[3:6]}-"
                f"{phone[6:]}"
            )

        return phone

    def make_info_table(items, columns=2):

        rows = []

        for index in range(0, len(items), columns):

            row = []

            group = items[index:index + columns]

            for label, value in group:

                row.append(
                    Paragraph(
                        clean(label),
                        label_style
                    )
                )

                row.append(
                    Paragraph(
                        clean(value),
                        value_style
                    )
                )

            while len(group) < columns:
                row.extend(["", ""])
                group.append(("", ""))

            rows.append(row)

        table = Table(
            rows,
            colWidths=[
                0.85 * inch,
                2.35 * inch
            ] * columns
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "LINEBELOW",
                        (0, 0),
                        (-1, -1),
                        0.35,
                        GRID
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ]
            )
        )

        return table

    # ---------------------------------------------------------
    # BRAND HEADER
    # ---------------------------------------------------------

    brand_table = Table(
        [
            [
                Paragraph(
                    "<b>LITTLE ONES TOO</b><br/>"
                    "<font size='8'>D A Y C A R E</font>",
                    brand_style
                ),
                Paragraph(
                    "Little Steps. Big Futures.",
                    tagline_style
                )
            ]
        ],
        colWidths=[
            0.62 * 7.0 * inch,
            0.38 * 7.0 * inch
        ]
    )

    brand_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0)
            ]
        )
    )

    story.append(brand_table)
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    title_table = Table(
        [
            [
                Paragraph(
                    "Child Profile",
                    title_style
                )
            ],
            [
                Paragraph(
                    (
                        f"{clean(child.first_name)} "
                        f"{clean(child.last_name)}"
                        "<br/>"
                        f"Generated {date.today().strftime('%B %d, %Y')}"
                    ),
                    subtitle_style
                )
            ]
        ],
        colWidths=[7.0 * inch]
    )

    title_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    HEADER_BG
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    BORDER
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    12
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    12
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, 0),
                    9
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    2
                ),
                (
                    "TOPPADDING",
                    (0, 1),
                    (-1, 1),
                    0
                ),
                (
                    "BOTTOMPADDING",
                    (0, 1),
                    (-1, 1),
                    9
                )
            ]
        )
    )

    story.append(title_table)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # BASIC INFORMATION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Child Information",
            section_style
        )
    )

    story.append(
        make_info_table(
            [
                (
                    "First Name",
                    child.first_name
                ),
                (
                    "Last Name",
                    child.last_name
                ),
                (
                    "Date of Birth",
                    display_date(child.date_of_birth)
                ),
                (
                    "Age",
                    calculate_age(child.date_of_birth)
                ),
                (
                    "Gender",
                    child.gender.title()
                    if child.gender
                    else "--"
                ),
                (
                    "Class",
                    child.class_name
                )
            ]
        )
    )

    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # ADDRESS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Address",
            section_style
        )
    )

    address = ", ".join(
        value
        for value in [
            child.street,
            child.city,
            child.state,
            child.zipcode
        ]
        if value
    )

    story.append(
        make_info_table(
            [
                (
                    "Address",
                    address if address else "--"
                )
            ],
            columns=1
        )
    )

    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # PROGRAM & ENROLLMENT
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Program & Enrollment",
            section_style
        )
    )

    story.append(
        make_info_table(
            [
                (
                    "Program",
                    child.program_type
                ),
                (
                    "Days Attending",
                    child.days_attending
                ),
                (
                    "Enrolled Date",
                    display_date(child.enrolled_date)
                ),
                (
                    "Start Date",
                    display_date(child.start_date)
                )
            ]
        )
    )

    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # PARENTS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Parents & Guardians",
            section_style
        )
    )

    if child.parents:

        parent_rows = [
            [
                Paragraph("Role", label_style),
                Paragraph("Name", label_style),
                Paragraph("Phone", label_style),
                Paragraph("Email", label_style),
                Paragraph("Occupation", label_style)
            ]
        ]

        for parent in child.parents:

            parent_rows.append(
                [
                    Paragraph(
                        clean(parent.role),
                        value_style
                    ),
                    Paragraph(
                        clean(parent.full_name),
                        name_style
                    ),
                    Paragraph(
                        display_phone(parent.phone_number),
                        value_style
                    ),
                    Paragraph(
                        clean(parent.email),
                        value_style
                    ),
                    Paragraph(
                        clean(parent.occupation),
                        value_style
                    )
                ]
            )

        parent_table = Table(
            parent_rows,
            colWidths=[
                0.75 * inch,
                1.45 * inch,
                1.05 * inch,
                2.0 * inch,
                1.75 * inch
            ],
            repeatRows=1
        )

        parent_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HEADER_BG
                    ),
                    (
                        "LINEBELOW",
                        (0, 0),
                        (-1, 0),
                        0.6,
                        BORDER
                    ),
                    (
                        "LINEBELOW",
                        (0, 1),
                        (-1, -1),
                        0.35,
                        GRID
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    )
                ]
            )
        )

        story.append(parent_table)

    else:

        story.append(
            Paragraph(
                "No parent information available.",
                empty_style
            )
        )

    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # AUTHORIZED PICKUPS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Authorized Pickup",
            section_style
        )
    )

    if child.pickups:

        pickup_rows = [
            [
                Paragraph("Name", label_style),
                Paragraph("Relationship", label_style),
                Paragraph("Phone", label_style)
            ]
        ]

        for pickup in child.pickups:

            pickup_rows.append(
                [
                    Paragraph(
                        clean(pickup.full_name),
                        name_style
                    ),
                    Paragraph(
                        clean(pickup.relationship),
                        value_style
                    ),
                    Paragraph(
                        display_phone(pickup.phone),
                        value_style
                    )
                ]
            )

        pickup_table = Table(
            pickup_rows,
            colWidths=[
                2.8 * inch,
                2.0 * inch,
                2.2 * inch
            ],
            repeatRows=1
        )

        pickup_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HEADER_BG
                    ),
                    (
                        "LINEBELOW",
                        (0, 0),
                        (-1, 0),
                        0.6,
                        BORDER
                    ),
                    (
                        "LINEBELOW",
                        (0, 1),
                        (-1, -1),
                        0.35,
                        GRID
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    )
                ]
            )
        )

        story.append(pickup_table)

    else:

        story.append(
            Paragraph(
                "No authorized pickup information available.",
                empty_style
            )
        )

    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # MEDICAL INFORMATION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Medical Information",
            section_style
        )
    )

    story.append(
        make_info_table(
            [
                (
                    "Allergies",
                    child.allergies
                ),
                (
                    "Medical Notes",
                    child.medical_notes
                ),
                (
                    "Additional Notes",
                    child.notes
                )
            ]
        )
    )

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------

    def draw_footer(canvas, doc):

        canvas.saveState()

        width, height = letter

        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.6)

        canvas.line(
            40,
            27,
            width - 40,
            27
        )

        canvas.setFont(
            "Helvetica",
            7.5
        )

        canvas.setFillColor(MUTED)

        canvas.drawString(
            40,
            15,
            "Thank you for being a part of our daycare family!"
        )

        canvas.drawRightString(
            width - 40,
            15,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    # ---------------------------------------------------------
    # BUILD
    # ---------------------------------------------------------

    doc.build(
        story,
        onFirstPage=draw_footer,
        onLaterPages=draw_footer
    )
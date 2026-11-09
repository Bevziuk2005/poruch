from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from pathlib import Path

out = Path(r"D:\Codex\2026-10-25\new-chat\outputs\ДЗ_2_Поруч_як_система.docx")
out.parent.mkdir(parents=True, exist_ok=True)

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.75)
sec.bottom_margin = Inches(0.7)
sec.left_margin = Inches(0.9)
sec.right_margin = Inches(0.75)

NAVY = "17365D"
BLUE = "2F75B5"
LIGHT = "EAF2F8"
GRAY = "666666"
BLACK = "111111"

styles = doc.styles
styles["Normal"].font.name = "Aptos"
styles["Normal"]._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
styles["Normal"]._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
styles["Normal"].font.size = Pt(12)
styles["Normal"].font.color.rgb = RGBColor.from_string(BLACK)
styles["Normal"].paragraph_format.space_after = Pt(6)
styles["Normal"].paragraph_format.line_spacing = 1.15

for name, size, color in [("Title", 24, NAVY), ("Heading 1", 16, NAVY), ("Heading 2", 13, BLUE)]:
    st = styles[name]
    st.font.name = "Aptos Display" if name == "Title" else "Aptos"
    st._element.rPr.rFonts.set(qn("w:ascii"), st.font.name)
    st._element.rPr.rFonts.set(qn("w:hAnsi"), st.font.name)
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = RGBColor.from_string(color)
    st.paragraph_format.space_before = Pt(12)
    st.paragraph_format.space_after = Pt(6)

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcPr.append(shd)
    shd.set(qn("w:fill"), fill)

def cell_border(cell, color="D9D9D9", size="6"):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    borders = tcPr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tcPr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = "w:" + edge
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)

def set_cell_text(cell, text, bold=False, color=BLACK, size=10, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run(text)
    r.font.name = "Aptos"
    r._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    r._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    cell_border(cell)

def add_table(headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for i, h in enumerate(headers):
        set_cell_text(table.rows[0].cells[i], h, True, "FFFFFF", 10, WD_ALIGN_PARAGRAPH.CENTER)
        shade(table.rows[0].cells[i], NAVY)
        if widths:
            table.rows[0].cells[i].width = Inches(widths[i])
    for ri, row in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(row):
            set_cell_text(cells[i], value, False, BLACK, 9)
            shade(cells[i], "FFFFFF" if ri % 2 == 0 else LIGHT)
            if widths:
                cells[i].width = Inches(widths[i])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table

def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Сторінка ")
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    paragraph._p.append(fld)

# Header/footer
header = sec.header.paragraphs[0]
header.text = "Технології створення програмного забезпечення"
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
header.runs[0].font.size = Pt(9)
header.runs[0].font.color.rgb = RGBColor.from_string(GRAY)
add_page_number(sec.footer.paragraphs[0])
sec.footer.paragraphs[0].runs[0].font.size = Pt(9)
sec.footer.paragraphs[0].runs[0].font.color.rgb = RGBColor.from_string(GRAY)

# Title page
p = doc.add_paragraph(style="Title")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Практичне завдання 2")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Опис ІТ-продукту як системи")
r.bold = True
r.font.size = Pt(18)
r.font.color.rgb = RGBColor.from_string(NAVY)
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Мобільний застосунок «Поруч»")
r.bold = True
r.font.size = Pt(16)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Офлайн-карта важливих місць і довідкові матеріали для кризових ситуацій").italic = True
doc.add_paragraph()
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.add_run("Виконав: Бевзюк Н. С.\n").bold = True
p.add_run("студент 3 курсу\nспеціальності «Комп’ютерні науки»")
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("2026").font.size = Pt(12)
doc.add_page_break()

# Body
doc.add_heading("1 Загальна характеристика системи", level=1)
doc.add_paragraph(
    "У цій роботі ІТ-продукт «Поруч» розглядається як система, що допомагає людині зорієнтуватися "
    "під час відсутності інтернету або в іншій кризовій ситуації. Застосунок зберігає на телефоні "
    "карту важливих місць, дає змогу шукати об’єкти за категоріями та містить короткі довідкові "
    "матеріали про першу допомогу і підготовку до надзвичайних ситуацій."
)
doc.add_paragraph(
    "Особливість продукту полягає в офлайн-режимі. Користувач заздалегідь завантажує дані потрібного "
    "регіону, а потім може переглядати їх без постійного підключення до мережі. Тому систему потрібно "
    "описати не тільки за її функціями, а й за складовими, з яких вона створюється."
)

doc.add_heading("2 Функціональний опис системи", level=1)
doc.add_paragraph(
    "Функціональний опис показує, що відбувається під час роботи застосунку. У центрі системи перебуває "
    "користувач, який задає запит і отримує результат. Інші частини застосунку обробляють цей запит, "
    "звертаються до локальних даних і відображають інформацію на екрані."
)
add_table(
    ["Функціональна частина", "Що робить", "Як взаємодіє з іншими частинами"],
    [
        ["Користувацький інтерфейс", "Приймає дії користувача та показує карту, результати пошуку і пости.", "Передає запити до модулів карти, пошуку та довідки."],
        ["Офлайн-карта", "Відображає збережену карту та позначки важливих місць.", "Використовує локальні геодані й передає вибраний об’єкт у картку."],
        ["Пошук і фільтрація", "Знаходить об’єкти за категорією, назвою або близькістю.", "Працює з локальною базою та повертає список результатів."],
        ["Довідковий розділ", "Показує матеріали про першу допомогу та тривожну сумку.", "Отримує текст і зображення з локального сховища."],
        ["Оновлення даних", "Завантажує нові карти, точки та матеріали, коли мережа доступна.", "Синхронізує серверні дані з локальною базою телефона."],
    ],
    widths=[1.55, 2.35, 2.65]
)

doc.add_heading("3 Робочий процес користувача", level=1)
doc.add_paragraph(
    "Типовий сценарій починається з відкриття застосунку. Користувач обирає потрібну категорію, наприклад "
    "укриття, лікарні або місця з теплом. Після цього система переглядає локальну базу, відбирає відповідні "
    "об’єкти та показує їх на карті або у вигляді списку. Користувач відкриває картку об’єкта й отримує "
    "адресу, опис та інші доступні відомості."
)
add_table(
    ["Елемент процесної моделі", "Для продукту «Поруч»"],
    [
        ["Вхід", "Запит користувача, вибрана категорія, місцезнаходження, локальна карта та база об’єктів."],
        ["Керувальні впливи", "Налаштування фільтрів, правила сортування, структура категорій і вимоги до актуальності даних."],
        ["Ресурси", "Пам’ять телефона, GPS, локальна база даних, інтерфейс застосунку та сервер для оновлення."],
        ["Дії", "Пошук, фільтрація, читання локальних даних, відображення карти, відкриття картки об’єкта."],
        ["Вихід", "Список або карта потрібних місць, детальна інформація про вибраний об’єкт чи довідковий матеріал."],
        ["Споживач результату", "Людина, яка шукає допомогу, місце для перебування або практичну інструкцію."],
    ],
    widths=[1.8, 4.75]
)

doc.add_heading("4 Фізичний та конструктивний опис", level=1)
doc.add_paragraph(
    "Фізичний опис показує, з яких програмних компонентів складається продукт. У цьому випадку "
    "«фізичними» компонентами є не деталі пристрою, а модулі програмної системи, дані та середовище, "
    "у якому вони працюють."
)
add_table(
    ["Компонент", "Призначення", "Основні дані або технології"],
    [
        ["Мобільний клієнт", "Екрани застосунку, навігація, відображення результатів.", "Код мобільного застосунку, UI-компоненти, локальні налаштування."],
        ["Локальна база даних", "Зберігає точки, категорії, координати та довідкові матеріали.", "Таблиці об’єктів, текстові записи, зображення, індекси пошуку."],
        ["Модуль карти", "Показує карту та розміщує на ній об’єкти.", "Офлайн-тайли або підготовлені фрагменти карти, координати, маркери."],
        ["Серверна частина", "Зберігає актуальні версії даних і віддає їх під час оновлення.", "API, база даних сервера, авторизація адміністратора."],
        ["Модуль адміністрування", "Додає, редагує та перевіряє інформацію про об’єкти.", "Форми редагування, статуси перевірки, журнал змін."],
        ["Довідковий контент", "Містить статті та інструкції, які доступні офлайн.", "Тексти, ілюстрації, категорії матеріалів, версії публікацій."],
    ],
    widths=[1.45, 2.55, 2.55]
)

doc.add_heading("5 Взаємодія компонентів під час оновлення", level=1)
doc.add_paragraph(
    "Коли телефон має доступ до мережі, застосунок може перевірити наявність нової версії даних. "
    "Сервер повертає тільки зміни або новий набір інформації, після чого мобільний клієнт зберігає "
    "їх у локальній базі. Якщо підключення немає, система не зупиняє роботу, а використовує останню "
    "збережену версію. Саме тому в продукті потрібно показувати дату оновлення, щоб користувач розумів, "
    "наскільки актуальною може бути інформація."
)
doc.add_paragraph(
    "Структурно систему можна уявити як зв’язок між трьома рівнями: інтерфейсом, локальними даними "
    "та серверною частиною. Інтерфейс взаємодіє з локальною базою під час звичайної роботи. Сервер "
    "потрібен переважно для підготовки й оновлення даних, а не для кожного окремого пошукового запиту."
)

doc.add_heading("6 Висновок", level=1)
doc.add_paragraph(
    "Застосунок «Поруч» є системою, у якій окремі модулі пов’язані спільною метою: надати користувачу "
    "важливу інформацію навіть без інтернету. Функціональний опис пояснює послідовність роботи від "
    "запиту до результату, а конструктивний опис показує, з яких компонентів цей результат формується."
)
doc.add_paragraph(
    "Такий поділ допомагає визначити межі майбутньої розробки. Для першого прототипу достатньо реалізувати "
    "мобільний клієнт, локальну базу, карту, пошук і довідковий розділ. Сервер та адміністрування можна "
    "розглядати як частини наступного етапу, потрібні для підтримки актуальності даних."
)

doc.save(out)
print(out)


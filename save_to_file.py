import os
from docx import Document
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def add_page_break(document):
    """添加分页符"""
    document.add_page_break()

def save_to_word(question_data, filename="ICBC_题库.docx"):
    """先存无图片题目，再存有图片题目，每页不固定题目数量"""
    document = Document()
    document.add_heading("ICBC 题库", level=1)

    # **分离无图片和有图片的题目**
    no_image_questions = [q for q in question_data if not q["image"]]
    image_questions = [q for q in question_data if q["image"]]

    def add_questions_to_document(questions, start_index=0):
        """按顺序存储题目，每页自动分页"""
        for item in questions:
            # **题目**
            p = document.add_paragraph()
            run = p.add_run(f"Q{questions.index(item) + start_index + 1}: {item['question']}")
            run.bold = True
            run.font.size = Pt(9)  # 字体变小
            p.paragraph_format.space_after = Pt(2)  # 行间距缩小

            # **图片**
            if item["image"] and os.path.exists(item["image"]):
                p = document.add_paragraph()
                p.add_run().add_picture(item["image"], width=Inches(2.2))  # 图片缩小

            # **选项**
            for option in item["options"]:
                p = document.add_paragraph(f"{option['letter']}: {option['text']}")
                p.paragraph_format.space_after = Pt(2)  # 行间距缩小
                p.runs[0].font.size = Pt(9)  # 字体变小

            # **正确答案**
            p = document.add_paragraph(f"✅ 正确答案: {item['correct_answer']}")
            p.runs[0].font.size = Pt(9)  # 字体变小
            p.paragraph_format.space_after = Pt(2)  # 行间距缩小

            
    # **先存无图片的题目**
    add_questions_to_document(no_image_questions, 0)
    
    # **再存有图片的题目**
    add_questions_to_document(image_questions, start_index=len(no_image_questions) )

    document.save(filename)
    print(f"✅ 所有题目已保存到 {filename}")

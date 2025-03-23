import sqlite3

def store_questions(data_list, db_path="data.db"):
    """
    将题目列表存入 SQLite 数据库
    :param data_list: 包含多个题目的 JSON 列表
    :param db_path: SQLite 数据库文件路径
    """
    # 连接 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表（如果不存在）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            a_letter TEXT, a_text TEXT,
            b_letter TEXT, b_text TEXT,
            c_letter TEXT, c_text TEXT,
            d_letter TEXT, d_text TEXT,
            image TEXT,
            correct_answer TEXT
        )
    """)

    # 遍历 JSON 数据列表并存入数据库
    for data in data_list:
        question_text = data["question"]
        image_path = data["image"]
        correct_answer = data["correct_answer"]

        # 解析选项
        options = {opt["letter"]: opt["text"] for opt in data["options"]}

        # 插入数据
        cursor.execute("""
            INSERT INTO questions (
                question, 
                a_letter, a_text, 
                b_letter, b_text, 
                c_letter, c_text, 
                d_letter, d_text, 
                image, correct_answer
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            question_text,
            "A", options.get("A", ""),
            "B", options.get("B", ""),
            "C", options.get("C", ""),
            "D", options.get("D", ""),
            image_path,
            correct_answer
        ))

    # 提交事务并关闭数据库
    conn.commit()
    conn.close()
    print(f"{len(data_list)} 道题目已成功存入数据库！")

# 示例 JSON 题目列表
data_list = [
    {
        "question": "此路标表示：",
        "options": [
            {"letter": "A", "text": "前方有高度较低的立交桥"},
            {"letter": "B", "text": "前方有铁路平交道"},
            {"letter": "C", "text": "前方有隐蔽的交叉路口或旁路"},
            {"letter": "D", "text": "前路不通；请向右转或向左转"}
        ],
        "image": "images_download\\V061.jpg",
        "correct_answer": "C"
    },
    {
        "question": "这个标志的含义是什么？",
        "options": [
            {"letter": "A", "text": "禁止驶入"},
            {"letter": "B", "text": "注意危险"},
            {"letter": "C", "text": "施工路段"},
            {"letter": "D", "text": "单行道"}
        ],
        "image": "images_download\\V062.jpg",
        "correct_answer": "A"
    }
]

# 调用方法，存储题目列表
store_questions(data_list)

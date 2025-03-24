import json


# 保存 questions 到 JSON 文件
def save_to_json(questions, filename="questions.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=4)
        print(f"✅ 已保存到 {filename}")
    except Exception as e:
        print(f"❌ 保存 JSON 文件失败: {e}")


# 从 JSON 文件读取题目
def load_from_json(filename="questions.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        print(f"✅ 从 {filename} 成功加载 {len(questions)} 道题目")
        return questions
    except FileNotFoundError:
        print("❌ 找不到 JSON 文件")
        return []
    except json.JSONDecodeError:
        print("❌ 读取 JSON 文件时出现错误")
        return []
    except Exception as e:
        print(f"❌ 加载 JSON 文件失败: {e}")
        return []

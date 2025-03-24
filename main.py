# main.py
from scraper import scrape_questions
from save_to_file import save_to_word
import json


def remove_duplicates(questions):
    """去重，确保相同题目不重复"""
    unique_questions = []
    seen_questions = set()

    for question in questions:
        question_text_image = question["question"] + "_" + question["image"]
        if question_text_image not in seen_questions:
            seen_questions.add(question_text_image)
            unique_questions.append(question)

    return unique_questions


def get_question_set(questions):
        
    # 创建一个空的 set
    question_set = set()

    # 遍历 data_list，将 question + "_" + image 组合后加入 set
    for item in questions:
        question_set.add(item["question"] + "_" + item["image"])
    
    return question_set




# 保存 questions 到 JSON 文件
def save_to_json(questions, filename="questions.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=4)
        print(f"✅ 所有题目已保存到 {filename}")
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


if __name__ == "__main__":
    print("🚀 开始抓取 ICBC 题目...")

    all_questions = []  # 存储所有去重后的题目

    # 如果存在已经保存的 JSON 文件，可以选择读取文件中的题目
    all_questions = load_from_json()  # 尝试从 JSON 文件加载题目

    question_set = get_question_set(all_questions)

    # 进行抓取  完整测试
    for i in range(5):  # 控制抓取次数，可以根据需要调整
        print(f"\n========================================================================")
        print(f"🔄 第 {i+1} 次抓取..完整测试...")
        new_questions = scrape_questions(True, question_set)

        if new_questions:
            all_questions.extend(new_questions)  # 合并题目
            all_questions = remove_duplicates(all_questions)  # 去重
            question_set = get_question_set(all_questions)
            print(f"✅ 当前总题目数: {len(all_questions)}")

            # 继续处理题目，保存到 Word
            print(f"✅ 全部抓取完成，共 {len(all_questions)} 道题目")
            save_to_word(all_questions)  # 保存到 Word
            # 存储抓取到的题目为 JSON 文件
            save_to_json(all_questions)  # 保存到 JSON 文件

        else:
            print(f"⚠️ 第 {i+1} 次抓取 没有新题目，跳过")


    # 进行抓取  标志测试
    for i in range(5):  # 控制抓取次数，可以根据需要调整
        print(f"\n========================================================================")
        print(f"🔄 第 {i+1} 次抓取..标志测试...")
        new_questions = scrape_questions(False, question_set)

        if new_questions:
            all_questions.extend(new_questions)  # 合并题目
            all_questions = remove_duplicates(all_questions)  # 去重
            question_set = get_question_set(all_questions)
            print(f"✅ 当前总题目数: {len(all_questions)}")

            # 继续处理题目，保存到 Word
            print(f"✅ 全部抓取完成，共 {len(all_questions)} 道题目")
            save_to_word(all_questions)  # 保存到 Word
            # 存储抓取到的题目为 JSON 文件
            save_to_json(all_questions)  # 保存到 JSON 文件

        else:
            print(f"⚠️ 第 {i+1} 次抓取 没有新题目，跳过")
    

    # 存储抓取到的题目为 JSON 文件
    if all_questions:
        print(f"✅ 全部抓取完成，共 {len(all_questions)} 道题目")
        save_to_json(all_questions)  # 保存到 JSON 文件
        # 继续处理题目，保存到 Word
        save_to_word(all_questions)  # 保存到 Word
    else:
        print("❌ 没有获取到任何题目")
# main.py
from scraper import scrape_questions
from save_to_file import save_to_word
from save_json import save_to_json, load_from_json
import json
import os


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


if __name__ == "__main__":
    print("🚀 开始抓取 ICBC 题目...")

    all_questions = []  # 存储所有去重后的题目

    # 如果存在已经保存的 JSON 文件，可以选择读取文件中的题目
    all_questions = load_from_json()  # 尝试从 JSON 文件加载题目


    # # 这部分为补充，加载最近两个版本 start
    # json_filename = os.path.join("json", "questions_20250322.json")
    # all_questions2 = load_from_json(json_filename)  # 尝试从 JSON 文件加载题目
    # all_questions.extend(all_questions2)  # 合并题目
    # all_questions = remove_duplicates(all_questions)  # 去重
    # print(f"✅ 从 Json 文件加载完毕, 去重后，当前总题目数: {len(all_questions2)}")
    # # 这部分为补充  end

    question_set = get_question_set(all_questions)

    # 进行抓取  完整测试
    for i in range(50):  # 控制抓取次数，可以根据需要调整
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
    for i in range(50):  # 控制抓取次数，可以根据需要调整
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
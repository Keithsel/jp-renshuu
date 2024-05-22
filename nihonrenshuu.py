from pynput.keyboard import Key, Listener
import time
import pandas as pd
import multiprocessing
import threading

hiragana = pd.read_csv('data/normal/hiragana.csv')
katakana = pd.read_csv('data/normal/katakana.csv')
english_vocab = pd.read_csv('data/normal/vocab_en.csv')
vietnamese_vocab = pd.read_csv('data/normal/vocab_vi.csv')

def choose_settings():
    global char_type, vocab_language
    char_type = input("Choose character type for the test: \n1. Hiragana\n2. Katakana\nYour choice: ").strip().lower()
    vocab_language = input("Choose meaning language: \n1. English (en)\n2. Vietnamese (vi)\nYour choice: ").strip().lower()

    # Mapping choices to character types
    char_type = 'hiragana' if char_type in ['1', 'hiragana'] else 'katakana'
    # Mapping choices to vocabulary languages
    vocab_language = 'english' if vocab_language in ['1', 'en', 'english'] else 'vietnamese'

def generate_questions():
    char_data = hiragana if char_type == 'hiragana' else katakana
    vocab_data = english_vocab if vocab_language == 'english' else vietnamese_vocab

    char_questions = char_data.sample(5)
    vocab_questions = vocab_data.sample(5)

    combined_questions = list(zip(char_questions['romaji'].tolist(), vocab_questions['meaning'].tolist()))
    combined_answers = list(zip(char_questions[char_type].tolist(), vocab_questions['kana'].tolist()))
    return combined_questions, combined_answers

def display_test(questions):
    print("\nTest Started. You have 60 seconds. Press Space to end earlier.")
    print(f"{'Character (1-5)':<15}{'Vocabulary (6-10)':<25}")
    print("-" * 50)
    for idx, (char, vocab) in enumerate(questions, 1):
        vocab_index = idx + 5
        print(f"{idx:<2}. {char:<12} {vocab_index:<2}. {vocab}")

def display_answers(answers):
    print("\nCorrect Answers:")
    print(f"{'Character':<15}{'Vocabulary':<25}")
    print("-" * 50)
    for idx, (char, vocab) in enumerate(answers, 1):
        vocab_index = idx + 5  # Offset by 5 for vocab index
        print(f"{idx:<2}. {char:<12} {vocab_index:<2}. {vocab}")

def on_press(key):
    global test_running, listener, all_questions, all_answers, test_started, test_process
    if key == Key.space and test_running:
        if not test_started:
            test_started = True
            display_test(all_questions)
            test_process = multiprocessing.Process(target=timer_end_test)
            test_process.start()
        else:
            end_test(test_process)

def timer_end_test():
    time.sleep(60)
    end_test(None)

def end_test(process):
    global test_running, test_started
    if test_running:
        test_running = False
        test_started = False
        print("\nTime limit exceeded or test manually ended.")
        display_answers(all_answers)
        if process:
            process.terminate()
        listener.stop()

def ask_to_continue():
    continue_test = input("Do you want to continue? (y/N): ").replace(" ", "")
    if continue_test.lower() == 'y':
        start_test()

def start_test():
    global test_running, listener, all_questions, all_answers, test_started
    all_questions, all_answers = generate_questions()
    test_running = True
    test_started = False
    print("Press Space to start the test.")
    with Listener(on_press=on_press) as listener:
        listener.join()
    ask_to_continue()

if __name__ == '__main__':
    choose_settings()
    start_test()
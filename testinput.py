from pynput.keyboard import Key, Listener
import time

def on_press(key):
    global start_time, test_running
    if key == Key.space:
        if test_running:
            test_running = False
            end_time = time.time()
            test_duration = end_time - start_time
            print(f"\nTest Ended. Duration: {test_duration:.2f} seconds")
            print("Enter the indexes of words you had trouble with:")
            trouble_indexes = input()
            print(f"Trouble indexes: {trouble_indexes}")
            return False
        else:
            test_running = True
            start_time = time.time()
            print("\nTest Started. Press Space to end.")

def start_test():
    global test_running
    test_running = False
    print("Press Space to start the test.")
    with Listener(on_press=on_press) as listener:
        listener.join()

start_test()

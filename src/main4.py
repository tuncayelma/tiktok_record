import argparse
import subprocess
import threading
import requests
import time
import sys

# Hàm để phân tích cú pháp các đối số dòng lệnh
def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-username",
                        dest="username",
                        help="Tên danh sách username.",
                        required=True,
                        action='store')
    
    args = parser.parse_args()
    return args

# Hàm để chạy lệnh bên ngoài và dừng sau 5 giờ
def run_command(username, output):
    """Chạy subprocess với giới hạn 5 giờ"""
    start_time = time.time()  # Lưu thời gian bắt đầu
    time_limit = 5 * 60 * 60  # 5 giờ tính bằng giây

    command = f"python3 ./src/main.py -user {username} -mode automatic -output {output}"
    
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Kiểm tra quá trình chạy
        while process.poll() is None:
            elapsed_time = time.time() - start_time
            if elapsed_time >= time_limit:
                print(f"Thread xử lý username {username} đã chạy quá 5 giờ, dừng ngay.")
                process.terminate()  # Dừng quá trình
                return
        
            time.sleep(10)  # Kiểm tra sau mỗi 10 giây
        
        stdout, stderr = process.communicate()
        print(stdout)
        if stderr:
            print(f"Lỗi khi chạy lệnh: {stderr}")

    except Exception as e:
        print(f"Lỗi khi chạy lệnh cho {username}: {str(e)}")

# # Đọc usernames từ file TXT
# def load_usernames(file_path):
#     with open(file_path, 'r', encoding="utf-8") as file:
#         usernames = [line.strip() for line in file if line.strip()]
#     return usernames

def load_usernames(file_path):
    with open(file_path, 'r') as file:
        usernames = [line.strip() for line in file if line.strip()]
    return usernames

# Chia usernames thành 10 danh sách dựa trên tên danh sách
def split_usernames(usernames, num_lists=10):
    return [usernames[i::num_lists] for i in range(num_lists)]

# Chia usernames thành 10 danh sách dựa trên tên danh sách
def split_usernames(usernames, num_lists=10):
    return [usernames[i::num_lists] for i in range(num_lists)]

def main():
    args = parse_args()
    output = args.username
    
    #url = "https://raw.githubusercontent.com/anisidina29/tiktok-live-recorder/main/usernames.txt"
    output_file = "./src/usernames.txt"

    # response = requests.get(url)
    
    # if response.status_code == 200:
    #     with open(output_file, "w", encoding="utf-8") as file:
    #         file.write(response.text)
    #     print(f"File downloaded successfully and saved as {output_file}")
    # else:
    #     print(f"Failed to download file. Status code: {response.status_code}")
    #     sys.exit(1)

    # Đọc usernames từ file TXT
    usernames = load_usernames(output_file)

    # Chia usernames thành 10 danh sách
    username_lists = split_usernames(usernames, num_lists=9)

    # Tạo mapping giữa tên danh sách và chỉ số danh sách
    # username_map = {
    #     'usernames1': 0, 'usernames2': 1, 'usernames3': 2, 'usernames4': 3, 'usernames5': 4,
    #     'usernames6': 5, 'usernames7': 6, 'usernames8': 7, 'usernames9': 8, 'usernames10': 9
    # }
        username_map = {
        'usernames1': 0, 'usernames2': 1, 'usernames3': 2, 'usernames4': 3, 'usernames5': 4,
        'usernames6': 5, 'usernames7': 6, 'usernames8': 7, 'usernames9': 8
    }

    # Lấy danh sách các username từ đối số dòng lệnh
    if args.username in username_map:
        index = username_map[args.username]
        usernames_to_process = username_lists[index]
    else:
        print("Tên danh sách username không hợp lệ.")
        sys.exit(1)

    # Tạo và chạy các thread với thời gian giới hạn
    threads = []
    
    for username in usernames_to_process:
        thread = threading.Thread(target=run_command, args=(username, output))
        threads.append(thread)
        thread.start()

    # Đợi tất cả các thread hoàn thành
    for thread in threads:
        thread.join()

    print("Tất cả luồng đã hoàn thành hoặc bị dừng sau 5 giờ.")

if __name__ == "__main__":
    main()

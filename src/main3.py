import argparse
import subprocess
import threading
import requests
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

# Hàm để chạy lệnh bên ngoài
def run_command(username, output):
    command = f"python3 anisidina29/tiktok_record/src/main.py  -user {username} -mode automatic -output {output}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' returned non-zero exit status {e.returncode}.")
        print(f"Error output: {e.stderr}")

# Đọc usernames từ file TXT
def load_usernames(file_path):
    with open(file_path, 'r') as file:
        usernames = [line.strip() for line in file if line.strip()]
    return usernames

# Chia usernames thành 10 danh sách dựa trên tên danh sách
def split_usernames(usernames, num_lists=10):
    return [usernames[i::num_lists] for i in range(num_lists)]

def main():
    args = parse_args()
    output = args.username
      
    url = "https://raw.githubusercontent.com/anisidina29/tiktok-live-recorder/main/usernames.txt"
    output_file = "anisidina29/tiktok_record/src/usernames.txt"
  
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"File downloaded successfully and saved as {output_file}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        
    # Đọc usernames từ file TXT
    usernames = load_usernames(output_file)
    
    # Chia usernames thành 10 danh sách
    username_lists = split_usernames(usernames)
    
    # Tạo mapping giữa tên danh sách và chỉ số danh sách
    username_map = {
        'usernames1': 0,
        'usernames2': 1,
        'usernames3': 2,
        'usernames4': 3,
        'usernames5': 4,
        'usernames6': 5,
        'usernames7': 6,
        'usernames8': 7,
        'usernames9': 8,
        'usernames10': 9
    }
    
    # Lấy danh sách các username từ đối số dòng lệnh
    if args.username in username_map:
        index = username_map[args.username]
        usernames_to_process = username_lists[index]
    else:
        print("Tên danh sách username không hợp lệ.")
        return
    
    # Tạo luồng cho mỗi username trong danh sách
    threads = []
    for username in usernames_to_process:
        thread = threading.Thread(target=run_command, args=(username, output))
        threads.append(thread)

    # Bắt đầu chạy các luồng
    for thread in threads:
        thread.start()

    # Đợi tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()

    print("Tất cả luồng đã hoàn thành.")

if __name__ == "__main__":
    main()

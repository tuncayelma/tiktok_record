import os
import subprocess
import sys
import zipfile

def unzip_all_files_in_directory(directory):
    # Lặp qua tất cả các file trong thư mục hiện tại
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        # Kiểm tra nếu item là file ZIP
        if os.path.isfile(item_path) and item.lower().endswith('.zip'):
            # Tạo thư mục mới để giải nén file
            extract_dir = os.path.join(directory, os.path.splitext(item)[0])
            
            # Nếu thư mục giải nén chưa tồn tại, thì giải nén
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)
                with zipfile.ZipFile(item_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                    print(f'Đã giải nén {item} vào {extract_dir}')
                    
                # Sau khi giải nén xong, xóa file zip
                os.remove(item_path)
                print(f'Đã xóa file ZIP {item}')
            else:
                print(f'Thu mục {extract_dir} đã tồn tại, bỏ qua {item}')

if __name__ == "__main__":
    # Lấy thư mục hiện tại
    current_directory = os.getcwd()
    unzip_all_files_in_directory(current_directory)

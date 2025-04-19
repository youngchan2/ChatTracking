import re
import glob
import os
from collections import defaultdict

chat_bot = ['채팅도구', '주식봇', '뉴스봇']

def load_kakao_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def extract_message_data(lines):
    # 메시지 패턴 정의 (날짜, 시간, 사용자명 추출)
    message_pattern = re.compile(r'\d{4}\. \d{1,2}\. \d{1,2}\. \d{1,2}:\d{2}, (.+?) : .+')
    message_counts = defaultdict(int)
    
    for line in lines:
        match = message_pattern.match(line)
        if match:
            sender = match.group(1)
            message_counts[sender] += 1
            
    return message_counts

def get_combined_message_counts(dir_path):
    txt_files = glob.glob(os.path.join(dir_path, '*.txt'))  # 모든 .txt 파일 리스트 가져오기
    combined_message_counts = defaultdict(int)  # 모든 파일의 결과를 합칠 딕셔너리
    
    for file_path in txt_files:
        lines = load_kakao_chat(file_path)  # 파일 읽기
        message_counts = extract_message_data(lines)  # 메시지 카운트 추출
        
        # 각 파일의 메시지 카운트를 합치기
        for sender, count in message_counts.items():
            combined_message_counts[sender] += count
    
    return combined_message_counts

def display_message_counts(date1, message_counts, title="Message Counts"):
    # 값을 기준으로 내림차순 정렬된 리스트 생성
    sorted_counts = sorted(message_counts.items(), key=lambda x: x[1], reverse=True)
    
    # 정렬된 결과 출력
    print(f"===\t[{date1}]\t===")
    print(f"===\t{title}\t===")
    for sender, count in sorted_counts:
        print(f'{sender}: {count} messages')

def compare_message_counts(date1, counts1, date2, counts2):
    # 두 기간 동안의 차이 계산
    all_senders = set(counts1.keys()).union(set(counts2.keys()))
    diff_counts = {}
    
    for sender in all_senders:
        count1 = counts1.get(sender, 0)
        count2 = counts2.get(sender, 0)
        diff_counts[sender] = abs(count1 - count2)
    
    # 차이를 기준으로 내림차순 정렬하여 출력
    sorted_diff = sorted(diff_counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"===\t{date1}~{date2}\t===")
    for sender, diff in sorted_diff:
        if sender in chat_bot:
            continue
        print(f'{sender}: +{diff} messages')

def main():
    # 두 기간 동안의 데이터 디렉토리 설정
    pwd = '/Users/chan/Documents/playground/ChatTracker/gsa_chat_data/'
    
    date1 = '25.04.18'
    dir_path_1 = f'{pwd}/{date1}'
    date2 = '25.02.18'
    dir_path_2 = f'{pwd}/{date2}'
    
    # 첫 번째 기간의 메시지 개수
    message_counts_1 = get_combined_message_counts(dir_path_1)
    display_message_counts(date1, message_counts_1, "Message Counts")
    
    message_counts_2 = get_combined_message_counts(dir_path_2)
    display_message_counts(date2, message_counts_2, "Message Counts")
    # 두 기간의 메시지 개수 차이 비교
    compare_message_counts(date1, message_counts_1, date2, message_counts_2)

if __name__ == '__main__':
    main()

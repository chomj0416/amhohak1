import string

# I와 J를 하나로 취급하기 위해 J를 제외한 알파벳
ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ" 

def create_playfair_matrix(key):
    """키워드를 사용하여 5x5 플레이페어 행렬을 생성합니다."""
    key = key.upper().replace('J', 'I')
    key_chars = []
    
    # 1. 키워드 문자 추가 (중복 제거)
    for char in key:
        if char not in key_chars and char in ALPHABET:
            key_chars.append(char)
            
    # 2. 나머지 알파벳 추가 (J 제외)
    for char in ALPHABET:
        if char not in key_chars:
            key_chars.append(char)
            
    # 3. 5x5 행렬로 변환
    matrix = []
    for i in range(5):
        matrix.append(key_chars[i*5 : (i+1)*5])
        
    return matrix

def get_char_pos(matrix, char):
    """행렬에서 문자의 (행, 열) 위치를 찾습니다."""
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return -1, -1

def preprocess_plaintext(plaintext):
    """평문 전처리: 대문자, J->I, 같은 문자 쌍에 X 삽입, 홀수 길이 시 X 추가"""
    # 공백 제거 후 대문자 및 J->I 치환
    text = plaintext.upper().replace('J', 'I').replace(' ', '')
    processed_text = ""
    i = 0
    while i < len(text):
        char1 = text[i]
        
        if i + 1 < len(text):
            char2 = text[i+1]
            # 같은 문자가 쌍에 오면 중간에 X 삽입
            if char1 == char2:
                processed_text += char1 + 'X'
                i += 1
            else:
                processed_text += char1 + char2
                i += 2
        else:
            # 마지막 글자 처리: 홀수 길이이면 X 추가
            processed_text += char1 + 'X' 
            i += 1
            
    # 알파벳만 포함하도록 최종 필터링
    return "".join(c for c in processed_text if c in ALPHABET)

def playfair_encrypt(plaintext, key):
    """플레이페어 암호화 함수"""
    matrix = create_playfair_matrix(key)
    processed_text = preprocess_plaintext(plaintext)
    ciphertext = ""
    
    for i in range(0, len(processed_text), 2):
        char1 = processed_text[i]
        char2 = processed_text[i+1]
        r1, c1 = get_char_pos(matrix, char1)
        r2, c2 = get_char_pos(matrix, char2)
        
        # 1. 같은 행: 오른쪽으로 한 칸
        if r1 == r2: 
            new_c1 = (c1 + 1) % 5
            new_c2 = (c2 + 1) % 5
            ciphertext += matrix[r1][new_c1] + matrix[r2][new_c2]
        # 2. 같은 열: 아래로 한 칸
        elif c1 == c2: 
            new_r1 = (r1 + 1) % 5
            new_r2 = (r2 + 1) % 5
            ciphertext += matrix[new_r1][c1] + matrix[new_r2][c2]
        # 3. 직사각형: 대각선 교환
        else: 
            ciphertext += matrix[r1][c2] + matrix[r2][c1]
            
    return ciphertext

def playfair_decrypt(ciphertext, key):
    """플레이페어 복호화 함수 (암호화의 역순 적용)"""
    matrix = create_playfair_matrix(key)
    decrypted_text = ""
    
    # 암호문은 항상 길이가 짝수
    for i in range(0, len(ciphertext), 2):
        char1 = ciphertext[i]
        char2 = ciphertext[i+1]
        r1, c1 = get_char_pos(matrix, char1)
        r2, c2 = get_char_pos(matrix, char2)

        # 1. 같은 행: 왼쪽으로 한 칸
        if r1 == r2: 
            new_c1 = (c1 - 1) % 5
            new_c2 = (c2 - 1) % 5
            decrypted_text += matrix[r1][new_c1] + matrix[r2][new_c2]
        # 2. 같은 열: 위로 한 칸
        elif c1 == c2: 
            new_r1 = (r1 - 1) % 5
            new_r2 = (r2 - 1) % 5
            decrypted_text += matrix[new_r1][c1] + matrix[new_r2][c2]
        # 3. 직사각형: 대각선 교환 (동일)
        else: 
            decrypted_text += matrix[r1][c2] + matrix[r2][c1]
            
    return decrypted_text

# --------------------------------------------------
#                   실행 예시 (VS Code 터미널 출력용)
# --------------------------------------------------
if __name__ == "__main__":
    key = "MONARCHY"
    plaintext = "SECRET MESSAGE"

    ciphertext = playfair_encrypt(plaintext, key)
    decryptedtext = playfair_decrypt(ciphertext, key)

    print("-" * 40)
    print(f"키워드: {key}")
    
    print("\n--- 5x5 키 매트릭스 ---")
    for row in create_playfair_matrix(key):
        print(row)
    print("------------------------")
    
    print(f"평문: {plaintext}")
    print(f"전처리된 평문(암호화 쌍): {preprocess_plaintext(plaintext)}")
    print(f"암호문: {ciphertext}")
    print(f"복호문: {decryptedtext}")
    print("-" * 40)
import json
import os
import shutil

class Quiz:
    def __init__(self, question, options, answer, category="일반", difficulty="보통"):
        self.question = question
        self.options = options   # 리스트 형태의 보기
        self.answer = answer     # 정답 번호 (1~4)
        self.category = category
        self.difficulty = difficulty

    def to_dict(self):
        return {
            "question": self.question,
            "options": self.options,
            "answer": self.answer,
            "category": self.category,
            "difficulty": self.difficulty
        }

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.file_path = 'state.json'
        self.load_data()

    def load_data(self):
        """파일 읽기 및 손상 시 복구 로직"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.quizzes = [
                        Quiz(
                            q['question'], 
                            q.get('options') or q.get('choices'), 
                            q['answer'],
                            q.get('category', '일반'),
                            q.get('difficulty', '보통')
                        ) for q in data.get("quizzes", [])
                    ]
            else:
                self.set_default_quizzes()
        except (json.JSONDecodeError, KeyError):
            print("\n⚠️ 데이터 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self.set_default_quizzes()

    def set_default_quizzes(self):
        """기본 퀴즈 데이터 5개"""
        self.quizzes = [
            Quiz("Python에서 리스트에 요소를 추가하는 함수는?", ["1. push()", "2. append()", "3. add()", "4. insert_end()"], 2, "프로그래밍", "보통"),
            Quiz("대한민국의 수도는 어디인가요?", ["1. 부산", "2. 인천", "3. 대구", "4. 서울"], 4, "상식", "쉬움"),
            Quiz("지구에서 가장 큰 바다는?", ["1. 대서양", "2. 인도양", "3. 태평양", "4. 북극해"], 3, "과학", "보통"),
            Quiz("나비의 다리 개수는 몇 개인가요?", ["1. 2개", "2. 4개", "3. 6개", "4. 8개"], 3, "과학", "쉬움"),
            Quiz("HTML에서 하이퍼링크를 만드는 태그는?", ["1. <link>", "2. <a>", "3. <href>", "4. <url>"], 2, "프로그래밍", "보통")
        ]
        self.save_data()

    def save_data(self):
        """데이터 저장 및 백업본 생성"""
        try:
            if os.path.exists(self.file_path):
                shutil.copy(self.file_path, self.file_path + ".bak")
            
            data = {
                "high_score": self.high_score,
                "quizzes": [q.to_dict() for q in self.quizzes]
            }
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"\n[오류] 데이터 저장 실패: {e}")

    def get_safe_input(self, prompt, min_val, max_val):
        """예외 처리를 포함한 숫자 입력 함수"""
        while True:
            try:
                user_input = input(f"{prompt} ({min_val}~{max_val}): ").strip()
                if not user_input:
                    continue
                val = int(user_input)
                if min_val <= val <= max_val:
                    return val
                print(f"범위 오류: {min_val}~{max_val} 사이를 입력하세요.")
            except ValueError:
                print("입력 오류: 숫자를 입력해주세요.")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0
        print(f"\n--- 퀴즈 시작! (현재 최고 점수: {self.high_score}) ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"\nQ{i}. [{q.category} | 난이도: {q.difficulty}] {q.question}")
            for opt in q.options:
                print(f"  {opt}")
            
            user_ans = self.get_safe_input("정답 번호 선택", 1, 4)
            if user_ans == q.answer:
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 {q.answer}번입니다.")
        
        print(f"\n[최종 결과] {len(self.quizzes)}문제 중 {score}문제를 맞혔습니다!")
        if score > self.high_score:
            print(f"🎊 최고 점수 갱신! ({self.high_score} -> {score})")
            self.high_score = score
            self.save_data()

    def add_quiz(self):
        print("\n--- 새 퀴즈 추가 ---")
        question = input("문제 내용을 입력하세요: ").strip()
        while not question:
            question = input("문제 내용은 비어둘 수 없습니다. 다시 입력: ").strip()
        
        options = []
        for i in range(1, 5):
            opt = input(f"보기 {i} 입력: ").strip()
            options.append(f"{i}. {opt}")
        
        answer = self.get_safe_input("정답 번호 입력", 1, 4)
        category = input("카테고리 (예: 과학, 역사): ").strip() or "일반"
        difficulty = input("난이도 (상/중/하): ").strip() or "보통"
        
        # [수정] Quiz 생성 시 5개의 인자를 모두 전달해야 합니다.
        self.quizzes.append(Quiz(question, options, answer, category, difficulty))
        self.save_data()
        print("✨ 퀴즈가 성공적으로 추가되었습니다!")

    def show_list(self):
        print("\n--- 퀴즈 목록 ---")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. [{q.category}] {q.question} (정답: {q.answer}번)")

    def show_high_score(self):
        print(f"\n🏆 현재 최고 점수: {self.high_score}점")

def main():
    game = QuizGame()
    try:
        while True:
            print("\n==== 퀴즈 게임 메뉴 ====")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록 보기")
            print("4. 최고 점수 확인")
            print("5. 종료")
            
            choice = game.get_safe_input("메뉴 선택", 1, 5)

            if choice == 1:
                game.play_quiz()
            elif choice == 2:
                game.add_quiz()
            elif choice == 3:
                game.show_list()
            elif choice == 4:
                game.show_high_score()
            elif choice == 5:
                print("게임을 종료합니다. 안녕!")
                break
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 비정상 종료 감지: 데이터를 저장하고 종료합니다.")
        game.save_data()

if __name__ == "__main__":
    main()
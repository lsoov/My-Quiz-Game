import json
import os
# 퀴즈정보를 담는 클래스
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices  # 4개의 선택지 리스트
        self.answer = answer    # 정답 번호 (1~4)

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
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
                        Quiz(q['question'], q['choices'], q['answer']) 
                        for q in data.get("quizzes", [])
                    ]
            else:
                self.set_default_quizzes()
        except (json.JSONDecodeError, KeyError):
            print("\n⚠️ 데이터 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self.set_default_quizzes()
            self.save_data()

    def set_default_quizzes(self):
        """기본 퀴즈 데이터 5개"""
        self.quizzes = [
            Quiz("Python에서 리스트에 요소를 추가하는 함수는?", ["push()", "append()", "add()", "insert_end()"], 2),
            Quiz("대한민국의 수도는 어디인가요?", ["부산", "인천", "대구", "서울"], 4),
            Quiz("지구에서 가장 큰 바다는?", ["대서양", "인도양", "태평양", "북극해"], 3),
            Quiz("나비의 다리 개수는 몇 개인가요?", ["2개", "4개", "6개", "8개"], 3),
            Quiz("HTML에서 하이퍼링크를 만드는 태그는?", ["<link>", "<a>", "<href>", "<url>"], 2)
        ]

    def save_data(self):
        """데이터 저장"""
        data = {
            "high_score": self.high_score,
            "quizzes": [q.to_dict() for q in self.quizzes]
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_safe_input(self, prompt, min_val=None, max_val=None):
        """예외 처리를 포함한 숫자 입력 함수"""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("⚠️ 입력값이 비어있습니다. 다시 입력해주세요.")
                    continue
                
                val = int(user_input)
                if min_val is not None and max_val is not None:
                    if not (min_val <= val <= max_val):
                        print(f"⚠️ {min_val}~{max_val} 사이의 숫자를 입력해주세요.")
                        continue
                return val
            except ValueError:
                print("⚠️ 숫자로만 입력해주세요.")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0
        print(f"\n--- 퀴즈 시작! (현재 최고 점수: {self.high_score}) ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"\nQ{i}. {q.question}")
            for idx, choice in enumerate(q.choices, 1):
                print(f"  {idx}) {choice}")
            
            user_ans = self.get_safe_input("정답 번호 선택 (1~4): ", 1, 4)
            
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
        
        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i} 입력: ").strip()
            while not choice:
                choice = input(f"선택지 {i}는 비어둘 수 없습니다. 다시 입력: ").strip()
            choices.append(choice)
        
        answer = self.get_safe_input("정답 번호 입력 (1~4): ", 1, 4)
        
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_data()
        print("✨ 퀴즈가 성공적으로 추가되었습니다!")

    def show_list(self):
        print("\n--- 퀴즈 목록 ---")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question} (정답: {q.answer}번)")

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
            
            choice = game.get_safe_input("메뉴 선택: ", 1, 5)

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
        print("\n\n⚠️ 비정상 종료가 감지되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
        game.save_data()

if __name__ == "__main__":
    main()
 # 최종 수정완료

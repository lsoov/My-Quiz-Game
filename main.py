import json
import os

class Quiz:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.file_path = "quizzes.json"
        self.load_quizzes()  # 시작할 때 파일에서 퀴즈 불러오기

    def add_quiz(self):
        print("\n--- ➕ 새 퀴즈 추가 ---")
        question = input("문제 내용을 입력하세요: ")
        answer = input("정답을 입력하세요: ")
        new_quiz = Quiz(question, answer)
        self.quizzes.append(new_quiz)
        self.save_quizzes()  # 추가하자마자 파일에 저장
        print("✅ 퀴즈가 성공적으로 추가되었습니다!")

    def save_quizzes(self):
        # 퀴즈 객체들을 딕셔너리 형태로 변환해서 저장
        data = [{"question": q.question, "answer": q.answer} for q in self.quizzes]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_quizzes(self):
        # 파일이 존재하는지 확인하고 불러오기
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = [Quiz(d["question"], d["answer"]) for d in data]
        else:
            # 파일이 없으면 기본 문제 세팅
            self.quizzes = [
                Quiz("대한민국의 수도는 어디인가요?", "서울"),
                Quiz("파이썬을 만든 사람은 누구인가요?", "귀도 반 로섬")
            ]

    def play_quiz(self):
        print("\n--- 🎮 퀴즈 시작! ---")
        score = 0
        for q in self.quizzes:
            print(f"문제: {q.question}")
            user_answer = input("정답: ")
            if user_answer.strip() == q.answer:
                print("⭕ 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 '{q.answer}'입니다.")
        
        print(f"\n결과: {len(self.quizzes)}문제 중 {score}문제를 맞혔습니다!")

    def show_menu(self):
        while True:
            print("\n--- 📝 퀴즈 프로그램 메뉴 ---")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가하기")
            print("3. 종료하기")
            choice = input("원하는 작업 번호를 입력하세요: ")

            if choice == "1":
                self.play_quiz()
            elif choice == "2":
                self.add_quiz()
            elif choice == "3":
                print("프로그램을 종료합니다. 안녕히 가세요!")
                break
            else:
                print("잘못된 입력입니다. 1~3번 중 선택해주세요.")

if __name__ == "__main__":
    game = QuizGame()
    game.show_menu()
    
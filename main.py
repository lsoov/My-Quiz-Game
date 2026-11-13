class Quiz:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class QuizGame:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
# --- [추가 1] 새로운 문제를 추가하는 기능 ---
    def add_question(self):
        print("\n➕ 새로운 퀴즈를 추가합니다.")
        question = input("문제 내용을 입력하세요: ")
        answer = input("정답을 입력하세요: ")
        self.questions.append(Quiz(question, answer))
        print("✅ 문제가 성공적으로 추가되었습니다!")

    # --- [수정 1] 기존의 run을 play_game으로 이름만 바꿨어요 ---
    def play_game(self):
        if not self.questions:
            print("\n❌ 풀 수 있는 문제가 없습니다. 문제를 먼저 추가해주세요!")
            return

        print("\n🎮 퀴즈 게임을 시작합니다!")
        self.score = 0  # 게임 시작할 때 점수 초기화
        for q in self.questions:
            user_answer = input(f"\n❓ 질문: {q.question}\n정답 입력: ")
            if user_answer == q.answer:
                print("✅ 정답입니다!")
                self.score += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 '{q.answer}'입니다.")
        
        print(f"\n🏁 게임 종료! 최종 점수: {self.score}/{len(self.questions)}")

    # --- [추가 2] 프로그램의 중심이 되는 메뉴 기능 ---
    def run(self):
        while True:
            print("\n--- 📝 퀴즈 프로그램 메뉴 ---")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가하기")
            print("3. 종료하기")
            choice = input("원하는 작업 번호를 입력하세요: ")

            if choice == "1":
                self.play_game()
            elif choice == "2":
                self.add_question()
            elif choice == "3":
                print("👋 프로그램을 종료합니다. 다음에 또 봐요!")
                break
            else:
                print("⚠️ 잘못된 입력입니다. 1~3번 중에서 골라주세요.")

    

# 퀴즈 데이터
question_list = [
    Quiz("대한민국의 수도는 어디인가요?", "서울"),
    Quiz("파이썬의 창시자는 누구인가요?", "귀도 반 로섬")
]

# 게임 실행
if __name__ == "__main__":
    game = QuizGame(question_list)
    game.run()


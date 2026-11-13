class Quiz:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class QuizGame:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0

    def run(self):
        print("🎮 퀴즈 게임을 시작합니다!")
        # 1. 리스트에 있는 문제를 하나씩 꺼내기
        for q in self.questions:
         # 2. 사용자에게 질문하고 답 입력받기
            user_answer = input(f"\n❓ 질문: {q.question}\n정답 입력: ")
            
        # 3. 정답 확인하기
            if user_answer == q.answer:
                print("✅ 정답입니다!")
                self.score += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 '{q.answer}'입니다.")
        
         # 4. 최종 점수 보여주기
        print(f"\n🏁 게임 종료! 당신의 최종 점수는 {self.score}/{len(self.questions)}입니다.")
        print("게임이 종료되었습니다.")

# 퀴즈 데이터
question_list = [
    Quiz("대한민국의 수도는 어디인가요?", "서울"),
    Quiz("파이썬의 창시자는 누구인가요?", "귀도 반 로섬")
]

# 게임 실행
if __name__ == "__main__":
    game = QuizGame(question_list)
    game.run()


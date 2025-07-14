import json
import os

# 파일 이름 설정
STATE_FILE = "simulation_state.json"

# 사전 정의된 업무 목록 (공부 유형)
TASKS = {
    "T1": {"name": "Python 기초 공부", "difficulty": 2, "points_per_chapter": 10, "chapters_completed": 0},
    "T2": {"name": "열역학 복습 및 과제", "difficulty": 2, "points_per_chapter": 10, "chapters_completed": 0},
    "T3": {"name": "공업수학 복습 및 문제풀이", "difficulty": 2, "points_per_chapter": 10, "chapters_completed": 0},
    "T4": {"name": "기계설계 복습", "difficulty": 3, "points_per_chapter": 15, "chapters_completed": 0},
    "T5": {"name": "열전달 복습 및 노트정리", "difficulty": 3, "points_per_chapter": 15, "chapters_completed": 0},
    "T6": {"name": "동역학 복습 및 노트정리", "difficulty": 3.5, "points_per_chapter": 18, "chapters_completed": 0},
    "T7": {"name": "유튜브 연구 동향/공학 영상 시청", "difficulty": 1, "points_per_chapter": 5, "chapters_completed": 0},
    "T8": {"name": "ROS 기초 공부", "difficulty": 2, "points_per_chapter": 10, "chapters_completed": 0},
    "T9": {"name": "만화로 배우는 한 권 완독", "difficulty": 3.5, "points_per_chapter": 60, "chapters_completed": 0},
    "T10": {"name": "스스로 공부", "difficulty": 2, "points_per_chapter": 120, "chapters_completed": 0}
}

# 사전 정의된 보상 목록 (공부 유형)
REWARDS = {
    "R1": {"description": "그림 그리기 (30분)", "cost": 10},
    "R2": {"description": "스트레칭 브레이크 (10분)", "cost": 5},
    "R3": {"description": "게임 (30분)", "cost": 10},
    "R4": {"description": "유튜브 시청 (30분)", "cost": 10},
    "R5": {"description": "넷플릭스 감상 (1시간)", "cost": 15},
    "R6": {"description": "PC방 2시간 이용", "cost": 25},
    "R7": {"description": "영화관에서 영화 한 편 보기", "cost": 30},
    "R8": {"description": "일러스트 감상 (30분)", "cost": 5},
    "R9": {"description": "맛집탐방(3.0내외)", "cost": 80},
    "R10": {"description": "코스 요리 레스토랑(7.0내외)", "cost": 180}
}

class Simulation:
    def __init__(self):
        # 초기 포인트 및 업무 상태 설정
        self.points = 0
        self.tasks = {tid: info.copy() for tid, info in TASKS.items()}
        self.rewards = REWARDS.copy()
        self.load_state()

    def load_state(self):
        """이전 저장된 상태가 있으면 불러옵니다."""
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
                self.points = state.get("points", 0)
                for task_id, task_state in state.get("tasks", {}).items():
                    if task_id in self.tasks:
                        self.tasks[task_id]["chapters_completed"] = task_state.get("chapters_completed", 0)

    def save_state(self):
        """현재 상태를 파일에 저장합니다."""
        state = {
            "points": self.points,
            "tasks": {
                task_id: {"chapters_completed": info["chapters_completed"]}
                for task_id, info in self.tasks.items()
            }
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def complete_chapter(self, task_id):
        """단원 완료 시 포인트를 부여하고 상태를 저장합니다."""
        if task_id not in self.tasks:
            return f"❌ 잘못된 업무 ID입니다: {task_id}"
        task = self.tasks[task_id]
        task["chapters_completed"] += 1
        points_gained = task["points_per_chapter"]
        self.points += points_gained
        self.save_state()
        return (
            f"✅ [{task_id}] {task['name']} 단원 완료!\n"
            f"획득 포인트: {points_gained}P\n"
            f"현재 누적 포인트: {self.points}P"
        )

    def redeem_reward(self, reward_id):
        """보상을 교환할 때 포인트를 차감하고 상태를 저장합니다."""
        if reward_id not in self.rewards:
            return f"❌ 잘못된 보상 ID입니다: {reward_id}"
        reward = self.rewards[reward_id]
        cost = reward["cost"]
        if self.points < cost:
            return f"❌ 포인트 부족: 현재 {self.points}P, 필요 {cost}P"
        self.points -= cost
        self.save_state()
        return (
            f"🎁 [{reward_id}] {reward['description']} 교환 완료!\n"
            f"차감 포인트: {cost}P\n"
            f"남은 포인트: {self.points}P"
        )

    def show_status(self):
        """현재 포인트와 업무 완료 상태 및 보상 목록을 문자열로 반환합니다."""
        lines = [f"📊 현재 누적 포인트: {self.points}P\n"]
        lines.append("📚 업무 상태:")
        for task_id, task in self.tasks.items():
            completed = task["chapters_completed"]
            if completed == 0:
                status = "완료한 단원 없음"
            else:
                status = f"완료한 단원: {completed}"
            lines.append(f" - {task_id}: {task['name']} — {status}")
        lines.append("\n🎁 보상 목록:")
        for reward_id, reward in self.rewards.items():
            lines.append(f" - {reward_id}: {reward['description']} — {reward['cost']}P")
        return "\n".join(lines)

    def reset(self):
        """모든 업무 완료 상태와 포인트를 초기화하고 저장 파일을 삭제합니다."""
        self.points = 0
        for task in self.tasks.values():
            task["chapters_completed"] = 0
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
        return "모든 상태가 초기화되었습니다."

if __name__ == "__main__":
    sim = Simulation()
    print(">>> 공부 시뮬레이션에 오신 것을 환영합니다!")
    print("명령어: complete_chapter [T번호], redeem_reward [R번호], show_status, reset, exit")
    while True:
        cmd_line = input("\n입력> ").strip().split()
        if not cmd_line:
            continue
        cmd = cmd_line[0]
        if cmd == "exit":
            print("시뮬레이션을 종료합니다.")
            break
        elif cmd == "show_status":
            print(sim.show_status())
        elif cmd == "reset":
            print(sim.reset())
        elif cmd == "complete_chapter" and len(cmd_line) == 2:
            print(sim.complete_chapter(cmd_line[1]))
        elif cmd == "redeem_reward" and len(cmd_line) == 2:
            print(sim.redeem_reward(cmd_line[1]))
        else:
            print("❌ 잘못된 명령어입니다. 다시 시도해 주세요.")

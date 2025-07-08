import json
import os

# JSON 저장 파일명
SAVE_FILE = "stock_sim_state.json"

# 업무 목록 (업무 ID, 이름, 포인트)
tasks = {
    "T1": {"name": "시황분석 영상 시청 (1시간)", "points": 2},
    "T2": {"name": "매매일지 작성", "points": 2},
    "T3": {"name": "특정 기업 실적 발표 분석", "points": 3},
    "T4": {"name": "특정 기업 10-K 문서 분석", "points": 10},
    "T5": {"name": "블로그에 분석글 작성", "points": 7},
    "T6": {"name": "13F 공시 분석", "points": 5},
    "T7": {"name": "하루 장 마감 요약 작성", "points": 3},
    "T8": {"name": "주간 장 요약 + 다음주 워치리스트", "points": 7}
}

# 보상 카탈로그 (보상 ID, 설명, 필요 포인트)
rewards = {
    "R1": {"desc": "레스토랑 가기 (약 3만원)", "cost": 30},
    "R2": {"desc": "마사지샵 방문 (약 7만원)", "cost": 70},
    "R3": {"desc": "여행 가기", "cost": 300},
}

# 초기 상태
state = {
    "total_points": 0
}

# 상태 저장
def save_state():
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

# 상태 불러오기
def load_state():
    global state
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            state = json.load(f)

# 업무 완료
def complete_task(tid):
    if tid not in tasks:
        print("❌ 존재하지 않는 업무 ID입니다.")
        return
    state["total_points"] += tasks[tid]["points"]
    print(f"✅ '{tasks[tid]['name']}' 완료! +{tasks[tid]['points']}P")
    save_state()

# 보상 사용
def redeem_reward(rid):
    if rid not in rewards:
        print("❌ 존재하지 않는 보상 ID입니다.")
        return
    cost = rewards[rid]["cost"]
    if state["total_points"] < cost:
        print(f"❌ 포인트 부족: {cost}P 필요, 현재 {state['total_points']}P 보유")
        return
    state["total_points"] -= cost
    print(f"🎉 '{rewards[rid]['desc']}' 보상을 사용했습니다! -{cost}P")
    save_state()

# 상태 출력
def show_status():
    print(f"\n📊 누적 포인트: {state['total_points']}P")
    print("\n📝 업무 목록:")
    for tid, task in tasks.items():
        print(f"  {tid}: {task['name']} ({task['points']}P)")
    print("\n🎁 보상 카탈로그:")
    for rid, reward in rewards.items():
        print(f"  {rid}: {reward['desc']} - {reward['cost']}P")
    print()

# 메인 루프
def main():
    load_state()
    print("📈 주식 분석 시뮬레이션 시작!")
    print("명령어 예시: complete T1 / redeem R1 / show_status / exit")

    while True:
        cmd = input("\n명령어를 입력하세요: ").strip().split()
        if not cmd:
            continue
        action = cmd[0]

        if action == "complete" and len(cmd) == 2:
            complete_task(cmd[1])
        elif action == "redeem" and len(cmd) == 2:
            redeem_reward(cmd[1])
        elif action == "show_status":
            show_status()
        elif action == "exit":
            print("👋 시뮬레이션 종료. 수고하셨어요!")
            break
        else:
            print("❓ 알 수 없는 명령어입니다.")

if __name__ == "__main__":
    main()

import json
import os

DATA_FILE = 'data.json'

tasks = {
    "T1": {"name": "요일별 운동 풀 루틴", "points": 4},
    "T2": {"name": "요일별 운동 절반", "points": 2},
    "T3": {"name": "운동 전후 스트레칭", "points": 1},
    "T4": {"name": "취침 전 스트레칭", "points": 1},
    "T5": {"name": "운동방법 유튜브 시청", "points": 1},
    "T6": {"name": "패션 유튜브 시청", "points": 1},
    "T7": {"name": "연속 날짜 초기화", "points": 0}
}

rewards = {
    "R1": {"desc": "베스킨라빈스 아이스크림", "cost": 20},
    "R2": {"desc": "원하는 음료 마시기", "cost": 12},
    "R3": {"desc": "맛집 1회 방문", "cost": 40},
    "R4": {"desc": "칵테일 바 다녀오기", "cost": 120},
    "R5": {"desc": "마사지 받고 오기", "cost": 280}
}

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"points": 0, "streak_T1": 0, "last_T1_success": False}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def show_status(data):
    print(f"\n📊 현재 포인트: {data['points']}P")
    print(f"🔥 T1 연속 성공일: {data['streak_T1']}일\n")

def complete_tasks(data):
    print("\n오늘 완료한 업무 ID를 쉼표로 입력하세요 (예: T1,T3,T5):")
    task_input = input(">> ").replace(" ", "").upper()
    task_ids = task_input.split(',')

    earned = 0
    t1_done = False

    for tid in task_ids:
        if tid in tasks:
            point = tasks[tid]['points']
            print(f"✅ {tasks[tid]['name']} 완료: +{point}P")
            earned += point
            if tid == "T1":
                t1_done = True
        else:
            print(f"❌ 알 수 없는 업무 ID: {tid}")

    # 연속 성공 체크
    if t1_done:
        if data["last_T1_success"]:
            data["streak_T1"] += 1
        else:
            data["streak_T1"] = 1
        data["last_T1_success"] = True

        # 보너스 포인트
        if data["streak_T1"] == 2:
            print("🎉 2일 연속 T1 성공! +2P 보너스!")
            earned += 2
        elif data["streak_T1"] == 3:
            print("🔥 3일 연속 T1 성공! +3P 보너스!")
            earned += 3
        elif data["streak_T1"] == 4:
            print("🏆 4일 연속 T1 성공! +5P 보너스!")
            earned += 5
        elif data["streak_T1"] == 5:
            print("💥 5일 연속 T1 성공! +7P 보너스!")
            earned += 7
        elif data["streak_T1"] == 6:
            print("🚀 6일 연속 T1 성공! +9P 보너스!")
            earned += 9
        elif data["streak_T1"] == 7:
            print("👑 7일 연속 T1 성공! +12P 보너스! (연속 초기화)")
            earned += 12
            data["streak_T1"] = 0
    else:
        data["last_T1_success"] = False
        data["streak_T1"] = 0

    data["points"] += earned
    print(f"\n📈 오늘 획득 포인트: +{earned}P")
    print(f"💰 총 누적 포인트: {data['points']}P\n")

def use_reward(data):
    print("\n사용 가능한 보상 목록:")
    for rid, info in rewards.items():
        print(f"- {rid}: {info['desc']} (필요: {info['cost']}P)")

    choice = input("\n받을 보상 ID를 입력하세요: ").upper()
    if choice in rewards:
        cost = rewards[choice]['cost']
        if data['points'] >= cost:
            data['points'] -= cost
            print(f"🎁 '{rewards[choice]['desc']}' 보상을 받았습니다! (-{cost}P)")
            print(f"💳 남은 포인트: {data['points']}P\n")
        else:
            print("❗ 포인트가 부족합니다.\n")
    else:
        print("❗ 존재하지 않는 보상 ID입니다.\n")

def main():
    data = load_data()

    while True:
        print("\n=== 운동 시뮬레이션 메뉴 ===")
        print("1. 오늘의 업무 완료 입력")
        print("2. 현재 상태 확인")
        print("3. 보상 사용")
        print("4. 종료 (저장)")

        choice = input("메뉴 선택 (1-4): ")
        if choice == '1':
            complete_tasks(data)
            save_data(data)
        elif choice == '2':
            show_status(data)
        elif choice == '3':
            use_reward(data)
            save_data(data)
        elif choice == '4':
            save_data(data)
            print("📁 저장 후 종료합니다. 내일도 힘내요!")
            break
        else:
            print("❌ 잘못된 입력입니다.\n")

if __name__ == '__main__':
    main()

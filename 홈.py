import os
import time
print("WANDU_TIPING_GAME━━━━━━━━━━━━━━━━━━━━━━━━Test.Ver") #36줄
print("📢공지사항━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("Test ver. 1.0의 새소식━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("'완두 타이핑 게임'에 오신 것을 환영합니다.")
print("이제 여기에 업데이트 소식이 실릴 것입니다.")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print('게임을 시작하시려면 "start"를 입력하세요.')
startMSG = input(">>")
if startMSG == "start":
    print("5초 후 게임이 시작됩니다.")
    time.sleep(1)
    print("4초 후 게임이 시작됩니다.")
    time.sleep(1)
    print("3초 후 게임이 시작됩니다.")
    time.sleep(1)
    print("2초 후 게임이 시작됩니다.")
    time.sleep(1)
    print("1초 후 게임이 시작됩니다.")
    time.sleep(1)
    print("게임이 시작됩니다.")
    My_See_Card = 1
    My_BeMil_Card = 4
    Sangde_see_card = 3
    sangde_bemil_card = 5
    My_CaraMell = 20
    print("당신이 선공입니다.")
    print("나의 이마카드 : ?")
    print("나의 히든카드 : ?")
    print("상대의 이마카드 : " + str(Sangde_see_card))
    print("상대의 히든카드 : ?")
    print("몇개을 베팅하시겠습니까?")
    print("현재 나의 카라멜 수 : " + str(My_CaraMell))
    betingGab = input(">>")
    print("나의 베팅이 끝났습니다.")
    print("상대가 베팅 중입니다...")
    time.sleep(13.23)
    print("상대가 베팅이 끝났습니다.")
    print("이제 결과를 발표합니다.")
    time.sleep(2)
    print("이번 라운드의 승자는...")
    time.sleep(4.5)
    if (My_See_Card + My_BeMil_Card) > (sangde_bemil_card + Sangde_see_card):
        print("당신입니다!")
        print("축하드립니다.")
        print("당신의 카라멜 숫자 : ")
    #else랑 상대베팅값, 그리고 반복문도 해야됨
    #최종수정일 : 2024.1.5 11:18


import threading
import argparse, sys

from concurrent.futures import ThreadPoolExecutor
import logging
import queue
import time

import grpc
import command
import command_pb2_grpc

game_session_lock = threading.Lock()
game_session = ""
under_game = False

def setup_game_session(session, status):
    global game_session_lock
    global game_session
    global under_game
    game_session_lock.acquire()
    game_session = session
    under_game = status
    game_session_lock.release()

class ChatMaker:
    def __init__(
        self,
        executor: ThreadPoolExecutor,
        channel: grpc.Channel,
        name,
    ) -> None:
        self._executor = executor
        self._channel = channel
        self._stub = command_pb2_grpc.DukongGSStub(self._channel)
        self._session_id = None
        self._consumer_future = None
        self._send_queue = queue.SimpleQueue()
        self._player = name

    def resp_watcher(self, response_iterator) -> None:
        logging.info("resp_watcher start")
        try:
            while True:
                response = next(response_iterator)
                logging.info("수신 값 : [%s]:[%s]", response.name, response.message)
        except Exception as e:
            raise

    def start(self) -> None:
        logging.info("start")
        response_iterator = self._stub.Chat(iter(self._send_queue.get, None))
        # Instead of consuming the response on current thread, spawn a consumption thread.
        self._consumer_future = self._executor.submit(
            self.resp_watcher, response_iterator
        )

        # start chat
        request = command_pb2.ChatMessage(name=self._player, message="start")
        self._send_queue.put(request)

        global under_game
        global game_session

        while True:
            msg = input(": ")
            if under_game == True:
                request = command_pb2.StopGameRequest(name=self._player, session=game_session, content=msg)
                resp = self._stub.StopGame(request, None)
                if resp.success != True:
                    logging.info("값이 일치하지 않습니다. 이유 : (%s)", resp.message)
                    continue
                # winner
                logging.info("WIN!ㅡㅡ게임을 이겼습니다. 축하합니다!")
                setup_game_session("", False)
                continue

            if (under_game != True) and (msg == "start game"):
                request = command_pb2.StartGameRequest(name=self._player, gameType="typing")
                resp = self._stub.StartGame(request, None)
                if resp.success != True:
                    logging.info("에러 : 게임 시작을 실패했습니다. 이유 : (%s)", resp.message)
                    continue

                setup_game_session(resp.session, True)
                logging.info("게임 시작을 성공했습니다. 세션 : (%s)", game_session)
                continue

            if under_game == False:
                request = command_pb2.ChatMessage(name=self._player, message=msg)
                self._send_queue.put(request)
                time.sleep(0.1)


def process_login(stub, name):
    logging.info("process_login start /w (%s)", name)
    request = command_pb2.LoginRequest(name=name)
    response_iterator = stub.Login(request, None)
    for response in response_iterator:
        logging.info("DukongGS: (%s)", response.content)
        if response.content == "game started":
            logging.info("(%s) 게임이 시작되었습니다. - 세션 : (%s)", response.gameType, response.session)
            setup_game_session(response.session, True)
        elif response.content == "game cleared":
            logging.info("(%s) 게임이 끝났습니다. 세션 : (%s)", response.gameType, response.session)
            setup_game_session(response.session, False)


def process_chat(
    executor: ThreadPoolExecutor, channel: grpc.Channel, name
) -> None:
    chat = ChatMaker(executor, channel, name)
    chat.start()


def run(playername, addr):
    print(f'서버 주소 : ', addr)
    print(f'플레이어 이름 : ', playername)
    executor = ThreadPoolExecutor()
    with grpc.insecure_channel(addr) as channel:
        future1 = executor.submit(
            process_chat, executor, channel, playername
        )
        future2 = executor.submit(
            process_login, command_pb2_grpc.DukongGSStub(channel), playername
        )
        future1.result()
        future2.result()


if __name__ == '__main__':
    print("WANDU_TIPING_GAME━━━━━━━━━━━━━━━━━━━━━━━━Test.Ver")
    print("📢공지사항━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Test ver. 1.0의 새소식━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("'완두 타이핑 게임'에 오신 것을 환영합니다.")
    print("이제 여기에 업데이트 소식이 실릴 것입니다.")
    print("🧾명령어 리스트━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("startgame : 게임 시작 (타이핑 게임)")
    print("[/(>n<)\; 열심히 개발중..! ━━━━━━━━━━━ 추후 추가 예정]")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    logging.basicConfig(level=logging.INFO)
    playername = input("사용자 이름 >>")
    run(playername, "127.0.0.1:50051")
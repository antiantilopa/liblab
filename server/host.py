import socket, threading, time, ipaddress

from logic.vmath import Vector2d, from_bytes, to_bytes
from logic.game import Game
from logic.cell import Cell, CellType
from logic.objects import WORLD_SIZE
from random import randint as rd


class Host:
    playerNumber: int
    sock: socket.socket
    connections: list[socket.socket]
    game: Game
    PlayersneedUpdate: int

    def __init__(self, playerNumber: int = 1) -> None:
        self.playerNumber = playerNumber
        self.PlayersneedUpdate = 2**playerNumber - 1
    
    def initSockets(self) -> list:
        self.sock = socket.socket()
        self.connections = []
        self.recvthreads: list[threading.Thread] = []
        self.recvthreads_results: list[bytes] = [None] * self.playerNumber
        self.sendthreads: list[threading.Thread] = [] 
        hostname = socket.gethostname()
        IPaddr = socket.gethostbyname(hostname)
        if not self.validate_ip(IPaddr):
            print(f"IP address {IPaddr} is not valid.")
            IPaddr = input("Enter a valid IP address: ")
        
        try:
            self.sock.bind((IPaddr, 9090))
            self.sock.listen(self.playerNumber)
        except socket.error as e:
            print(f"Socket error: {e}")
            return []
        for i in range(self.playerNumber):
            conn, _ = self.sock.accept()
            conn.send(to_bytes(i))
            self.connections.append(conn)
        for i in range(self.playerNumber):
            self.recvthreads.append(threading.Thread(target=self.recvData, args=[i]))
            self.recvthreads[i].start()
        for conn in self.connections:
            conn.send(b"game started!")
    
    def validate_ip(self, ip: str) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def initGame(self) -> None:
        self.game = Game()
        for rtype in range(4):
            for i in range(20 - rtype*5):
                self.game.add_obj(rtype, Vector2d(rd((rtype) * 500, WORLD_SIZE.x - (rtype) * 500), rd((rtype) * 500, WORLD_SIZE.y - (rtype) * 500)))
        for _ in range(self.playerNumber):
            self.game.add_player()
        self.game.players[0].add_cell(Cell.correct_init(CellType.CELLTYPES[0], Vector2d(200, 200), 0))
        self.game.players[0].add_cell(Cell.correct_init(CellType.CELLTYPES[4], Vector2d(300, 300), 0))
        self.game.players[0].add_cell(Cell.correct_init(CellType.CELLTYPES[8], Vector2d(300, 300), 0))
        self.game.players[1].add_cell(Cell.correct_init(CellType.CELLTYPES[0], Vector2d(800, 800), 1))
        self.game.players[1].add_cell(Cell.correct_init(CellType.CELLTYPES[4], Vector2d(800, 700), 1))
        self.game.players[1].add_cell(Cell.correct_init(CellType.CELLTYPES[8], Vector2d(700, 700), 1))

    # Send data to player and wait untill getting verification that he recieved it
    def sendData(self, playerIndex: int) -> None:
        a = self.game.getPlayerData()
        self.connections[playerIndex].send(bytes(a))

    # Wait untill getting data from player and then write it in recvthreads_results
    def recvData(self, playerIndex: int) -> None:
        data = self.connections[playerIndex].recv(1024)
        self.recvthreads_results[playerIndex] = data
        # programm stops waiting for recv()
        # that is why threading is used

    def playersControl(self):
        for i in range(self.playerNumber):
            if not self.recvthreads[i].is_alive():
                # TODO do something with self.recvthreads_results[i] in game
                # The thing here is just test version
                gotten = from_bytes(self.recvthreads_results[i])
                if len(gotten) != 0:
                    for data in gotten[0]:
                        for cell in self.game.players[i].cells:
                            if cell.id == data[0]:
                                cell.new_target(Vector2d.from_tuple(data[1]))
                    for data in gotten[1]:
                        # print(data)
                        for cell in self.game.players[i].cells:
                            if cell.id == data[0]:
                                if data[1] < 4:
                                    cell.burn_resource({data[1] : 1})
                                else:
                                    cell.start_production(data[1] - 4)
                self.sendData(i)
                self.recvthreads[i] = threading.Thread(target=self.recvData, args=[i])
                self.recvthreads[i].start()
    
    def iteration(self) -> None:
        start_time = time.time()
        self.game.iteration() 
        self.playersControl()
        end_time = time.time()
        time.sleep(max(0.016 - (end_time - start_time), 0))
        
    def close(self):
        for conn in self.connections:
            conn.close()
        for thread in self.recvthreads:
            thread.join()
        self.sock.close()
        exit()


if __name__ == "__main__":
    a = Host(2)
    a.initGame()
    a.initSockets()
    while True:
        a.iteration()




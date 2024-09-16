import socket, pygame
from fuckin_engine.vmath_mini import Vector2d, from_bytes, to_bytes, print_bytes

sock = socket.socket()

hostname = socket.gethostname()
IPaddr = socket.gethostbyname(hostname)

sock.connect((IPaddr, 9090))
pl = from_bytes(sock.recv(1024))
print(pl)


message = sock.recv(1024).decode()
print(message)


WORLD_SIZE = Vector2d(20000, 20000)
camera = Vector2d(pl*600, pl*600)


data = []

selected = []
info = -1
buttons = [] 
# button [[pos: Vector, size: Vector, color, text]]
group_selected = -1

owner_colors = [
    (0, 255, 0), 
    (255, 0, 0),
    (0, 0, 255)
]

class Obj_Type:
    ALL: list["Obj_Type"] = []
    def __init__(self, name: str, radius_mass: int, color: tuple[int, int, int]) -> None:
        self.name = name
        self.radius_mass = radius_mass
        self.color = color
        Obj_Type.ALL.append(self)
class Obj_types:
    A = Obj_Type("A", 1, (0, 200, 0))
    B = Obj_Type("B", 0.5, (250, 200, 40))
    C = Obj_Type("C", 0.3, (60, 100, 220))
    D = Obj_Type("D", 0.7, (250, 20, 20))

class Cell_Type:
    ALL: list["Cell_Type"] = []
    def __init__(self, name: str, radius:int, color: tuple[int, int, int], cost: tuple[int, int, int, int, int], produce = (), initial_energy = 0):
        self.name = name
        self.radius = radius
        self.color = color
        self.cost = cost
        self.produce = produce
        self.initial_energy = initial_energy
        Cell_Type.ALL.append(self)

class Cell_Types:
    Amother = Cell_Type("A mother", 50,  (0, 120, 0),   (20, 20, 0, 0, 0), (4, 8, 0, 1))
    Bmother = Cell_Type("B mother", 75,  (200, 200, 0), (30, 20, 0, 0, 0), (5, 9, 0, 1, 2))
    Cmother = Cell_Type("C mother", 100, (0, 0, 200),   (40, 0, 20, 0, 0), (6, 10, 0, 1, 2, 3))
    Dmother = Cell_Type("D mother", 125, (200, 0 , 0),  (50, 0, 0, 20, 0), (7, 11 ,0, 1, 2, 3))

    Acollector = Cell_Type("A collector", 20, (120, 250, 120), (10, 0, 0, 0, 0), initial_energy = 3)
    Bcollector = Cell_Type("B collector", 20, (250, 220, 120), (15, 2, 0, 0, 0), initial_energy = 5)
    Ccollector = Cell_Type("C collector", 20, (120, 150, 250), (20, 0, 2, 0, 0), initial_energy = 7)
    Dcollector = Cell_Type("D collector", 20, (250, 120, 120), (25, 0, 0, 2, 0), initial_energy = 9)

    Adigester = Cell_Type("A digester", 25, (0, 60, 0),  (15, 5, 0, 0, 0), initial_energy = 1)
    Bdigester = Cell_Type("B digester", 25, (30, 40, 0), (25, 0, 5, 0, 0), initial_energy = 2)
    Cdigester = Cell_Type("C digester", 25, (0, 0, 60),  (35, 0, 0, 5, 0), initial_energy = 3)
    Ddigester = Cell_Type("D digester", 25, (60, 0, 0),  (45, 0, 0, 0, 5), initial_energy = 4)



def draw_obj(screen:pygame.Surface, typee:int, pos: Vector2d, mass:int):
    radius = Obj_Type.ALL[typee].radius_mass * mass
    color = Obj_Type.ALL[typee].color
    pygame.draw.circle(screen, color, (pos - camera).as_tuple(), radius)

def draw_cell(screen:pygame.Surface, typee:int, pos:Vector2d, owner: int, is_sellected:bool, energy: int = 0):
    color = Cell_Type.ALL[typee].color
    radius = Cell_Type.ALL[typee].radius
    color_around = (0, 0, 0)
    if is_sellected:
        color_around = (255, 255, 0)
    pygame.draw.circle(screen, owner_colors[owner], (pos - camera).as_tuple(), radius + 5)
    pygame.draw.circle(screen, color_around, (pos - camera).as_tuple(), radius + 2)
    pygame.draw.circle(screen, color, (pos - camera).as_tuple(), radius)
    if typee >= 4:
        start_pos = pos + Vector2d(-radius, -radius) - camera
        middle_pos = pos + Vector2d((radius * 2 * energy) // Cell_Type.ALL[typee].initial_energy - radius, -radius) - camera
        end_pos = pos + Vector2d(radius, -radius) - camera

        pygame.draw.line(screen, (250, 250, 20), start_pos.as_tuple(), middle_pos.as_tuple(), width = 5)
        pygame.draw.line(screen, (250, 0, 0), middle_pos.as_tuple(), end_pos.as_tuple(), width = 5)

def info_obj(screen:pygame.Surface, font: pygame.font.Font, typee:int, pos: tuple[float, float], mass: int):
    radius = Obj_Type.ALL[typee].radius_mass * mass
    color = Obj_Type.ALL[typee].color
    pygame.draw.circle(screen, color, (h//10, h//10), h//12)
    texts = []
    texts.append(font.render(Obj_Type.ALL[typee].name + " resource", 0, (200, 20, 20)))
    texts.append(font.render(f"mass = {mass}", 0, (200, 20, 20)))
    texts.append(font.render(f"radius = {radius}", 0, (200, 20, 20)))
    texts.append(font.render(f"x coord = {pos[0]}", 0, (200, 20, 20)))
    texts.append(font.render(f"y coord = {pos[1]}", 0, (200, 20, 20)))

    for i in range(len(texts)):
        screen.blit(texts[i], (0, h//5 + i * font.get_height()))

def info_cell(screen:pygame.Surface, font: pygame.font.Font, typee:int, pos: tuple[float, float], mass: int, energy:int, owner:int, args:list = []):
    global buttons
    radius = Cell_Type.ALL[typee].radius
    color = Cell_Type.ALL[typee].color
    pygame.draw.circle(screen, owner_colors[owner], (h//10, h//10), h//10)
    pygame.draw.circle(screen, (0, 0, 0), (h//10, h//10), h//11)
    pygame.draw.circle(screen, color, (h//10, h//10), h//12)
    texts = []
    texts.append(font.render(Cell_Type.ALL[typee].name + " cell", 0, (200, 20, 20)))
    texts.append(font.render(f"mass = {mass}", 0, (200, 20, 20)))
    texts.append(font.render(f"radius = {radius}", 0, (200, 20, 20)))
    texts.append(font.render(f"x coord = {pos[0]}", 0, (200, 20, 20)))
    texts.append(font.render(f"y coord = {pos[1]}", 0, (200, 20, 20)))
    texts.append(font.render(f"owner = {owner}", 0, (200, 20, 20)))
    if len(args) == 0:
        texts.append(font.render(f"energy = {energy}", 0, (250, 250, 20)))
        buttons = []
    elif len(args) == 1:
        texts.append(font.render(f"energy = {energy}", 0, (250, 250, 20)))
        texts.append(font.render("load: ", 0, (200, 20, 20)))
        for r in (0, 1, 2, 3):
            texts.append(font.render(f"  {"ABCD"[r]} resources = {args[0][r]}", 0, Obj_Type.ALL[r].color))
        buttons = []
    elif len(args) == 3:
        texts.append(font.render("ready to use: ", 0, (200, 20, 20)))
        texts.append(font.render(f"  energy = {energy}", 0, (250, 250, 20)))
        for r in (0, 1, 2, 3):
            texts.append(font.render(f"  {"ABCD"[r]} resources = {args[0][r]}", 0, Obj_Type.ALL[r].color))
        
        if args[1] != -1:
            texts.append(font.render("producing: ", 0, (200, 20, 20)))
            texts.append(font.render(f"  {Cell_Type.ALL[args[1]].name}", 0, Cell_Type.ALL[args[1]].color))
            texts.append(font.render(f"  ticks left = {args[2]}", 0, (200, 20, 20)))
        
        buttons = []
        for r in (0, 1, 2, 3):
            buttons.append((Vector2d(r * h // 16, len(texts) * font.get_height() + h//4), Vector2d(w // 16, h // 16), Obj_Type.ALL[r].color, "BURN", (0, 0, 0), r))
        for r in range(len(Cell_Type.ALL[typee].produce)):
            ctype = Cell_Type.ALL[typee].produce[r]
            buttons.append((Vector2d(0, len(texts) * font.get_height() + h//4 + h//16 + r * (h//16)), Vector2d(w//4, h//16), Cell_Type.ALL[ctype].color, Cell_Type.ALL[ctype].name, (0, 0, 0), ctype + 4))
        

    for i in range(len(texts)):
        screen.blit(texts[i], (0, h//4 + i * font.get_height()))
    
    for button in buttons:
        pygame.draw.rect(screen, button[2], (button[0].x, button[0].y, button[1].x, button[1].y))
        text = font.render(button[3], 0, button[4])
        screen.blit(text, (button[0].x, button[0].y + (button[1].y - font.get_height())//2))

pygame.init()
pygame.font.init()
pygame.display.set_caption(f"liblab {pl}")
w, h = pygame.display.get_desktop_sizes()[0]
camera_speed = 5 * h // 500
# w = 500
# h = 500

font = pygame.font.SysFont("consolas", 12 * h // 500)
screen=pygame.display.set_mode((w, h))


active_zone = pygame.Surface((w - w//4, h))
info_zone = pygame.Surface((w//4, h))

shift_down = False
send_info = []
mouse_down = False
mouse_down_point = Vector2d(0, 0)

while True:
    send_info = [[], []]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sock.close()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                shift_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                shift_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[0] <= w - w//4:
                    hit = False
                    if not shift_down:
                        selected = []
                    for obj in data[0]:
                        typee = obj[0]
                        pos = obj[1]
                        mass = obj[2]
                        objid = obj[3]
                        radius = Obj_Type.ALL[typee].radius_mass * mass
                        central_line = (Vector2d.from_tuple(event.pos) + camera - Vector2d.from_tuple(pos))
                        if central_line.isInBox(Vector2d(-radius, -radius), Vector2d(radius, radius)):
                            if central_line.lenght() <= radius:
                                info = objid
                                selected = []
                                hit = True
                                break
                    if not hit:
                        for cell in data[1]:
                            typee = cell[0]
                            owner = cell[1]
                            pos = cell[3]
                            cellid = cell[5]
                            radius = Cell_Type.ALL[typee].radius
                            central_line = (Vector2d.from_tuple(event.pos) + camera - Vector2d.from_tuple(pos))
                            if central_line.isInBox(Vector2d(-radius, -radius), Vector2d(radius, radius)):
                                if central_line.lenght() <= radius:
                                    info = cellid
                                    hit = True
                                    if owner == pl:
                                        selected.append(cellid)
                                    break
                    if not hit:
                        info = -1
                        mouse_down = True
                        mouse_down_point = Vector2d.from_tuple(event.pos) + camera
                    else:
                        mouse_down = False
                else:
                    if info != -1:
                        for button in buttons:
                            if Vector2d.from_tuple(event.pos).isInBox(button[0] + Vector2d((w//4)*3, 0), button[0] + button[1] + Vector2d((w//4)*3, 0)):
                                send_info[1].append([info, button[5]])
                                break
            elif event.button == 3:
                for cellid in selected:
                    send_info[0].append([cellid, (Vector2d.from_tuple(event.pos) + camera).get_squeezed(Vector2d(0, 0), WORLD_SIZE)])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if mouse_down:
                    mouse_down = False
                    if not shift_down:
                        selected = []
                    for cell in data[1]:
                        owner = cell[1]
                        pos = cell[3]
                        cellid = cell[5]
                        if owner != pl:
                            continue
                        if Vector2d.from_tuple(pos).isInBox(mouse_down_point, Vector2d.from_tuple(event.pos) + camera):
                            selected.append(cellid)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera.y -= camera_speed
    if keys[pygame.K_a]:
        camera.x -= camera_speed
    if keys[pygame.K_s]:
        camera.y += camera_speed
    if keys[pygame.K_d]:
        camera.x += camera_speed
    # print(send_info)
    if len(send_info[0]) == 0 and len(send_info[1]) == 0:
        sock.send(to_bytes([]))
    else:
        sock.send(to_bytes(send_info))

    # print("awaiting data")
    dataa = sock.recv(2**16)
    # print_bytes(dataa)
    data = from_bytes(dataa)
    # print("recieved data")

    active_zone.fill((20, 20, 20))
    info_zone.fill((0, 0, 0))
    for obj in data[0]:
        typee = obj[0]
        pos = obj[1]
        mass = obj[2]
        objid = obj[3]
        # print("was  here")
        draw_obj(active_zone, typee, Vector2d.from_tuple(pos), mass)

        if objid == info:
            info_obj(info_zone, font, typee, pos, mass)
    
    for cell in data[1]:
        # print(cell)
        typee = cell[0]
        owner = cell[1]
        energy = cell[2]
        pos = cell[3]
        mass = cell[4]
        cellid = cell[5]
        draw_cell(active_zone, typee, Vector2d.from_tuple(pos), owner, (cellid in selected), energy)
        if cellid == info:
            if 0 <= typee < 4:
                resources = cell[6]
                next_produce = cell[7] - 1
                timer = cell[8]
                args = [resources, next_produce, timer]
            elif 4 <= typee < 8:
                resources = cell[6]
                args = [resources]
            elif 8 <= typee < 12:
                args = []
            info_cell(info_zone, font, typee, pos, mass, energy, owner, args)

    if mouse_down:
        mx, my = pygame.mouse.get_pos()
        nx, ny = (mouse_down_point - camera).as_tuple()
        mx, nx = min(mx, nx), max(mx, nx)
        my, ny = min(my, ny), max(my, ny)
        pygame.draw.rect(active_zone, (200, 200, 200), (mx, my, nx-mx, ny-my), 5)
    screen.blit(active_zone, (0, 0))
    screen.blit(info_zone, (w - w//4, 0))
    pygame.display.flip()
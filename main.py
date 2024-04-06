import pygame
import math

# 初始化 Pygame
pygame.init()

# 設置視窗大小和顯示
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three Body Simulation")

# 定義顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Particle_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# 定義物體類
class Particle:
    def __init__(self, x, y, mass, vx=0, vy=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.vx = 0
        self.vy = 0
        self.color = Particle_colors.pop(0)
        self.tails = []
        self.tail_length = 500

    def update(self):
        self.x += self.vx
        self.y += self.vy
        # save tails
        self.tails.append((self.x, self.y))
        if len(self.tails) > self.tail_length:
            self.tails.pop(0)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.mass//100)
        # draw tails
        for i, tail in enumerate(self.tails):
            # draw line
            if i > 0:
                pygame.draw.line(screen, self.color, self.tails[i-1], tail, i//100)

# 計算引力
def calculate_gravity(p1, p2):
    G = 0.1
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = max(math.sqrt(dx**2 + dy**2), 10)  # 避免除以0
    force = G * p1.mass * p2.mass / distance**2
    angle = math.atan2(dy, dx)
    fx = math.cos(angle) * force
    fy = math.sin(angle) * force
    return fx, fy

# 創建物體
particle1 = Particle(200, 300, 1000)
particle2 = Particle(600, 300, 500)
particle3 = Particle(500, 100, 700)
# 穩定三體特殊解
# particle1 = Particle(300, 300, 1000)
# particle2 = Particle(400, 300, 500)
# particle3 = Particle(200, 300, 500)
# particle1.vx = 0
# particle1.vy = 0
# particle2.vx = 0
# particle2.vy = -1
# particle3.vx = 0
# particle3.vy = 1


# 主迴圈
running = True
is_drag = False

screen_x, screen_y = 0, 0
scale = 1
while running:
    # make screen dragable
    if pygame.mouse.get_pressed()[0] and (is_drag == False):
        is_drag = True 
        lastMousePos = pygame.mouse.get_pos()
    elif is_drag and pygame.mouse.get_pressed()[0]:
        dx = pygame.mouse.get_pos()[0] - lastMousePos[0]
        dy = pygame.mouse.get_pos()[1] - lastMousePos[1]
        print("drag", dx, dy)
        particle1.x += dx
        particle1.y += dy
        particle2.x += dx
        particle2.y += dy
        particle3.x += dx
        particle3.y += dy
        screen_x += dx
        screen_y += dy
        for i in range(len(particle1.tails)):
            particle1.tails[i] = (particle1.tails[i][0] + dx, particle1.tails[i][1] + dy)
        for i in range(len(particle2.tails)):
            particle2.tails[i] = (particle2.tails[i][0] + dx, particle2.tails[i][1] + dy)
        for i in range(len(particle3.tails)):
            particle3.tails[i] = (particle3.tails[i][0] + dx, particle3.tails[i][1] + dy)
        lastMousePos = pygame.mouse.get_pos()
    elif not pygame.mouse.get_pressed()[0]:
        is_drag = False
    # print(is_drag,pygame.mouse.get_pressed()[0], screen_x, screen_y)
    
    

        
    
    
    
    screen.fill(BLACK)
    
    # show screen_x, screen_y
    font = pygame.font.SysFont("simhei", 24)
    text = font.render(f"screen_x: {screen_x}, screen_y: {screen_y}", True, WHITE)
    screen.blit(text, (0,0))
    
    

    # 繪製和更新物體
    particle1.draw()
    particle2.draw()
    particle3.draw()
    particle1.update()
    particle2.update()
    particle3.update()

    # 計算引力並更新速度
    for p1, p2 in [(particle1, particle2), (particle2, particle3), (particle3, particle1)]:
        fx, fy = calculate_gravity(p1, p2)
        p1.vx += fx / p1.mass
        p1.vy += fy / p1.mass
        p2.vx -= fx / p2.mass
        p2.vy -= fy / p2.mass
    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 滑鼠滾輪縮放，當滾輪向前滾動時，放大顯示，向後滾動時，縮小
            print(event.button)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.button == 4:
                if scale < 20:
                    scale *= 1.1
                    # scale the particle relative to the mouse position
                    particle1.x = (particle1.x - mouse_x) * 1.1 + mouse_x
                    particle1.y = (particle1.y - mouse_y) * 1.1 + mouse_y
                    particle2.x = (particle2.x - mouse_x) * 1.1 + mouse_x
                    particle2.y = (particle2.y - mouse_y) * 1.1 + mouse_y
                    particle3.x = (particle3.x - mouse_x) * 1.1 + mouse_x
                    particle3.y = (particle3.y - mouse_y) * 1.1 + mouse_y
                    for i in range(len(particle1.tails)):
                        particle1.tails[i] = ((particle1.tails[i][0] - mouse_x) * 1.1 + mouse_x, (particle1.tails[i][1] - mouse_y) * 1.1 + mouse_y)
                    for i in range(len(particle2.tails)):
                        particle2.tails[i] = ((particle2.tails[i][0] - mouse_x) * 1.1 + mouse_x, (particle2.tails[i][1] - mouse_y) * 1.1 + mouse_y)
                    for i in range(len(particle3.tails)):
                        particle3.tails[i] = ((particle3.tails[i][0] - mouse_x) * 1.1 + mouse_x, (particle3.tails[i][1] - mouse_y) * 1.1 + mouse_y)
                        
            elif event.button == 5:
                if scale > 0.1:
                    scale *= 0.9
                    # scale the particle
                    particle1.x = (particle1.x - mouse_x) * 0.9 + mouse_x
                    particle1.y = (particle1.y - mouse_y) * 0.9 + mouse_y
                    particle2.x = (particle2.x - mouse_x) * 0.9 + mouse_x
                    particle2.y = (particle2.y - mouse_y) * 0.9 + mouse_y
                    particle3.x = (particle3.x - mouse_x) * 0.9 + mouse_x
                    particle3.y = (particle3.y - mouse_y) * 0.9 + mouse_y
                    for i in range(len(particle1.tails)):
                        particle1.tails[i] = ((particle1.tails[i][0] - mouse_x) * 0.9 + mouse_x, (particle1.tails[i][1] - mouse_y) * 0.9 + mouse_y)
                    for i in range(len(particle2.tails)):
                        particle2.tails[i] = ((particle2.tails[i][0] - mouse_x) * 0.9 + mouse_x, (particle2.tails[i][1] - mouse_y) * 0.9 + mouse_y)
                    for i in range(len(particle3.tails)):
                        particle3.tails[i] = ((particle3.tails[i][0] - mouse_x) * 0.9 + mouse_x, (particle3.tails[i][1] - mouse_y) * 0.9 + mouse_y)
                    
            print("scale", scale)

            
        

    pygame.display.flip()

# 退出 Pygame
pygame.quit()

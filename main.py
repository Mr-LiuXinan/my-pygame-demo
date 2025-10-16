import pygame
from pygame.locals import *
from ext import *
pygame.init()
pygame.font.init()

class res:
    s_x, s_y = 400, 500
    fps, real_fps = 60, 0
    title = "Powered by Pygame"
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([s_x, s_y])
    tf = 1
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (135, 206, 250)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    ORANGE = (255, 128, 0)
    GREY = (64, 64, 64)
    event = None

    进制 = ["BIN", "OCT", "DEC", "HEX"]
    进制_list = []
    chozn_进制 = 2
    进制_fontsize =  int(s_x/16)
    进制_font = pygame.font.SysFont("Simhei", 进制_fontsize)
    b_fontsize = int(s_x/14)
    b_font = pygame.font.SysFont("Simhei", b_fontsize)
    num_button_list = []

def rect_modify(x, y, w, h, p):
    if p == "c": #中心
        return Rect(x-w/2, y-h/2, w, h)
    elif p == "lu": #左上
        return Rect(x, y, w, h)
    elif p == "ld": #左下
        return Rect(x, y-h, w, h)
    elif p == "ru": #右上
        return Rect(x-w, y, w, h)
    elif p == "rd": #右下
        return Rect(x-w, y-h, w, h)
    elif p == "lm": #左中
        return Rect(x, y-h/2, w, h)
    elif p == "rm": #右中
        return Rect(x-w, y-h/2, w, h)
    elif p == "um": #上中
        return Rect(x-w/2, y, w, h)
    elif p == "dm": #下中
        return Rect(x-w/2, y-h, w, h)

class 进制_button:
    def __init__(self, index):
        self.color = [res.WHITE, res.BLUE]
        self.is_chozn = 0
        self.index = index
        self.name = res.进制[self.index]
        self.rect = None
        self.num = str(0)

    def show(self):
        x, y = 10, res.s_y/8 + self.index*res.进制_fontsize
        w, h = res.s_x, res.进制_fontsize
        self.rect = rect_modify(x, y, w, h, "lm")
        rect1 = rect_modify(x+len(self.name)*res.进制_fontsize, y, w, h, "lm")
        self.is_chozn = 1 if self.index == res.chozn_进制 else 0
        res.screen.blit(res.进制_font.render(self.name+"=", True, self.color[self.is_chozn]), self.rect)
        res.screen.blit(res.进制_font.render(self.num, True, self.color[self.is_chozn]), rect1)

    def show_boundary(self):
        rect = Rect(self.rect.x - 5, self.rect.y, self.rect.w-10, self.rect.h)
        pygame.draw.rect(res.screen, res.WHITE, rect, 1)

    def calculate(self):
        if res.进制_list[res.chozn_进制] != "0":
            if res.chozn_进制 == 0:
                if self.name == "OCT": self.num = B_O(res.进制_list[0].num) #2-8
                elif self.name == "DEC": self.num = B_D(res.进制_list[0].num) #2-10
                elif self.name == "HEX": self.num = B_H(res.进制_list[0].num) #2-16
            elif res.chozn_进制 == 1: 
                if self.name == "BIN": self.num = O_B(res.进制_list[1].num)  #8-2
                elif self.name == "DEC": self.num = B_D(res.进制_list[0].num) #8-2
                elif self.name == "HEX": self.num = B_H(res.进制_list[0].num) #2-10
            elif res.chozn_进制 == 2:
                if self.name == "BIN": self.num = D_B(res.进制_list[2].num)  #10-2
                elif self.name == "OCT": self.num = B_O(res.进制_list[0].num) #2-8
                elif self.name == "HEX": self.num = B_H(res.进制_list[0].num) #2-16
            elif res.chozn_进制 == 3:
                if self.name == "BIN": self.num = H_B(res.进制_list[3].num)  #16-2
                elif self.name == "OCT": self.num = B_O(res.进制_list[0].num) #2-8
                elif self.name == "DEC": self.num = B_D(res.进制_list[0].num) #2-10


def add_进制():
    for i in range(4):
        new_进制 = 进制_button(index=i)
        res.进制_list.append(new_进制)

def add_num():
    for V in range(len(num_obj)):
        for H in range(len(num_obj[V])):
            new_num = num_button(num=num_obj[V][H], pos=num_pos[V][H])
            res.num_button_list.append(new_num)
            

def AC():
    for j in res.进制_list:
        j.num = str(0)

def Del():
    num = res.进制_list[res.chozn_进制].num
    if len(num) >= 2: res.进制_list[res.chozn_进制].num = num[:-1]
    else: res.进制_list[res.chozn_进制].num = "0"

class num_button:
    def __init__(self, num, pos):
        self.num = num
        self.pos = pos
        self.x_len = res.s_x/5
        if self.pos[0] < 3: self.y_len = res.s_x/8 
        elif self.pos[0] == 3: self.y_len = res.s_x/10
        elif self.pos[0] == 4: self.y_len = res.s_x/4
        self.click_tf = 1  # 是否可点击
        self.boundary_index = 0
        self.rect = None
        self.color = [res.GREY, res.WHITE]

    def check(self):
        if self.num == "AC" or self.num == "Del" or self.num == "." or self.num == "=": self.click_tf = 1
        else: 
            if res.chozn_进制 == 0: 
                if self.num == "1" or self.num == "0": self.click_tf = 1 
                else: self.click_tf = 0
            elif res.chozn_进制 == 1:
                if self.num == "1" or self.num == "0" or self.num == "2" or self.num == "3" or self.num == "4" or self.num == "5" or self.num == "6" or self.num == "7": self.click_tf = 1
                else: self.click_tf = 0
            elif res.chozn_进制 == 2:
                if self.num == "1" or self.num == "0" or self.num == "2" or self.num == "3" or self.num == "4" or self.num == "5" or self.num == "6" or self.num == "7" or self.num == "8" or self.num == "9": self.click_tf = 1
                else: self.click_tf = 0
            elif res.chozn_进制 == 3:
                self.click_tf = 1

    def input(self):
        if res.进制_list[res.chozn_进制].num == "0": 
            if self.num != ".": res.进制_list[res.chozn_进制].num = ""
            else:  res.进制_list[res.chozn_进制].num += "."
        if self.num == "AC": AC()
        elif self.num == "Del": Del()
        elif self.num == ".": 
            ch = 0
            for i in res.进制_list[res.chozn_进制].num:
                if i == ".": ch = 1
            res.进制_list[res.chozn_进制].num += self.num if ch == 0 else ""
        else:
            res.进制_list[res.chozn_进制].num += self.num
        
    def show(self):
        x, y, w, h = self.pos[0]*self.x_len, res.s_y-res.s_x/2+self.pos[1]*self.y_len, self.x_len, self.y_len
        self.rect = Rect(x, y, w, h)
        pygame.draw.rect(res.screen, self.color[self.boundary_index], self.rect, 1)
        rect2 = rect_modify(x+self.x_len/2,
                            y+self.y_len/2,
                            res.b_fontsize*len(self.num)/2,
                            res.b_fontsize, "c")
        res.screen.blit(res.b_font.render(self.num, True, self.color[self.click_tf]), rect2)

def screen_update():
    pygame.display.update()
    res.clock.tick(res.fps)
    res.real_fps = res.clock.get_fps()
    pygame.display.set_caption(res.title+"  fps:"+str(int(res.real_fps)))

def traversal(m_x, m_y):
    mouse_rect = Rect(m_x, m_y, 1, 1)
    for jinzhi in res.进制_list:
        jinzhi.calculate()
        jinzhi.show()
        if mouse_rect.colliderect(jinzhi.rect):
            jinzhi.show_boundary()
            if res.event.type == pygame.MOUSEBUTTONDOWN:
                res.chozn_进制 = res.进制_list.index(jinzhi)
    for num_button in res.num_button_list:
        num_button.check()
        num_button.show()
        num_button.boundary_index = 0
        if mouse_rect.colliderect(num_button.rect):
            if num_button.click_tf:
                num_button.boundary_index = 1
                if res.event.type == pygame.MOUSEBUTTONDOWN:
                    num_button.input()
        

def start():
    add_进制()
    add_num()
    while res.tf:
        res.screen.fill((res.BLACK))
        res.event = pygame.event.poll()
        if res.event.type == pygame.QUIT:
            res.tf = 0
        m_x, m_y = pygame.mouse.get_pos()
        traversal(m_x, m_y)
        screen_update()
        
if __name__ == "__main__":
    start()

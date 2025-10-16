num_obj = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["0", ".", "F"],

    ["A", "B", "C", "D", "E"],
    ["AC", "Del"]
]

num_pos = [
    [(0,0), (1,0), (2,0)],
    [(0,1), (1,1), (2,1)],
    [(0,2), (1,2), (2,2)],
    [(0,3), (1,3), (2,3)],

    [(3,0), (3,1), (3,2), (3,3), (3,4), (3,5)],
    [(4,0), (4,1)]
]

O_B_list = [
    ("0","000"), ("1","001"), ("2","010"),
    ("3","011"), ("4","100"), ("5","101"),
    ("6","110"), ("7","111"),
]

H_B_list = [
    ("0","0000"), ("1","0001"), ("2","0010"),
    ("3","0011"), ("4","0100"), ("5","0101"),
    ("6","0110"), ("7","0111"), ("8","1000"),
    ("9","1001"), ("A","1010"), ("B","1011"),
    ("C","1100"), ("D","1101"), ("E","1110"), ("F", "1111"),
]

def catg(num):  # 整数小数分类
    point_num = 0
    point_index = 0
    for p in range(len(num)):
        if num[p] == ".":
            point_num += 1
            point_index = p
    Int, Float = "", ""
    if point_num == 0: 
        Int = num
    elif point_num == 1:
        Int = num[:point_index]
        Float = num[point_index+1:]
    return Int, Float

def segm(Int, Float, nav):  # 分节
    Int_part, Float_part = [], []
    for Z in range(len(Int)//nav):
        Int_part.append(Int[Z*nav:(Z+1)*nav])
    for F in range(len(Float)//nav):
        Float_part.append(Float[F*nav:(F+1)*nav])
    return Int_part, Float_part 

def allot_1(Int_part, Float_part, allot_list):  # 分配数值，置换2-n
    shift_Int, shift_Float = "",""
    for si in Int_part:
        for a in allot_list:
            if a[1] == si:
                shift_Int += a[0]
    for sf in Float_part:
        for b in allot_list:
            if b[1] == sf:
                shift_Float += b[0]
    return shift_Int, shift_Float

def allot_2(Int_part, Float_part, allot_list):  # 分配数值，置换n-2
    shift_Int, shift_Float = "",""
    for si in Int_part:
        for a in allot_list:
            if a[0] == si:
                shift_Int += a[1]
    for sf in Float_part:
        for b in allot_list:
            if b[0] == sf:
                shift_Float += b[1]
    return shift_Int, shift_Float

def zero_del(shift_Int, shift_Float):  #去零
    for qu0i in shift_Int:
        if shift_Int[0] == "0" and len(shift_Int) >= 2: shift_Int = shift_Int[1:]
        else: break
    for qu0f in shift_Float:  
        if shift_Float[-1] == "0": shift_Float = shift_Float[:-1]
        else: break
    return shift_Int, shift_Float

def recur_z(num, shift_Int_list):  #10-2整数部分
    while num > 1:
        shift_Int_list.insert(0, num%2)
        num //= 2
    shift_Int_list.insert(0, 1) if num != 0 else shift_Int_list.insert(0, 0)

def recur_f(num, shift_Float_list):  #10-2小数部分
    num = float("0."+num)
    if num == 0: pass
    else:
        for f in range(25):
            num *= 2
            if num >= 1:  shift_Float_list.append(1); num -= 1
            else: shift_Float_list.append(0)
            if num == 0: break

def B_O(bin):  # 2-8
    Int, Float = catg(bin)
    Int = (3-len(Int)%3)*"0" + Int
    Float = Float + (3-len(Float)%3)*"0"
    Int_part, Float_part = segm(Int, Float, 3)  # 分节
    shift_Int, shift_Float = allot_1(Int_part, Float_part, O_B_list)
    shift_Int, shift_Float = zero_del(shift_Int, shift_Float)
    new_num = shift_Int+"."+shift_Float if shift_Float != "" else shift_Int
    return new_num
    
def B_D(bin):
    Int, Float = catg(bin)
    shift_Int, shift_Float = 0, 0
    for i in range(len(Int)):
        shift_Int += int(Int[i])*(2**(len(Int)-i-1))
    for f in range(len(Float)):
        shift_Float += int(Float[f])*(2**(-f-1))
    new_num = str(shift_Int + shift_Float)
    return new_num

def B_H(bin):
    Int, Float = catg(bin)
    Int = (4-len(Int)%4)*"0" + Int  
    Float = Float + (4-len(Float)%4)*"0"
    Int_part, Float_part = segm(Int, Float, 4)  # 分节
    shift_Int, shift_Float = allot_1(Int_part, Float_part, H_B_list)
    shift_Int, shift_Float = zero_del(shift_Int, shift_Float)
    new_num = shift_Int+"."+shift_Float if shift_Float != "" else shift_Int
    return new_num

def O_B(oct):
    Int, Float = catg(oct)
    Int_part, Float_part = segm(Int, Float, 1)
    shift_Int, shift_Float = allot_2(Int_part, Float_part, O_B_list)
    shift_Int, shift_Float = zero_del(shift_Int, shift_Float)
    new_num = shift_Int+"."+shift_Float if shift_Float != "" else shift_Int
    return new_num

def H_B(hex):
    Int, Float = catg(hex)
    Int_part, Float_part = segm(Int, Float, 1)
    shift_Int, shift_Float = allot_2(Int_part, Float_part, H_B_list)
    shift_Int, shift_Float = zero_del(shift_Int, shift_Float)
    new_num = shift_Int+"."+shift_Float if shift_Float != "" else shift_Int
    return new_num

def D_B(dec):
    Int, Float = catg(dec)
    shift_Int_list, shift_Float_list = [], []
    recur_z(int(Int), shift_Int_list)
    recur_f(Float, shift_Float_list)
    shift_Int, shift_Float = "", ""
    for sz in shift_Int_list:
        shift_Int += str(sz)
    for sf in shift_Float_list:
        shift_Float += str(sf)
    new_num = shift_Int+"."+shift_Float if shift_Float != "" else shift_Int
    return new_num

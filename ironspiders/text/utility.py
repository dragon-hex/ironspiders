def split8(number, length=8):
    value, gen = (-(number) if number < 0 else number), []
    for index in range(0, length):
        gen.append(value & 0xFF)
        value = value >> 8
    return gen

def convert8(listv, length=8):
    totalSum, shift = 0, 0
    for index in range(0, length):
        totalSum    += (listv[index] << shift)
        shift       += 8
    return totalSum

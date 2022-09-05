I = [[1, 20, 2],
     [30, 40, 4],
     [50, 60, 6]]

k = [[0, 0, 0],
     [0,  1, 0],
     [0, 0, 0]]

largura = 3
altura = 3
x = 1
y = 1


def p_x(px):
    if px < 0:
        px = 0
    if px >= largura:
        px = largura - 1
    return px


def p_y(py):
    if py < 0:
        py = 0
    if py >= altura:
        py = altura - 1
    return py


for j in range(altura):
    for i in range(largura):
        I[j][i] = I[p_x(j - 1)][p_y(i - 1)] * k[0][0] + I[p_x(j)][p_y(i - 1)] * k[1][0] + I[p_x(j + 1)][p_y(i - 1)] * k[2][0] \
                  + I[p_x(j - 1)][p_y(i)] * k[0][1] + I[p_x(j)][p_y(i)] * k[1][1] + I[p_x(j + 1)][p_y(i)] * k[2][1] \
                  + I[p_x(j - 1)][p_y(i + 1)] * k[0][2] + I[p_x(j)][p_y(i + 1)] * k[1][2] + I[p_x(j + 1)][p_y(i + 1)] * k[2][2]


print(I)

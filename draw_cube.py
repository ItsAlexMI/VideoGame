from libraries import *

# Vertices y caras del cubo
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 1),
    (1, 1, 0),
    (1, 0, 1)
)

def draw_cube(x, y, z):
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(colors[i])
        for vertex in surface:
            # Ajusta las coordenadas del vértice según la posición del cubo
            glVertex3f(vertices[vertex][0] + x,
                       vertices[vertex][1] + y,
                       vertices[vertex][2] + z)
    glEnd()

    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            # Ajusta las coordenadas del vértice según la posición del cubo
            glVertex3f(vertices[vertex][0] + x,
                       vertices[vertex][1] + y,
                       vertices[vertex][2] + z)
    glEnd()

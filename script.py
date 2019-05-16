import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    polygons = new_matrix()
    ident( polygons )

    stack = [ [x[:] for x in polygons] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    polygons = []
    step_3d = 100
    consts = ''
    polygons = []
    edges = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    #print symbols
    #for s in symbols:
    #    print s
    #    print symbols[s]
    for command in commands:

        #print command
        op = command['op']
        args = command['args']

        if op == 'push':
            stack.append( [x[:] for x in stack[-1]] )

        elif op == 'pop':
            stack.pop()

        elif op == 'move':
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif op == 'scale':
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            if command['knob']:
                knob = command['knob']
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif op == 'rotate':
            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif op == 'sphere':
            if command['constants'] == None:
                con = '.white'
            else:
                con = command['constants']
            add_sphere(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult( stack[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, con)
            polygons = []

        elif op == 'torus':
            if command['constants'] == None:
                con = '.white'
            else:
                con = command['constants']
            add_torus(polygons,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult( stack[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, con)
            polygons = []

        elif op == 'box':
            if command['constants'] == None:
                con = '.white'
            else:
                con = command['constants']
            add_box(polygons,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( stack[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, con)
            polygons = []

        elif op == 'line':
            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( systems[-1], edges )
            draw_lines(eges, screen, zbuffer, color)
            edges = []

        elif op == 'display' or op == 'save':
            print command
            if op == 'display':
                display(screen)
            else:
                save_extension(screen, args[0] + '.jpg')

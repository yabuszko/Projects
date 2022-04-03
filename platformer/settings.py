import os
MUSIC_VOLUME = 0.5
WIDTH = 1200
HEIGHT = 700

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))

levels = [
[
'                     ',
'                     ',
'                     ',
'                     ',
'                     ',
'                     ',
'             C       ',
'            CXC      ',
'          CXXXXXC    ',
'P        XXXXXXXXX  E',
'XXXXXXXXXXXXXXXXXXXXX'
],
[
'                     ',
'                     ',
'                     ',
'                     ',
'                     ',
'            XX       ',
'    CCC     XX       ',
'    XXXX   XXXX      ',
'           XXXXX1    ',
'  EP      XXXXXXXX  T',
'  XXXXXXXXXXXXXXXXXXX'
],
[
'                                   ',
'                                   ',
'                                   ',
'                                   ',
'                                   ',
'                 11                ',
'               CXXXXC              ',
'               XXXXXX              ',
'                XXXX               ',
'C     EP      F XXXX F    5  C  CCT',
'XXXXXXXXXXXXXXXXXXXXXXXXXXX  X  XXX'],
[
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X  6 6                                           X',
'XK                                           CCCEX',
'XXXXXX             CCCCC                    CXXXXX',
'X                11 11  11   K             CXXXXXX',
'X     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X7CC  X                                     66   X',
'X7CC X                                  CCCCCCCCCX',
'X7CC X      CCCC                        XXXXXXXXXX',
'X FF D P  11   11   Q   5   K   CCCC    DD      TX',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
],
[
'X    @         #     ^         $@        X',
'X    @         #     ^         $@        X',
'X    @         #     ^         $@        X',
'X    @         #     ^         $@        X',
'X    @         #     ^         $@        X',
'X    @         #     ^         $@        X',
'X C  @  C      #  C  ^    C    $@        X',
'X C  @  C      #  C  ^    C    $@        X',
'X r  @  g   P  #  g  ^    r    $@      E X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X@@@^^^###$$$@@@^^^###$$$@@@^^^###$$$@@@^X'],
[
'                                          X'
'                                          X',
'E     XXXX                                X',
'^     XCCX                                X',
'^^    XCCX                                X',
'^^^   D rX                                X',
'     XXXXX                                X',
' K  #                                     X',
'^^^#                  ^^                XXX',
'^F^                  @  @              8XKX',
'^X^ Q  g     P   Q  111111       r      DTX',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXX XXXXXXXX'],
[
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
'X                                                X',
'X                                                X',
'X                                                X',
'X                   RRR   RRR                    X',
'X                  RCCCCCCCCCR                   X',
'X                 RCCCCCRCCCCCR                  X',
'X                RCCCCCC CCCCCCR                 X',
'X               RCCCCC  !  CCCCCR                X',
'X              RCCCCC  RRR  CCCCCR               X',
'X  P          RCCCC   RRRRR   CCCCR              X',
'XRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRX'
]]

tile_size = 64
screen_width = 1200
#screen_height = len(level1_map) * tile_size
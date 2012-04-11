from pandac.PandaModules import BitMask32

RED               = (1, 0, 0, 0)
GREEN             = (0, 1, 0, 0)
BLUE              = (0, 0, 1, 0)
YELLOW            = (1, 1, 0, 0)
TEAL              = (0, 1, 1, 0)
GREY              = (0.5, 0.5, 0.5, 0.5)

TRANSLATE         = 1
TRANSLATE_POINT_A = 2
TRANSLATE_POINT_B = 4
SCALE             = 8
NONE              = 16
CAMERA_VECTOR     = 32

AXIS_COLLISION_MASK = BitMask32.bit(0)

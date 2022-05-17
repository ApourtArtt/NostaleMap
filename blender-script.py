import bpy
import os
import struct
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

class bgr:
    def __init__(self, data):
        self.blue   = data[0]
        self.red    = data[1]
        self.green  = data[2]

#struct.unpack('<f', bytes(data[0x30:0x30+4]))[0]

class MapObject:
    def __init__(self, data):
        self.interType  = data[0x00]
        self.modelIndex = int.from_bytes(data[0x01:0x01+2], byteorder='little', signed=True)
        if self.interType == 0x00:
            self.x = -15
            self.y = -15
            self.z = -15
        elif self.interType == 0x01:
            self.x          = struct.unpack('<f', bytes(data[0x2F:0x2F+4]))[0]
            self.z          = struct.unpack('<f', bytes(data[0x33:0x33+4]))[0]
            self.y          = struct.unpack('<f', bytes(data[0x37:0x37+4]))[0]
        elif self.interType == 0x02:
            self.x          = struct.unpack('<f', bytes(data[0x2F:0x2F+4]))[0]
            self.z          = struct.unpack('<f', bytes(data[0x33:0x33+4]))[0]
            self.y          = struct.unpack('<f', bytes(data[0x37:0x37+4]))[0]
        elif self.interType == 0x03:
            self.x          = struct.unpack('<f', bytes(data[0x2F:0x2F+4]))[0]
            self.z          = struct.unpack('<f', bytes(data[0x33:0x33+4]))[0]
            self.y          = struct.unpack('<f', bytes(data[0x37:0x37+4]))[0]
        print(self.x, self.y, self.z)
        
        #self.x          = struct.unpack('<f', bytes(data[0x31:0x31+4]))[0]
        #self.z          = struct.unpack('<f', bytes(data[0x35:0x35+4]))[0]
        #self.y          = struct.unpack('<f', bytes(data[0x39:0x39+4]))[0]
        #self.rx         = struct.unpack('<f', bytes(data[0x37:0x37+4]))[0]
        #self.ry         = struct.unpack('<f', bytes(data[0x39:0x39+4]))[0]
        #self.rz         = struct.unpack('<f', bytes(data[0x3B:0x3B+4]))[0]
        self.size       = 1

def getModelsID(data):
    array = []
    for i in range(0,len(data),4):
        array.append(int.from_bytes(data[i:i+4], byteorder='little', signed=True))
    return array

def getMapObjects(data):
    array = []
    i = 1
    while i < len(data):
        interType = data[i]
        step = 0
        if interType == 0x00:
            step = 0x13
        elif interType == 0x01:
            step = 0x45
        elif interType == 0x02:
            step = 0x4B
        elif interType == 0x03:
            step = 0x58
        else:
            print(str(hex(interType)) + " INTERACTION NOT HANDLED")
            break
        array.append(MapObject(data[i:i+step]))
        i += step
    return array

class MapStructure:
    def __init__(self, data):
        self.bgrAmbient = bgr(data[0x5F:0x5F+3])
        self.bgrObjects = bgr(data[0x64:0x64+3])
        self.bgrMapBackground = bgr(data[0x67:0x67+3])
        self.cameraRotation = data[0x6D]
        self.fog = int.from_bytes(data[0x77:0x77+2], byteorder='little', signed=True)
        self.numberModels = int.from_bytes(data[0x85:int(0x85+2)], byteorder='little', signed=True)
        self.modelsID = getModelsID(data[0x87:0x87+(4*self.numberModels)])
        self.mapObjects = getMapObjects(data[0x88+int((4*self.numberModels)):])

def display(mapStruct, f):
    #for i in range(mapStruct.mapObjects):
    i = 0
    a = 0
    # a is used to display a maximum of {a} objects
    # remove it from the condition below if you want to show all the objects
    # but my shitty graphic card don't allow me to :(
    while i < len(mapStruct.mapObjects) and a < 500:
        if mapStruct.mapObjects[i].modelIndex < len(mapStruct.modelsID) and mapStruct.mapObjects[i].modelIndex >= 0:
            mapObj = mapStruct.mapObjects[i]
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.import_scene.obj(filepath=os.path.dirname(os.path.abspath(f))+os.sep+"3dmodels"+os.sep+str()+str(mapStruct.modelsID[mapObj.modelIndex])+".obj")
            obj = bpy.context.selected_objects[0]
            
            obj.location[0] = mapObj.y
            obj.location[1] = mapObj.x
            obj.location[2] = mapObj.z
            
            if mapObj.interType == 0x01:
                obj.delta_rotation_euler[2] = 1.57
            elif mapObj.interType == 0x02:
                obj.rotation_euler[0] = 0
                obj.delta_rotation_euler[0] = 1.57
                obj.delta_rotation_euler[2] = 3.14
            
            # Mirror effect
            #if mapObj.interType == 0x01:
             #   bpy.ops.transform.mirror(
              #  orient_type='GLOBAL',
               # orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                #orient_matrix_type='GLOBAL',
                #constraint_axis=(False, True, False))
                
            #obj.rotation_euler[0] = mapObj.rx
            #obj.rotation_euler[0] = mapObj.ry
            #obj.rotation_euler[0] = mapObj.rz
            #obj.delta_rotation_euler[0] = 1.57
            #print(mapObj.x, mapObj.y, mapObj.z) 
        i = i + 1
        a = a + 1
        

def read_map_file(context, filepath):
    print("running read_map_file...")
    f = open(filepath, 'rb')
    data=list(f.read())
    f.close()
    display(MapStructure(data), filepath)

    return {'FINISHED'}

class ImportMap(Operator, ImportHelper):
    """Import NosTale map file"""
    bl_idname = "import_map.data"
    bl_label = "Import Map file"

    # ImportHelper mixin class uses this
    filename_ext = ".map"

    filter_glob: StringProperty(
        default="*.map",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        return read_map_file(context, self.filepath)

class AyugraPanel(bpy.types.Panel):
    """Manage NosTale map file"""
    bl_label = "Ayugra Panel"
    bl_idname = "OBJECT_PT_ayugra"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    #bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="NosTale Map Manager", icon='WORLD_DATA')
        
        row = layout.row()
        row.operator("import_map.data")


def register():
    bpy.utils.register_class(ImportMap)
    bpy.utils.register_class(AyugraPanel)


def unregister():
    bpy.utils.unregister_class(ImportMap)
    bpy.utils.unregister_class(AyugraPanel)


if __name__ == "__main__":
    register()

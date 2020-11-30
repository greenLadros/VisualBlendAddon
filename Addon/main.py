#ivri korem 2020
"""
VisualBlend is a data visualization tool 
for blender and data scientists.
"""

#addon info
bl_info = {
    "name": "VisualBlend",
    "author": "Ivri Korem",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "description": "Generates a histogram graph based on a csv",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}


#init
#import
import bpy
import csv
import random
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
)
from bpy.props import (
    StringProperty,
    IntProperty,
)


#addon class
class OBJECT_OT_visual_blend(Operator):
    """Create a new Histogram Graph"""
    bl_idname = "object.generate_graph"
    bl_label = "GenerateGraph"
    bl_description = "Generates a histogram graph based on a csv"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_options = {'REGISTER', 'UNDO'}
    
    #props
    filePath: bpy.props.StringProperty(
        name = "File Path",
        default = r"default",
        description = "The Absolute path to the target csv file"
    )
    tickNum: bpy.props.IntProperty(
        name = "Amount of Ticks",
        default = 10,
        min = 1,
        max = 15,
        description = "The Amount of ticks aside the graph"        
    )
    
    #funcs
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self)
    
    def readData(self,filePath):
        #read data from file
        data = dict()
        with open(filePath, newline='') as file:
            reader = csv.reader(file)
            for idx,row in enumerate(reader):
                data[idx] = {
                    'label': row[0],
                    'value': row[1]
                }
        return data
                
    def generateHistogram(self,data,tickNum):
        print("Generating Graph...")
        maxValue = 0
        minValue = 0
        for idx,pair in enumerate(data):
            value = float(data[pair]["value"])
            label = data[pair]["label"]
            
            #generate material
            mat = bpy.data.materials.new("GraphMat"+str(random.randint(0,1000)))
            mat.diffuse_color = (
                random.uniform(0,1),
                random.uniform(0,1),
                random.uniform(0,1),
                1
            )
            
            #create bar
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(idx,0,0)
            )
            bpy.ops.transform.resize(
                value=(1,1,value)
            )
            bpy.ops.transform.translate(
                value=(0.5,0,value/2)
            )
            bpy.context.object.data.materials.append(mat)
            
            #create label
            bpy.ops.object.text_add(
                radius=0.45,
                enter_editmode=False,
                align='WORLD',
                location=(idx,-1.2, 0), 
                rotation=(0, 0, 0)
            )
            ob=bpy.context.object
            ob.data.body = label
            ob.data.bevel_depth = 0.05
            ob.data.materials.append(mat)
            
            #update max and min Value
            maxValue = max(value,maxValue)
            minValue = min(value,minValue)
        
         #create ticks  
        for i in range(0,tickNum):
            step = (maxValue-minValue)/tickNum
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(-1,0,minValue+(i*step))
            )
            bpy.ops.transform.resize(
                value=(1.5,1,0.2)
            )
            
            #add label
            bpy.ops.object.text_add(
                radius=1,
                enter_editmode=False,
                align='WORLD',
                location=(-1.5,0,minValue+(i*step)+0.1), 
                rotation=(1.5, 0, 0)
            )
            ob=bpy.context.object
            ob.data.body = str(minValue+(i*step))
            ob.data.bevel_depth = 0.05
        
        print("Done!")
    
    def cleanUp(self):
        print("Cleaning Up...")
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)
        print("Done!")
    
    #main
    def execute(self, context):
        data = self.readData(self.filePath)
        self.cleanUp()
        self.generateHistogram(data, self.tickNum)
        print("Finished!")
        
        #return
        return {'FINISHED'}


def menuFunc():
    self.layout.operator(OBJECT_OT_visual_blend.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_visual_blend)
    bpy.types.VIEW3D_MT_object.append(menuFunc)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_visual_blend)
    bpy.types.VIEW3D_MT_object.remove(menuFunc)


if __name__ == "__main__":
    register()
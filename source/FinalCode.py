import maya.cmds as mc
from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QAbstractItemView, QColorDialog, QSlider
from PySide2.QtGui import QColor, QPainter, QBrush

class SwapMat():
    def __init__(self):
        self.mesh = set() # a set is a list that has unique elements.
        self.color = [0,0,0]
        self.srcMesh = ""
    def UpdateMatColors(self, r, g, b):
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b
    def AddMaterial(self): 
        for srcMesh in self.mesh:
            ghostName = srcMesh 
            self.srcMesh = ghostName
        matName = self.GetMaterialNameForMesh(self.srcMesh) # figure out the name for the material
        if not mc.objExists(matName): # check if material not exist
            mc.shadingNode("lambert", asShader = True, name = matName) # create the lambert material if not exists
            
        sgName = self.GetShadingEngineForMesh() # fiture out the name of the shading engine
        if not mc.objExists(sgName): # check if the shading engine exists
            mc.sets(name = sgName, renderable = True, empty = True) # create the shading engine if not exists

        mc.connectAttr(matName + ".outColor", sgName + ".surfaceShader", force = True) # connet the material to the shading engine
        mc.sets(self.srcMesh, edit=True, forceElement = sgName) # assign the material to ghost

        mc.setAttr(matName + ".color", self.color[0], self.color[1], self.color[2], type = "double3")
    def GetMaterialNameForMesh(self, mesh):
        return self.srcMesh  + "_mat"
    def GetShadingEngineForMesh(self):
        return self.srcMesh + "_sg"
    def UpdateSelection(self):
        selection = mc.ls(sl=True)
        self.mesh.clear() # removes all elements in the set.
        for selected in selection:
            shapes = mc.listRelatives(selected, s=True) # find all shapes of the selected object
            for s in shapes:
                if mc.objectType(s) == "mesh": # the object is a mesh
                    self.mesh.add(selected) # add the mesh to our set.


        

class ColorPicker(QWidget):
    onColorChanged = Signal(QColor) # this adds a built in class member called onColorChanged.
    def __init__(self, width = 80, height = 20):
        super().__init__()
        self.setFixedSize(width, height)
        self.color = QColor()

    def mousePressEvent(self, event):
        color = QColorDialog().getColor(self.color) 
        self.color = color
        self.onColorChanged.emit(self.color)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(0,0,self.width(), self.height())

class GhostWidget(QWidget):
    def __init__(self):
        super().__init__() # needed to call if you are inheriting from a parent class
        self.swapmat = SwapMat() # create a ghost to pass command to.
        self.setWindowTitle("Ghoster Poser V1.0") # set the title of the window
        self.masterLayout = QVBoxLayout() # creates a vertical layout         
        self.setLayout(self.masterLayout) # tells the window to use the vertical layout created in the previous line


        self.ctrlLayout = QHBoxLayout()
        self.masterLayout.addLayout(self.ctrlLayout)

        addGhostBtn = QPushButton("Add/Update")
        addGhostBtn.clicked.connect(self.AddMaterialBtn)
        self.ctrlLayout.addWidget(addGhostBtn)

        self.materialLayout = QHBoxLayout()
        self.masterLayout.addLayout(self.materialLayout)
        self.colorPicker = ColorPicker()
        self.colorPicker.onColorChanged.connect(self.UpdateColor)
        self.materialLayout.addWidget(self.colorPicker)                     

    

   

    def AddMaterialBtn(self):
        self.swapmat.UpdateSelection()
        self.swapmat.AddMaterial()
        
    def UpdateColor(self, newColor: QColor):
        r = newColor.redF()
        g = newColor.greenF()
        b = newColor.blueF()
        self.swapmat.UpdateMatColors(r,g,b)

ghostWidget = GhostWidget()
ghostWidget.show()   
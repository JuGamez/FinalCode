import maya.cmds as mc
from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QAbstractItemView, QColorDialog, QSlider
from PySide2.QtGui import QColor, QPainter, QBrush

class SwapMat():
    def __init__(self):
        self.mesh = ""
        self.color = [0,0,0]
    def UpdateMatColors(self, r, g, b):
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b
        mat = self.GetMaterialNameForGhost(self.mesh)
        mc.setAttr(mat + ".color", self.color[0], self.color[1], self.color[2], type = "double3")
    def AddMaterial(self):
        selection = mc.ls(sl=True)[0]
        matName = self.GetMaterialNameForGhost(self.mesh) # figure out the name for the material
        if not mc.objExists(matName): # check if material not exist
            mc.shadingNode("lambert", asShader = True, name = matName) # create the lambert material if not exists
            
        sgName = self.GetShadingEngineForMesh(self.mesh) # fiture out the name of the shading engine
        if not mc.objExists(sgName): # check if the shading engine exists
            mc.sets(name = sgName, renderable = True, empty = True) # create the shading engine if not exists

        mc.connectAttr(matName + ".outColor", sgName + ".surfaceShader", force = True) # connet the material to the shading engine
        mc.sets(self.mesh, edit=True, forceElement = sgName) # assign the material to ghost

        mc.setAttr(matName + ".color", self.color[0], self.color[1], self.color[2], type = "double3")
    def GetMaterialNameForMesh(self):
        return "Alex_Body_geo"
    def GetShadingEngineForMesh(self):
        return self.mesh + "_sg"

        

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
        addGhostBtn.clicked.connect(self.swapmat.AddMaterial)
        self.ctrlLayout.addWidget(addGhostBtn)

        self.materialLayout = QHBoxLayout()
        self.masterLayout.addLayout(self.materialLayout)
        colorPicker = ColorPicker()
        colorPicker.onColorChanged.connect(self.swapmat.UpdateMatColors)
        self.materialLayout.addWidget(colorPicker)                     

    

   

    def AddSrcMeshBtnClicked(self):
        self.ghost.SetSelectedAsSrcMesh() # asks ghost to populate it's srcMeshes with the current selection
        self.srcMeshList.clear() # this clears our list widget
        self.srcMeshList.addItems(self.ghost.srcMeshes) # this add the srcMeshes collected eariler to the list widget

ghostWidget = GhostWidget()
ghostWidget.show()
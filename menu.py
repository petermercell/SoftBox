# AreaLight — Soft shadow area light for ScanlineRender2
# Place this file and AreaLight.dll in your ~/.nuke/ directory

import nuke

toolbar = nuke.toolbar("Nodes")
lightMenu = toolbar.addMenu("3D/Lights", icon="Light.png")
lightMenu.addCommand("AreaLight", "nuke.createNode('AreaLight')", icon="Light.png")

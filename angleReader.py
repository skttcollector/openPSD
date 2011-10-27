import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.OpenMayaRender as omRender
import maya.OpenMayaUI as omUI

pluginName = 'angleReader'
nodeId = om.MTypeId(0x101121)


class angleReader(ompx.MPxLocatorNode):
    
    glRenderer = omRender.MHardwareRenderer.theRenderer()
    glFT = glRenderer.glFunctionTable()


    def __init__(self):
        ompx.MPxLocatorNode.__init__(self)


    def compute(self, plug, dataBlock):
        dataBlock.setClean(plug)


#         if plug != angleReader.outAngle_uAttr and plug != angleReader.outWeights_nAttr :
#             return om.kUnknownParameter


#         baseMatrix_DH = om.MDataHandle()
#         baseMatrix_DH = dataBlock.inputValue(angleReader.baseMatrix_mAttr)
#         base_M = baseMatrix_DH.asMatrix()

#         driverMatrix_DH = om.MDataHandle()
#         driverMatrix_DH = dataBlock.inputValue(angleReader.driverMatrix_mAttr)
#         driver_M = driverMatrix_DH.asMatrix()

#         baseAxisX_DH = om.MDataHandle()
#         baseAxisX_DH = data.inputValue(angleReader.baseAxisX_nAttr)
#         baseAxisY_DH = om.MDataHandle()
#         baseAxisY_DH = data.inputValue(angleReader.baseAxisY_nAttr)
#         baseAxisZ_DH = om.MDataHandle()
#         baseAxisZ_DH = data.inputValue(angleReader.baseAxisZ_nAttr)
#         baseAxis_V = om.MVector(baseAxisX_DH.asDouble(), baseAxisY_DH.asDouble(), baseAxisZ_DH.asDouble())


#         frontAxisX_DH = om.MDataHandle()
#         frontAxisX_DH = data.inputValue(angleReader.frontAxisX_nAttr)
#         frontAxisY_DH = data.inputValue(angleReader.frontAxisY_nAttr)
#         frontAxisZ_DH = data.inputValue(angleReader.frontAxisZ_nAttr)
#         MVector frontAxis_V = om.MVector((frontAxisX_DH.asDouble(), frontAxisY_DH.asDouble(), frontAxisZ_DH.asDouble()))


    def draw( self, view, path, dispStyle, status ):
                
        thisNode = self.thisMObject()
        plugDraw = om.MPlug(thisNode, self.draw_nAttr)
        draw = plugDraw.asInt()
        plugSegment = om.MPlug(thisNode, self.segment_nAttr)
        segment = plugSegment.asInt()
        plugPreStart = om.MPlug(thisNode, self.preStart_nAttr)
        preStart = plugPreStart.asFloat()
        plugStart = om.MPlug(thisNode, self.start_nAttr)
        start = plugStart.asFloat()
        plugEnd = om.MPlug(thisNode, self.end_nAttr)
        end = plugEnd.asFloat()
        plugPostEnd = om.MPlug(thisNode, self.postEnd_nAttr)
        postEnd = plugPostEnd.asFloat()
        plugRadius = om.MPlug(thisNode, self.radius)
        radius = plugRadius.asFloat()


        if (draw == 0):
            return


        view.beginGL()  

        self.glFT.glPushAttrib(omRender.MGL_CURRENT_BIT | omRender.MGL_POINT_BIT | omRender.MGL_LINE_BIT)
        self.glFT.glBegin(omRender.MGL_LINE_STRIP)

        arc_angl = math.radians(preStart-postEnd)
        start_ang = math.radians(postEnd)

        theta = arc_angl/(segment-1)
        tag = math.tan(theta)
        rad = math.cos(theta)
        x = radius * math.cos(start_ang)
        y = radius * math.sin(start_ang)

        for i in range(segment):
            self.glFT.glVertex3d(x, y, 0.0)
            tx = -y
            ty = x
            x += tx*tag
            y += ty*tag
            x *= rad
            y *= rad



        self.glFT.glEnd()


        text = ("Angle : "+str(postEnd - preStart))
        view.drawText(text,om.MPoint(0,0,0), omUI.M3dView().kLeft)

        self.glFT.glLineWidth(3)
        self.glFT.glColor3f(1,0,0)
        self.glFT.glBegin(omRender.MGL_LINES)

        x = radius * math.cos(start_ang)
        y = radius * math.sin(start_ang)

        self.glFT.glVertex3d(x*1.05, y*1.05, 0.0)
        self.glFT.glVertex3d(x*0.95, y*0.95, 0.0)

        x = radius * math.cos(math.radians(preStart))
        y = radius * math.sin(math.radians(preStart))

        self.glFT.glVertex3d(x*1.05, y*1.05, 0.0)
        self.glFT.glVertex3d(x*0.95, y*0.95, 0.0)

        x = radius * math.cos(math.radians(start))
        y = radius * math.sin(math.radians(start))

        self.glFT.glVertex3d(x*1.05, y*1.05, 0.0)
        self.glFT.glVertex3d(x*0.95, y*0.95, 0.0)

        x = radius * math.cos(math.radians(end))
        y = radius * math.sin(math.radians(end))

        self.glFT.glVertex3d(x*1.05, y*1.05, 0.0)
        self.glFT.glVertex3d(x*0.95, y*0.95, 0.0)

        self.glFT.glEnd()
        self.glFT.glLineWidth(1.0);
        self.glFT.glPopAttrib()
        view.endGL()


def isBounded( self ):
    return True
        
        
def nodeCreator():
    return ompx.asMPxPtr(angleReader())



def nodeInit():
    nAttr = om.MFnNumericAttribute()
    mAttr = om.MFnMatrixAttribute()
    uAttr = om.MFnUnitAttribute()
    eAttr = om.MFnEnumAttribute()
    cAttr = om.MFnCompoundAttribute()

    # draw
    angleReader.draw_nAttr = nAttr.create("draw", "drw", om.MFnNumericData.kBoolean, 1)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.draw_nAttr)
        
    # segment
    angleReader.segment_nAttr = nAttr.create("segment", "seg", om.MFnNumericData.kInt, 9)
    nAttr.setKeyable(True)
    nAttr.setMin(2)
    angleReader.addAttribute(angleReader.segment_nAttr)
        
    # preStart
    angleReader.preStart_nAttr = nAttr.create("preStart", "pre", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.preStart_nAttr)
        
    # start
    angleReader.start_nAttr = nAttr.create("start", "str", om.MFnNumericData.kFloat, 75.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.start_nAttr)
        
    # end
    angleReader.end_nAttr = nAttr.create("end", "end", om.MFnNumericData.kFloat, 100.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.end_nAttr)
        
    # postEnd
    angleReader.postEnd_nAttr = nAttr.create("postEnd", "sta", om.MFnNumericData.kFloat, 180.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute( angleReader.postEnd_nAttr )
        
    # radius
    angleReader.radius = nAttr.create("radius", "rad", om.MFnNumericData.kFloat, 2.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute( angleReader.radius )
        
    # baseMatrix_mAttr
    angleReader.baseMatrix_mAttr = mAttr.create("baseMatrix", "bm", om.MFnMatrixAttribute.kDouble)
    angleReader.addAttribute(angleReader.baseMatrix_mAttr)

    # driverMatrix_mAttr
    angleReader.driverMatrix_mAttr = mAttr.create("driverMatrix", "dm", om.MFnMatrixAttribute.kDouble)
    angleReader.addAttribute(angleReader.driverMatrix_mAttr)

    # baseAxisX  - this should be kDouble in C++
    angleReader.baseAxisX_nAttr = nAttr.create("baseAxisX", "bax", om.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.baseAxisX_nAttr)

    # baseAxisY
    angleReader.baseAxisY_nAttr = nAttr.create("baseAxisY", "bay", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.baseAxisY_nAttr)

    # baseAxisZ
    angleReader.baseAxisZ_nAttr = nAttr.create("baseAxisZ", "baz", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.baseAxisZ_nAttr)

    # baseAxis
    angleReader.baseAxis_nAttr = nAttr.create("baseAxis", "ba",
                                              angleReader.baseAxisX_nAttr,
                                              angleReader.baseAxisY_nAttr,
                                              angleReader.baseAxisZ_nAttr)
    nAttr.setDefault(1.0, 0.0, 0.0)
    angleReader.addAttribute(angleReader.baseAxis_nAttr)

    # frontAxisX
    angleReader.frontAxisX_nAttr = nAttr.create("frontAxisX", "fax", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.frontAxisX_nAttr)

    # frontAxisY
    angleReader.frontAxisY_nAttr = nAttr.create("frontAxisY", "fay", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.frontAxisY_nAttr)

    # frontAxisZ
    angleReader.frontAxisZ_nAttr = nAttr.create("frontAxisZ", "faz", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.frontAxisZ_nAttr)

    # frontAxis
    angleReader.frontAxis_nAttr = nAttr.create("frontAxis", "fa",
                                               angleReader.frontAxisX_nAttr,
                                               angleReader.frontAxisY_nAttr,
                                               angleReader.frontAxisZ_nAttr)
    
    nAttr.setDefault(0.0, 1.0, 0.0)
    angleReader.addAttribute(angleReader.frontAxis_nAttr)


    # outAngle
    angleReader.outAngle_uAttr = uAttr.create("outAngle", "oa", om.MFnUnitAttribute.kAngle, 0.0)
    uAttr.setWritable(False)
    uAttr.setStorable(False)
    angleReader.addAttribute(angleReader.outAngle_uAttr)


    # outWeights
    angleReader.outWeights_nAttr = nAttr.create("outWeights", "otw", om.MFnNumericData.kDouble, 0.0)
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    nAttr.setArray(True)
    nAttr.setUsesArrayDataBuilder(True)
    angleReader.addAttribute(angleReader.outWeights_nAttr)

        
    # attributeAffects calls
    angleReader.attributeAffects(angleReader.baseMatrix_mAttr, angleReader.outAngle_uAttr)
    angleReader.attributeAffects(angleReader.driverMatrix_mAttr, angleReader.outAngle_uAttr)
    angleReader.attributeAffects(angleReader.baseAxis_nAttr, angleReader.outAngle_uAttr)
    angleReader.attributeAffects(angleReader.frontAxis_nAttr, angleReader.outAngle_uAttr)

    angleReader.attributeAffects(angleReader.baseMatrix_mAttr, angleReader.outWeights_nAttr)
    angleReader.attributeAffects(angleReader.driverMatrix_mAttr, angleReader.outWeights_nAttr)
    angleReader.attributeAffects(angleReader.baseAxis_nAttr, angleReader.outWeights_nAttr)
    angleReader.attributeAffects(angleReader.frontAxis_nAttr, angleReader.outWeights_nAttr)
    # angleReader.attributeAffects(angleReader.inputSettings_cAttr, angleReader.outWeights_nAttr)



# initialize the plugin
def initializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject,'Marin&Alex', '0.1', 'Any')
    try:
        mplugin.registerNode(pluginName, nodeId, nodeCreator ,nodeInit,ompx.MPxNode.kLocatorNode)

    except:
        raise Exception, 'Unable to register node: %s' %pluginName


# uninitializePlugin
def uninitializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(nodeId)
    except:
        sys.stderr.write( 'Failed to deregister node: %s' %pluginName)
        raise


# helper function to calculate the weight
def computeWeight(angle, preStart, start, end, postEnd, negate=False):
    output = 0.0

    if negate:
        angle *= -1.0

    if start <= angle <= end:
        output = 1.0

    elif preStart <= angle < start:
        output = (angle - preStart) / (start - preStart)

    elif end < angle <= postEnd:
        output = (angle - postEnd) / (end - postEnd)


    return output


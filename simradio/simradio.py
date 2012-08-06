#!/usr/bin/python
#coding:utf-8
# Author:  Dan-Erik Lindberg -- <simradio@dan-erik.com>
# Created: 2012-07-12
# License: GPL-3

# Main window class

# Major library imports
import numpy as np

# SIMRAD sonar support
import simrad


# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
os.environ["ETS_TOOLKIT"] = "qt4"
from pyface.qt import QtCore, QtGui

# Enthought library imports
from enable.api import Component, ComponentEditor
from traits.api import HasTraits, Instance, on_trait_change, Int, Dict
from traitsui.api import View, Item, Group
# These are the major Mayavi2 classes
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
# Chaco imports
################################################################################
# CHACO COLOR MAPS
################################################################################
# autumn is yellow-red 
# Blues is darkblue-white 
# bone is white-black 
# BrBG is green-white-brown 
# BuGn is green-white 
# BuPu is purple-blue-white 
# cool is magenta-cyan 
# copper is lightbrown-darkbrown 
# cw1_004 is blue-lavender-brown
# cw1_005 is green-orange-brown
# cw1_006 is green-purple
# cw1_028 is lightblue-darkblue
# flag is random US-flag (red,blue,white,black)
# gist_earth is white-brown-green-blue
# gist_gray is white-black
# gist_heat is white-yellow-red-black
# gist_ncar is white-purple-red-yellow-green-cyan-blue-darkgreen
# gist_rainbow is magenta-blue-green-yellow-red
# gist_stern is white-yellow-purple-red-black
# gist_yarg is black-white
# gmt_drywet is blue-indigo-cyan-green-orange-brown (altitude map)
# GnBu is blue-green-white
# gray is white-black
# Greens is green-white
# Greys is black-white
# hot is white-yellow-red-black
# hsv is red-magenta-purple-blue-cyan-green-yellow-orange-red
# jet is brown-red-orange-yellow-green-cyan-blue-indigo
# Oranges is brown-white
# OrRd is red-brown-white
# pink is white-oldpink-brown
# PiYG is green-white-pink
# PRGn is green-white-purple
# prism is random bright colors
# PuBu is blue-gray-white
# PuBuGn is green-blue-gray-white
# Spectral is purple-blue-green-yellow-orange-red
# spring is yellow-pink
# summer is yellow-green
# winter is icegreen-blue
# yarg is black-white
################################################################################
from chaco.api import ArrayPlotData, Plot, reverse, Spectral
from chaco.tools.api import PanTool, ZoomTool, RegressionLasso, RegressionOverlay


################################################################################
#The Mayavi 3D visualization
class MayaviVisualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    #----------------------------------------------------------------------
    @on_trait_change('scene.activated')
    def update_plot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        # We can do normal mlab calls on the embedded scene.
        self.scene.mlab.test_points3d()

    # the layout of the dialog screated
    view = View(
                Item(
                    'scene', 
                    editor=SceneEditor(scene_class=MayaviScene),
                    height=600, 
                    width=600, 
                    show_label=False),
                resizable=True)


################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
# Just copied from the Mayavi Wiki page, but changed to OO code (super()).
class MayaviQWidget(QtGui.QWidget):
    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        super(MayaviQWidget, self).__init__()
        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(0)
        self.setMinimumSize(600,600)
        self.visualization = MayaviVisualization()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)

################################################################################
# Create the Chaco plot.
def _create_plot_component():
    pd = ArrayPlotData(x=np.random.random(100), y=np.random.random(100))
    # Create some line plots of some of the data
    plot = Plot(pd)
    # Create a scatter plot and get a reference to it (separate from the
    # Plot object) because we'll need it for the regression tool below.
    scatterplot = plot.plot(("x", "y"), color="blue", type="scatter")[0]
    # Tweak some of the plot properties
    plot.padding = 50
    # Attach some tools to the plot
    plot.tools.append(PanTool(plot, drag_button="right"))
    plot.overlays.append(ZoomTool(plot))
    # Add the regression tool and overlay.  These need to be added
    # directly to the scatterplot instance (and not the Plot instance).
    regression = RegressionLasso(scatterplot, selection_datasource=scatterplot.index)
    scatterplot.tools.append(regression)
    scatterplot.overlays.append(RegressionOverlay(scatterplot, lasso_selection=regression))
    return plot

################################################################################
# Visualization classes for Chaco plots.
class TopDownView(HasTraits):
    plot = Instance(Component)
    traits_view = View(
                        Item('plot', 
                             editor=ComponentEditor(size=(300,100)),
                             height=300,
                             width=100,
                             show_label=False),
                    resizable=True)
    def _plot_default(self):
         return _create_plot_component()
################################################################################
class SideView(HasTraits):
    plot = Instance(Component)
    traits_view = View(
                        Item('plot', 
                             editor=ComponentEditor(size=(300,100)),
                             height=100,
                             width=300,
                             show_label=False),
                    resizable=True)
    def _plot_default(self):
         return _create_plot_component()

################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
# Just copied the Mayavi widget and modified it.
class ChacoQWidget(QtGui.QWidget):
    #----------------------------------------------------------------------
    def __init__(self, parent=None,choice="TopDown"):
        super(ChacoQWidget, self).__init__()
        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(0)
        #layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        if choice == "TopDown":
            self.visualization = TopDownView()
            self.setMinimumSize(100, 300)
            self.setSizeIncrement(1,3)
        elif choice == "Side":
            self.visualization = SideView()
            self.setMinimumSize(300, 100)
            self.setSizeIncrement(3,1)

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)

########################################################################
class Window(QtGui.QMainWindow):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(Window, self).__init__(parent)
        self.setWindowTitle("SimradIO")
        self.central = QtGui.QWidget()
        self.layout = QtGui.QGridLayout(self.central)

        # Mayavi widget for 3D
        self.mayavi_widget = MayaviQWidget(self.central)
        # Chaco top-down view
        self.chaco_widget1 = ChacoQWidget(self.central, "TopDown")
        # Chaco side view
        self.chaco_widget2 = ChacoQWidget(self.central, "Side")

        self.layout.addWidget(self.mayavi_widget, 1, 1)
        self.layout.addWidget(self.chaco_widget1, 1, 2)
        self.layout.addWidget(self.chaco_widget2, 2, 1)
        self.setCentralWidget(self.central)
        self.central.show()
        
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateplots)
        self.timer.start(1000)
        
        # test raw file reading
        sonar = simrad.ek60()
        head = sonar.read_fileheader("..\\rawsample\\sample.raw")
        data = sonar.read_filedata("..\\rawsample\\sample.raw")
        self.textedit = QtGui.QTextEdit()
        self.textedit.setText(head["dgType"] + '\n' + head["datetext"] + '\n' + str(head["transceivercount"]))
        self.layout.addWidget(self.textedit)

    def updateplots(self):
        x = np.sort(np.random.random(100))
        y = np.random.random(100)
        color = np.exp(-(x**2+y**2)) #np.random.random(100)
        pd = ArrayPlotData()
        pd.set_data("index",x)
        pd.set_data("value",y)
        pd.set_data("color",color)
        # Create some line plots of some of the data
        plot = Plot(pd)
        # Create a scatter plot and get a reference to it (separate from the
        # Plot object) because we'll need it for the regression tool below.
        scatterplot = plot.plot(("index","value","color"), type="cmap_scatter",color_mapper=reverse(Spectral),marker = "square",fill_alpha = 0.9,marker_size=6,bgcolor=QtGui.QColor(240,240,240))[0]
        # Tweak some of the plot properties
        plot.padding = 50
        # Attach some tools to the plot
        plot.tools.append(PanTool(plot, drag_button="right"))
        plot.overlays.append(ZoomTool(plot))
        # Add the regression tool and overlay.  These need to be added
        # directly to the scatterplot instance (and not the Plot instance).
        regression = RegressionLasso(scatterplot, selection_datasource=scatterplot.index)
        scatterplot.tools.append(regression)
        scatterplot.overlays.append(RegressionOverlay(scatterplot, lasso_selection=regression))
        self.chaco_widget1.visualization.plot = plot
        self.chaco_widget2.visualization.plot = plot

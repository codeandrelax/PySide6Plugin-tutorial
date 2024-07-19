
import os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

from customcompass import CustomCompass

from PySide6.QtDesigner import  QDesignerCustomWidgetInterface
from PySide6.QtGui import QIcon


DOM_XML = """
<ui language='c++'>
    <widget class='CustomCompass' name='customcompass'/>
</ui>
"""

class CustomCompassPlugin(QDesignerCustomWidgetInterface):
    def __init__(self):
        super().__init__()
        self._form_editor = None

    def createWidget(self, *args, **kwargs):
        t = CustomCompass(*args, **kwargs)
        return t

    def domXml(self):
        return DOM_XML

    def group(self):
        return 'Custom Compass Widgets'

    def icon(self):
        imgLocation = os.path.join(CURRENT_DIR,'compassIcon.ico')
        return QIcon(imgLocation)

    def includeFile(self):
        return 'customcomopass'

    def initialize(self, form_editor):
        self._form_editor = form_editor

    def isContainer(self):
        return False

    def isInitialized(self):
        return self._form_editor is not None

    def name(self):
        return 'CustomCompass'

    def toolTip(self):
        return 'This is a custom compass plugin developet for the purposes of the tutorial'

    def whatsThis(self):
        return self.toolTip()

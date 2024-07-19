
from customcompassplugin import CustomCompassPlugin

from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection


if __name__ == '__main__':
    QPyDesignerCustomWidgetCollection.addCustomWidget(CustomCompassPlugin())
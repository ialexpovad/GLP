# GLP - General Library of Povod Alex

This is library provides a pre-build custom application with framework PyQt5.

## Layout preview


## Automatic
Go to the [releases section](https://github.com/ialexpovod/GLP/releases)  of this repository and download the package for yourself.

## Manual
### Windows
1. Clone this repository
2. Add `GLP` to environment variable `[Your disk]:\[path to saving]\GLP` or create `namefile.py` for using `library GLP`
3. Example code:
```py
from GLP import *
import GLP

import sys

# import qt Modules
from PyQt5.Qt import QApplication, QClipboard 
from PyQt5 import QtWidgets,QtCore,QtGui,Qt

# Qt designer
from ui import Ui_MainWindow

class MainApp(GLPMainApp):
    def __init__(self, args):
        super(MainApp, self).__init__(args)
        # ... your code
class MainWindow(GLPWindow, Ui_MainWindow):
    def __init__(self, MainApp, parent = None):
        super(MainWindow, self).__init__(parent)
        # ...your code
        

if __name__ == "__main__":
    application = MainApp([])
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())
```

## Contributing 


## License
GLP is available under MIT License. See the [LICENSE](https://github.com/ialexpovod/GLP/blob/main/LICENSE) file for more information.





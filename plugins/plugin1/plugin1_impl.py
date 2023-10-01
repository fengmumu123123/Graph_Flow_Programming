from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QFileDialog


class Plugin1:
    def __init__(self, app):
        # 插件初始化，需要一个app参数作为主应用的引用
        self.app = app
        self.file_menu = None  # 文件菜单的初始化

    def load(self):
        # 加载插件时添加一个文件菜单到主应用
        self.file_menu = self.app.menu_bar.addMenu("文件")

        # 在文件菜单中添加一个"打开"操作
        open_action = QAction("打开文件", self.app)
        open_action.triggered.connect(self.open_file)
        self.file_menu.addAction(open_action)
        print('插件1加载成功')
    def open_file(self):
        # 打开文件对话框并打印所选文件的名称
        file_name, _ = QFileDialog.getOpenFileName(self.app, "打开文件")
        if file_name:
            print(f"选中了文件: {file_name}")

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog
import os


class Plugin2:
    def __init__(self, app):
        # 插件初始化，需要一个app参数作为主应用的引用
        self.app = app

    def load(self):
        # 加载插件2时，在插件1的文件菜单中添加一个选择文件夹的操作
        print('插件2加载成功')
        plugin1 = self.app.plugin_manager.mediator.get_plugin('plugin1')
        print(plugin1)
        if plugin1 and plugin1.file_menu:
            select_folder_action = QAction("选择文件夹", self.app)
            select_folder_action.triggered.connect(self.select_folder)
            plugin1.file_menu.addAction(select_folder_action)

    def select_folder(self):
        # 打开选择文件夹对话框并打印所选文件夹的内容
        folder_name = QFileDialog.getExistingDirectory(self.app, "选择文件夹")
        if folder_name:
            print(f"选中了文件夹: {folder_name}")
            for root, dirs, files in os.walk(folder_name):
                print(f"目录: {root}")
                for file in files:
                    print(f"文件: {file}")

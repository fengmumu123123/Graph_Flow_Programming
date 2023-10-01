from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog
import os


class Plugin2:
    def __init__(self, app):
        # 插件初始化，需要一个app参数作为主应用的引用
        self.app = app

    def load(self):
        # 获取插件1创建的子菜单
        plugin1 = self.app.plugin_manager.mediator.get_plugin('plugin1')
        # 检查Plugin1是否存在且已经创建了file_menu
        print(plugin1)
        if plugin1 and hasattr(plugin1, 'plugin_test_menu') and plugin1.plugin_test_menu:
            # 创建一个新的"选择文件夹"操作
            select_folder_action = QAction("插件中介测试", self.app)
            select_folder_action.triggered.connect(self.test_function)

            # 在Plugin1的插件测试菜单中添加新的操作
            plugin1.plugin_test_menu.addAction(select_folder_action)
            print('插件2加载成功')
        else:
            print('插件2加载失败，因为找不到插件1的子菜单')

    def select_folder(self):
        # 打开选择文件夹对话框并打印所选文件夹的内容
        folder_name = QFileDialog.getExistingDirectory(self.app, "选择文件夹")
        if folder_name:
            print(f"选中了文件夹: {folder_name}")
            for root, dirs, files in os.walk(folder_name):
                print(f"目录: {root}")
                for file in files:
                    print(f"文件: {file}")

    def test_function(self):
        print("插件2测试操作被点击了!")


from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QFileDialog


class Plugin1:
    def __init__(self, app):
        """
        初始化插件1.

        :param app: 主应用的引用，允许插件访问主应用的功能和属性
        """

        # 主应用的引用，提供对主应用功能的访问
        self.app = app

        # 插件1创建的子菜单的引用，其他插件（例如插件2）可能会使用它
        self.plugin_test_menu = None

        # 插件1可能使用或修改的主应用的主菜单的引用
        self.main_menu = None

        # 插件1可能提供的示例功能的引用，这只是为了示范，并不是真正的函数或方法
        self.example_function = None

    def load(self):
        # 在主应用的菜单栏中添加一个新的菜单"插件测试"
        self.main_menu = self.app.main_menu

        # 创建一个子菜单并添加到主菜单中
        self.plugin_test_menu = QMenu("插件测试", self.app)
        self.main_menu.addMenu(self.plugin_test_menu)

        # 可以为这个子菜单添加菜单项，或者留给其他插件添加
        example_action = QAction("插件1测试", self.app)
        example_action.triggered.connect(test_function)  # 点击测试
        self.plugin_test_menu.addAction(example_action)

        # 从主应用获取文件菜单
        file_menu = self.app.file_menu
        # 在文件菜单中添加一个"打开"操作
        open_action = QAction("打开文件", self.app)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        print('插件1加载成功')

    def open_file(self):
        # 打开文件对话框并打印所选文件的名称
        file_name, _ = QFileDialog.getOpenFileName(self.app, "打开文件")
        if file_name:
            print(f"选中了文件: {file_name}")


def test_function(self):
    print("插件1测试操作被点击了!")

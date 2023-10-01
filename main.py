import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit, QToolBar, QVBoxLayout, QWidget, \
    QMenuBar, QMenu, QStatusBar, QLabel
from PySide6.QtCore import Qt

from core.plugin_manager import PluginManager
from plugin_manager_dialog import PluginManagerDialog


class MainAppWindow(QMainWindow):
    def __init__(self):
        # 主应用窗口的初始化
        super().__init__()
        self.plugin_manager_dialog = None
        self.setWindowTitle("我的图形应用")
        # 中间工作区
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)

        # 主菜单栏
        self.main_menu = QMenuBar(self)
        self.file_menu = QMenu("文件", self)
        self.edit_menu = QMenu("编辑", self)
        self.view_menu = QMenu("查看", self)

        # 添加到主菜单栏
        self.main_menu.addMenu(self.file_menu)
        self.main_menu.addMenu(self.edit_menu)
        self.main_menu.addMenu(self.view_menu)

        # 为文件菜单添加选项
        save_action = QAction("保存", self)
        self.file_menu.addAction(save_action)

        self.setMenuBar(self.main_menu)

        # 状态栏
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        # 左侧工具栏
        self.left_toolbar = QToolBar("左侧工具栏", self)
        self.addToolBar(Qt.LeftToolBarArea, self.left_toolbar)

        # 右侧工具栏
        self.right_toolbar = QToolBar("右侧工具栏", self)
        self.addToolBar(Qt.RightToolBarArea, self.right_toolbar)

        # 左侧浮动窗口
        self.left_dock = QDockWidget("左侧浮动窗口", self)
        self.left_panel = QWidget(self.left_dock)
        self.left_dock.setWidget(self.left_panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)

        # 右侧浮动窗口
        self.right_dock = QDockWidget("右侧浮动窗口", self)
        self.right_panel = QWidget(self.right_dock)
        self.right_dock.setWidget(self.right_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)

        # 底部控制台输出栏
        self.console_output = QTextEdit(self)
        self.central_layout.addWidget(self.console_output)

        # 创建插件菜单
        self.plugins_menu = QMenu("插件", self)
        self.main_menu.addMenu(self.plugins_menu)

        # 创建插件设置选项
        self.plugin_setting_action = QAction("设置", self)
        self.plugin_setting_action.triggered.connect(self.show_plugin_manager)
        self.plugins_menu.addAction(self.plugin_setting_action)
        # 创建插件管理器并加载所有插件
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_plugins()



    def log_to_console(self, message: str):
        """向控制台输出栏添加日志信息。"""
        self.console_output.append(message)

        # 创建插件管理器并加载所有插件

    def show_plugin_manager(self):
        """显示插件管理对话框"""
        self.plugin_manager_dialog = PluginManagerDialog(self.plugin_manager)
        self.plugin_manager_dialog.exec()

def main():
    # 主函数，用于启动GUI应用
    app = QApplication([])
    main_window = MainAppWindow()
    main_window.show()
    app.exec()


if __name__ == "__main__":
    # 当直接运行这个脚本时，启动GUI应用
    main()
# main_app.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QMenuBar

from core.plugin_manager import PluginManager


class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("我的图形应用")  # 设置主应用窗口的标题
        label = QLabel("欢迎使用主应用！", self)  # 创建一个标签作为欢迎信息
        label.setAlignment(Qt.AlignCenter)  # 设置标签居中
        self.setCentralWidget(label)

        self.menu_bar = QMenuBar(self)  # 创建菜单条
        self.setMenuBar(self.menu_bar)  # 将菜单条设置为窗口的菜单条
        self.plugin_manager = PluginManager(self)  # 初始化插件管理器
        self.plugin_manager.load_plugins()  # 加载所有插件


def main():
    app = QApplication([])  # 创建应用实例
    main_window = MainAppWindow()  # 创建并初始化主窗口实例
    main_window.show()  # 显示主窗口
    app.exec()  # 开始GUI应用的事件循环


if __name__ == "__main__":
    main()

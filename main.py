from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QMenuBar

from core.plugin_manager import PluginManager


class MainAppWindow(QMainWindow):
    def __init__(self):
        # 主应用窗口的初始化
        super().__init__()
        self.setWindowTitle("我的图形应用")

        # 添加一个欢迎标签到窗口中
        label = QLabel("欢迎使用主应用！", self)
        self.setCentralWidget(label)

        # 创建一个菜单条
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # 创建插件管理器并加载所有插件
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_plugins()

def main():
    # 主函数，用于启动GUI应用
    app = QApplication([])
    main_window = MainAppWindow()
    main_window.show()
    app.exec()

if __name__ == "__main__":
    # 当直接运行这个脚本时，启动GUI应用
    main()

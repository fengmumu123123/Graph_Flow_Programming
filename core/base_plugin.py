# base_plugin.py

class BasePlugin:
    def __init__(self, main_window):
        self.main_window = main_window  # 插件保存主窗口的引用

    def load(self):
        """插件的加载方法，子类可以根据需要进行覆盖"""
        pass

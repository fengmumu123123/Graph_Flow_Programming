from importlib.metadata import entry_points

from core.mediator import PluginMediator


class PluginManager:
    def __init__(self, app):
        # 初始化插件管理器，需要一个app参数作为主应用的引用
        self.app = app
        # 创建一个中介者实例来帮助管理插件间的交互
        self.mediator = PluginMediator()

    def load_plugins(self):
        # 从入口点加载所有插件
        plugins = self._discover_plugins()
        for name, PluginClass in plugins.items():
            # 对于每一个找到的插件，都实例化并加载它
            plugin_instance = PluginClass(self.app)
            self.mediator.register(name, plugin_instance)  # 使用中介者注册插件实例
            print(f'加载的插件: {name}')
            plugin_instance.load()  # 调用插件的加载方法

    def _discover_plugins(self):
        # 从入口点获取所有已注册的插件
        entries = entry_points(group='my_app_plugins')
        # 返回一个插件名称到其实现类的映射字典
        return {entry.name: entry.load() for entry in entries}

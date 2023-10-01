import json
from importlib.metadata import metadata

from importlib_metadata import entry_points

from core.mediator import PluginMediator


class PluginManager:
    def __init__(self, app):
        self.app = app  # 将应用实例保存为属性，以便其他方法可以访问
        self.mediator = PluginMediator()  # 初始化插件中介者实例
        self.enabled_plugins = set()
        self.all_plugins = self._discover_plugins()
        self.config_path = 'plugins_config.json'
        self.load_enabled_plugins()  # 加载启用的插件

    def load_plugins(self):
        # 获取所有已注册的插件
        all_plugins = self._discover_plugins()
        # 仅选择在配置文件中启用的插件
        plugins_to_load = {name: all_plugins[name] for name in self.enabled_plugins if name in all_plugins}
        # 根据它们的依赖关系对插件进行排序
        sorted_plugins = self._sort_plugins_by_dependency(plugins_to_load)

        # 按排序后的顺序加载每个插件
        for name in sorted_plugins:
            # 从字典中获取插件类
            plugin_class = plugins_to_load[name]
            # 创建插件实例
            plugin_instance = plugin_class(self.app)
            # 在中介者中注册插件实例
            self.mediator.register(name, plugin_instance)
            # 调用插件的加载方法
            plugin_instance.load()

    def _sort_plugins_by_dependency(self, plugins: dict) -> list:
        """
        根据插件之间的依赖关系对插件进行排序。
        如果插件A依赖于插件B，那么插件B应该在插件A之前加载。

        :param plugins: 一个字典，其中键是插件的名称，值是插件的实例。
        :return: 一个包含插件名称的列表，这些插件是按照依赖关系排序的。
        """
        sorted_plugins = []  # 结果列表，按依赖关系排序的插件名称
        visited = set()  # 已经访问过的插件名称

        def process(plugin_name):
            """递归函数，处理每个插件和它的依赖关系"""
            if plugin_name not in visited:
                visited.add(plugin_name)

                # 使用importlib_metadata获取插件的元数据
                plugin_dist = metadata(plugin_name)
                # 从元数据中获取依赖关系
                dependencies = plugin_dist.get('Requires-Dist', [])

                # 将依赖关系转换为我们预期的格式
                dependencies = [dep.split(' ')[0] for dep in dependencies if dep in plugins]

                for dep in dependencies:
                    process(dep)

                sorted_plugins.append(plugin_name)

        for name in plugins:
            process(name)

        return sorted_plugins

    def _discover_plugins(self):
        # 从入口点获取所有已注册的插件
        entries = entry_points(group='my_app_plugins')
        # 返回一个插件名称到其实现类的映射字典
        return {entry.name: entry.load() for entry in entries}

    def load_enabled_plugins(self):
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_content = f.read().strip()
                if not config_content:
                    self.enabled_plugins = set()
                else:
                    config = json.loads(config_content)
                    self.enabled_plugins = set(config.get('enabled_plugins', []))
        except FileNotFoundError:
            self.enabled_plugins = set()

    def save_enabled_plugins(self):
        """将启用的插件列表保存到配置文件"""
        print(f"将启用的插件保存到: {self.config_path}")  # 输出保存路径
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                print("启用插件:", list(self.enabled_plugins))  # 输出启用的插件
                json.dump({"enabled_plugins": list(self.enabled_plugins)}, f, indent=4)
                print("成功保存启用的插件！")  # 输出成功信息
        except Exception as e:
            print(f"保存时出错：{e}")  # 输出错误信息

    @property
    def installed_plugins(self):
        return set(ep.name for ep in entry_points().select(group='my_app_plugins'))

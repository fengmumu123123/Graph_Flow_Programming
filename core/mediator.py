class PluginMediator:
    def __init__(self):
        # 初始化一个空的插件字典来存储插件实例
        self.plugins = {}

    def register(self, name, plugin):
        """注册插件到中介者中"""
        # 注册/添加插件到字典中
        self.plugins[name] = plugin

    def get_plugin(self, name):
        """获取指定名称的插件"""
        # 从字典中获取指定名称的插件实例
        return self.plugins.get(name, None)

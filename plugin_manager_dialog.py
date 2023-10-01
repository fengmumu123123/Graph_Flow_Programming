from PySide6.QtWidgets import QPushButton, QCheckBox, QLabel, QHBoxLayout, QVBoxLayout, QDialog


class PluginManagerDialog(QDialog):
    def __init__(self, plugin_manager, parent=None):
        super().__init__(parent)
        self.temp_enabled_plugins = None
        self.plugin_manager = plugin_manager
        self.setWindowTitle("插件管理")

        self.layout = QVBoxLayout(self)

        self.update_plugin_list()

        self.setLayout(self.layout)
        self.temp_enabled_plugins = set(self.plugin_manager.enabled_plugins)  # 初始化为当前已启用的插件集合

    def update_plugin_list(self):
        # 首先清除布局中的所有小部件
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for plugin_name, plugin_class in self.plugin_manager.all_plugins.items():
            # 创建一个水平布局以容纳标签和复选框
            hbox = QHBoxLayout()

            # 标签显示插件名称
            label = QLabel(plugin_name)
            hbox.addWidget(label)

            # 标签显示是否已安装
            if plugin_name in self.plugin_manager.installed_plugins:
                status_label = QLabel("已安装")
            else:
                status_label = QLabel("未安装")
            hbox.addWidget(status_label)

            # 复选框控制是否加载插件
            checkbox = QCheckBox("加载")
            checkbox.setChecked(plugin_name in self.plugin_manager.enabled_plugins)
            checkbox.stateChanged.connect(lambda state, name=plugin_name: self.toggle_plugin(name, state))
            hbox.addWidget(checkbox)

            # 将水平布局添加到主布局中
            self.layout.addLayout(hbox)

        # 添加一个应用按钮，当点击时保存配置
        apply_button = QPushButton("应用")
        apply_button.clicked.connect(self.apply_changes)
        self.layout.addWidget(apply_button)

    def toggle_plugin(self, name, state):
        """启用或禁用插件"""
        print("插件", name, "已", state)
        if state == 2:
            self.temp_enabled_plugins.add(name)
        else:
            self.temp_enabled_plugins.discard(name)

    def apply_changes(self):
        """保存启用的插件列表到配置文件并关闭对话框"""
        print("启用插件列表：", self.temp_enabled_plugins)

        self.plugin_manager.enabled_plugins = self.temp_enabled_plugins
        self.plugin_manager.save_enabled_plugins()
        self.accept()

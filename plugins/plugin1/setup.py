# plugins/plugin1/setup.py

from setuptools import setup, find_packages

setup(
    name="plugin1",  # 插件名称
    version="0.1",  # 插件版本号
    packages=find_packages(),  # 自动发现并包括所有包
    install_requires=[  # 依赖项
        'PySide6',
        'importlib_metadata',
        'setuptools',
        'PySide6',
        'importlib_resources'
    ],
    package_data={
        'plugins.plugin1': ['resources/*'],  # 包括插件的所有资源文件
    },
    entry_points={
        'my_app_plugins': [  # 定义插件的入口点
            'plugin1 = plugin1_impl:Plugin1',  # 插件的入口点及其对应的实现类
        ],
    },
)

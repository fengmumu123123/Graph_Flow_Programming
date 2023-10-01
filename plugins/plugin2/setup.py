from setuptools import setup, find_packages

setup(
    name="plugin2",  # 插件名称
    version="0.1",  # 插件版本号
    packages=find_packages(),  # 自动发现并包括所有包
    install_requires=[
        'PySide6',
        'plugin1'
    ],
    extras_require={
        'dependencies': ['plugin1'],  # 定义插件2依赖于插件1
    },
    entry_points={
        'my_app_plugins': [  # 定义插件的入口点
            'plugin2 = plugin2_impl:Plugin2',  # 插件的入口点及其对应的实现类
        ],
    },
)

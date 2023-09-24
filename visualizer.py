from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QShortcut, QImage, QPixmap, QKeySequence, QPainter
from PySide6.QtCore import Qt
from io import BytesIO
from analyzer import CodeAnalyzer
import matplotlib.pyplot as plt
import networkx as nx


class CodeFlowVisualizer(QMainWindow):

    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.initUI()

    def initUI(self):
        """初始化用户界面"""
        self.setWindowTitle('Python Code Flow Visualizer')
        self.setGeometry(100, 100, 800, 600)

        # 创建一个QGraphicsView来展示流程图，并设置其拖放和缩放属性
        self.view = QGraphicsView(self)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.view.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 设置快捷键用于重置视图
        reset_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        reset_shortcut.activated.connect(self.reset_view)

        self.setCentralWidget(self.view)
        self.draw_graph_to_view()

    def draw_graph_to_view(self):
        """绘制流程图到QGraphicsView中"""
        plt.figure(figsize=(14, 12))
        pos = nx.spring_layout(self.graph, seed=42)

        # 根据边的类型（执行或变量传递）选择颜色和样式
        edges_execution = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d["edge_type"] == "execution"]
        edges_variable = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d["edge_type"] == "variable"]

        nx.draw_networkx_nodes(self.graph, pos, node_size=4500, node_color="lightblue")
        nx.draw_networkx_edges(self.graph, pos, edgelist=edges_execution, edge_color="gray", width=2)
        nx.draw_networkx_edges(self.graph, pos, edgelist=edges_variable, edge_color="red", width=2, style="dotted")
        nx.draw_networkx_labels(self.graph, pos, labels=nx.get_node_attributes(self.graph, 'label'), font_size=10)

        # 将图像保存到BytesIO对象中，然后加载到QPixmap中
        buf = BytesIO()
        plt.savefig(buf, format="PNG", dpi=100)
        buf.seek(0)
        image = QImage.fromData(buf.read())
        pixmap = QPixmap.fromImage(image)

        # 设置QGraphicsView的场景为该图像
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.view.setScene(scene)
        self.view.setSceneRect(pixmap.rect())
        self.view.fitInView(self.view.sceneRect(), Qt.KeepAspectRatio)
        self.view.show()

    def wheelEvent(self, event):
        """处理滚轮事件以放大或缩小图像"""
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # 设置缩放中心为鼠标的当前位置
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if event.angleDelta().y() > 0:
            self.view.scale(zoomInFactor, zoomInFactor)
        else:
            self.view.scale(zoomOutFactor, zoomOutFactor)

    def reset_view(self):
        """重置视图到原始大小"""
        self.view.resetTransform()
        self.view.fitInView(self.view.sceneRect(), Qt.KeepAspectRatio)


if __name__ == "__main__":
    app = QApplication([])
    analyzer = CodeAnalyzer()
    code = """from pymodbus.client.sync import ModbusSerialClient
import time

# 1. 设置串口和数据收集参数
PORT = 'COM3'  # 修改为您的实际串口号
BAUDRATE = 9600
TIMEOUT = 1  # 响应超时时间（秒）

DEVICE_ADDRESSES = list(range(1, 255))  # 假设设备地址从1到254
TEMPERATURE_REGISTER = 0x300
HUMIDITY_REGISTER = 0x301
COLLECTION_INTERVAL = 60  # 每60秒收集一次数据


def discover_devices(port, addresses):
    
    active_devices = []
    print(
    )
    # 创建一个Modbus客户端实例
    client = ModbusSerialClient(method='rtu', port=port, baudrate=BAUDRATE, bytesize=8, parity='N', stopbits=1,
                                timeout=TIMEOUT)

    # 尝试连接到设备
    if not client.connect():
        print("无法连接到串口。请检查连接设置。")
        return []

    for address in addresses:
        try:
            # 尝试从一个注册表读取数据作为测试
            result = client.read_input_registers(TEMPERATURE_REGISTER, 1, unit=address)
            if result.isError():
                continue
            # 读取温度作为测试
            temperature = result.registers[0]
            active_devices.append(address)
            print(f"成功连接到地址为 {address} 的设备，读取的温度为: {temperature}")
        except Exception as e:
            print(f"连接到地址为 {address} 的设备时出现错误: {e}")

    client.close()
    return active_devices


# 输出查找的结果
if __name__ == "__main__":
    print(discover_devices(PORT, DEVICE_ADDRESSES))
                                              """
    graph = analyzer.generate_graph(code)
    window = CodeFlowVisualizer(graph)
    window.show()
    app.exec()

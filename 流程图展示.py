import networkx as nx
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtGui import QPen, QColor, QTransform
from PySide6.QtCore import Qt, QPointF

from 流程图 import DetailedCodeToGraph


class DraggableNode(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, label, parent=None):
        # 调用父类初始化函数
        super(DraggableNode, self).__init__(x, y, w, h, parent)
        # 设置该节点为可移动
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        # 设置该节点在移动时发送位置改变信号
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges, True)
        # 为节点添加文本标签
        self.label = QGraphicsTextItem(label, self)
        self.label.setPos(x + w/4, y + h/4)
        # 存储与该节点连接的边
        self.edges = []

    # 添加与该节点连接的边
    def add_edge(self, edge):
        self.edges.append(edge)

    # 当节点位置改变时，调整与其连接的边的位置
    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.ItemPositionChange:
            for edge in self.edges:
                edge.adjust()
        return super(DraggableNode, self).itemChange(change, value)


# 定义边类，继承自 QGraphicsLineItem
class Edge(QGraphicsLineItem):
    def __init__(self, source_node, dest_node):
        super(Edge, self).__init__()
        self.source_node = source_node  # 边的起始节点
        self.dest_node = dest_node      # 边的结束节点
        self.source_node.add_edge(self)
        self.dest_node.add_edge(self)
        self.adjust()

    # 调整边的位置以匹配连接的节点的位置
    def adjust(self):
        line = self.line()
        src_point = self.source_node.pos()
        dest_point = self.dest_node.pos()
        self.setLine(src_point.x(), src_point.y(), dest_point.x(), dest_point.y())


# 定义交互式流程图的主窗口类，继承自 QMainWindow
class InteractiveGraph(QMainWindow):
    def __init__(self, graph, parent=None):
        super(InteractiveGraph, self).__init__(parent)
        self.graph = graph  # 存储流程图的数据
        self.initUI()       # 初始化用户界面

    # 初始化用户界面
    def initUI(self):
        # 创建一个QGraphicsScene，用于管理所有的图形项
        self.scene = QGraphicsScene()
        # 创建一个QGraphicsView，用于显示场景内容
        self.view = QGraphicsView(self.scene)

        # 根据流程图数据创建节点和边
        nodes = {}
        for node in self.graph.nodes:
            item = DraggableNode(-30, -30, 60, 60, self.graph.nodes[node]['label'])
            nodes[node] = item
            self.scene.addItem(item)

        for edge in self.graph.edges:
            line = Edge(nodes[edge[0]], nodes[edge[1]])
            if 'style' in self.graph.edges[edge] and self.graph.edges[edge]['style'] == "dashed":
                pen = QPen(Qt.DashLine)
                line.setPen(pen)
            self.scene.addItem(line)

        # 设置窗口的布局和大小
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("交互式流程图")
        self.setGeometry(100, 100, 800, 600)


# 定义一个带初始布局的交互式流程图的主窗口类，继承自 InteractiveGraph
class InteractiveGraphWithLayout(InteractiveGraph):
    def initUI(self):
        # 调用父类的initUI方法
        super().initUI()

        # 为节点设置一个简单的网格布局
        row_spacing = 100
        col_spacing = 150
        nodes = {}
        positions = {}

        # 根据节点在图中的入度和出度为其分配行和列位置
        # 为了简化，我们使用节点的入度和出度（连接到节点的边的数量）来为其分配行和列
        for idx, node in enumerate(self.graph.nodes):
            in_degree = self.graph.in_degree(node)
            out_degree = self.graph.out_degree(node)
            positions[node] = (in_degree * col_spacing, out_degree * row_spacing)

        # 使用分配的位置创建节点
        for node in self.graph.nodes:
            x, y = positions[node]
            item = DraggableNode(x - 30, y - 30, 60, 60, self.graph.nodes[node]['label'])
            nodes[node] = item
            self.scene.addItem(item)

        # 创建边
        for edge in self.graph.edges:
            line = Edge(nodes[edge[0]], nodes[edge[1]])
            # 如果边的样式是虚线，则设置为虚线
            if 'style' in self.graph.edges[edge] and self.graph.edges[edge]['style'] == "dashed":
                pen = QPen(Qt.DashLine)
                line.setPen(pen)
            self.scene.addItem(line)


class InteractiveGraphWithSpringLayout(InteractiveGraph):
    def initUI(self):
        # 调用父类的initUI方法
        super().initUI()

        nodes = {}

        # 使用networkx的spring_layout布局算法为节点分配位置
        layout = nx.spring_layout(self.graph, seed=42)

        # 使用分配的位置创建节点
        for node, (x, y) in layout.items():
            item = DraggableNode(x * 500 - 30, y * 500 - 30, 60, 60, self.graph.nodes[node]['label'])
            nodes[node] = item
            self.scene.addItem(item)

        # 创建边
        for edge in self.graph.edges:
            line = Edge(nodes[edge[0]], nodes[edge[1]])
            # 如果边的样式是虚线，则设置为虚线
            if 'style' in self.graph.edges[edge] and self.graph.edges[edge]['style'] == "dashed":
                pen = QPen(Qt.DashLine)
                line.setPen(pen)
            self.scene.addItem(line)


class InteractiveGraphWithImprovedLayout(InteractiveGraph):
    def initUI(self):
        # 调用父类的initUI方法
        super().initUI()

        nodes = {}

        # 使用networkx的spring_layout布局算法为节点分配位置
        layout = nx.spring_layout(self.graph, seed=42, scale=500)

        # 使用分配的位置创建节点
        for node, (x, y) in layout.items():
            item = DraggableNode(x - 30, y - 30, 60, 60, self.graph.nodes[node]['label'])
            nodes[node] = item
            self.scene.addItem(item)

        # 创建边，并确保边的位置与节点的新位置匹配
        for edge in self.graph.edges:
            line = Edge(nodes[edge[0]], nodes[edge[1]])
            line.adjust()
            # 如果边的样式是虚线，则设置为虚线
            if 'style' in self.graph.edges[edge] and self.graph.edges[edge]['style'] == "dashed":
                pen = QPen(Qt.DashLine)
                line.setPen(pen)
            self.scene.addItem(line)


class ImprovedEdge(Edge):
    def adjust(self):
        # 获取源节点和目标节点的中心位置
        src_center = self.source_node.boundingRect().center() + self.source_node.pos()
        dest_center = self.dest_node.boundingRect().center() + self.dest_node.pos()
        self.setLine(src_center.x(), src_center.y(), dest_center.x(), dest_center.y())


# 更新InteractiveGraphWithImprovedLayout类，使用新的ImprovedEdge类
class InteractiveGraphWithCenteredEdges(InteractiveGraphWithImprovedLayout):
    def initUI(self):
        super().initUI()

        # 删除先前添加的边
        for item in self.scene.items():
            if isinstance(item, Edge):
                self.scene.removeItem(item)

        # 使用ImprovedEdge类重新创建边
        nodes = {node['label']: item for node, item in self.graph.nodes(data=True)}
        for edge in self.graph.edges:
            line = ImprovedEdge(nodes[self.graph.nodes[edge[0]]['label']], nodes[self.graph.nodes[edge[1]]['label']])
            if 'style' in self.graph.edges[edge] and self.graph.edges[edge]['style'] == "dashed":
                pen = QPen(Qt.DashLine)
                line.setPen(pen)
            self.scene.addItem(line)


# 更新InteractiveGraphWithCenteredEdges类，修复上述问题
class InteractiveGraphWithFixedEdges(InteractiveGraphWithImprovedLayout):
    def initUI(self):
        super().initUI()

        # 删除先前添加的边
        for item in self.scene.items():
            if isinstance(item, Edge):
                self.scene.removeItem(item)

        # 使用ImprovedEdge类重新创建边
        nodes = {self.graph.nodes[node]['label']: item for node, item in self.graph.nodes(data=True)}
        for edge in self.graph.edges:
            line = ImprovedEdge(nodes[self.graph.nodes[edge[0]]['label']], nodes[self.graph.nodes[edge[1]]['label']])
            if 'style' in self.graph.edges[edge] and self.graph.edges[edge]['style'] == "dashed":
                pen = QPen(Qt.DashLine)
                line.setPen(pen)
            self.scene.addItem(line)


# 更新InteractiveGraphWithFixedEdges类，修复上述问题
class InteractiveGraphWithCorrectedEdges(InteractiveGraphWithImprovedLayout):
    def initUI(self):
        super().initUI()

        # 删除先前添加的边
        for item in self.scene.items():
            if isinstance(item, Edge):
                self.scene.removeItem(item)

        # 使用ImprovedEdge类重新创建边
        draggable_nodes = {item.label: item for item in self.scene.items() if isinstance(item, DraggableNode)}
        for edge in self.graph.edges:
            line = ImprovedEdge(draggable_nodes[self.graph.nodes[edge[0]]['label']],
                                draggable_nodes[self.graph.nodes[edge[1]]['label']])
            if 'style' in self.graph.edges[edge] and self.graph.edges[edge]['style'] == "dashed":
                pen = QPen(Qt.DashLine)
                line.setPen(pen)
            self.scene.addItem(line)


# 重新定义InteractiveGraphWithCorrectedEdges类，修复上述问题
class InteractiveGraphWithFinalEdges(InteractiveGraphWithImprovedLayout):
    def initUI(self):
        super().initUI()

        # 删除先前添加的边
        for item in self.scene.items():
            if isinstance(item, Edge):
                self.scene.removeItem(item)

        # 使用ImprovedEdge类重新创建边
        draggable_nodes = {item.label: item for item in self.scene.items() if isinstance(item, DraggableNode)}

        # Double-check and ensure all nodes are present
        for node in self.graph.nodes():
            label = self.graph.nodes[node]['label']
            if label not in draggable_nodes:
                print(f"Missing node: {label}")

        # Create edges
        for edge in self.graph.edges:
            if self.graph.nodes[edge[0]]['label'] in draggable_nodes and self.graph.nodes[edge[1]][
                'label'] in draggable_nodes:
                line = ImprovedEdge(draggable_nodes[self.graph.nodes[edge[0]]['label']],
                                    draggable_nodes[self.graph.nodes[edge[1]]['label']])
                if 'style' in self.graph.edges[edge] and self.graph.edges[edge]['style'] == "dashed":
                    pen = QPen(Qt.DashLine)
                    line.setPen(pen)
                self.scene.addItem(line)
            else:
                print(
                    f"Missing edge between {self.graph.nodes[edge[0]]['label']} and {self.graph.nodes[edge[1]]['label']}")


# This is just for diagnostic purposes to check which nodes/edges might be missing
# You can integrate the InteractiveGraphWithFinalEdges class into your script and run it

app = QApplication([])
detailed_graph_generator = DetailedCodeToGraph()
detailed_graph_generator.generate_graph("""from pymodbus.client.sync import ModbusSerialClient
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
                                              """)

window = InteractiveGraphWithFinalEdges(detailed_graph_generator.graph)
window.show()
app.exec_()
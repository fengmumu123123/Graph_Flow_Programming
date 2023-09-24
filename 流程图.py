import ast
import json

import networkx as nx
import matplotlib.pyplot as plt


class RefinedCodeToGraph:

    def __init__(self):
        """初始化函数：创建一个有向图来表示代码流程"""
        self.graph = nx.DiGraph()
        self.current_node = None
        self.last_condition = None

    def add_node(self, node, label):
        """向图中添加节点并创建从当前节点到新节点的边"""
        prev_node = self.current_node
        self.current_node = label
        self.graph.add_node(self.current_node, label=label)
        if prev_node:
            self.graph.add_edge(prev_node, self.current_node)

    def visit_Import(self, node):
        """处理import语句"""
        for name in node.names:
            self.add_node(node, f"import {name.name}")

    def visit_ImportFrom(self, node):
        """处理from...import...语句"""
        for name in node.names:
            self.add_node(node, f"from {node.module} import {name.name}")

    def visit_Assign(self, node):
        """处理赋值语句"""
        targets = ' '.join([ast.dump(t) for t in node.targets])
        self.add_node(node, f"{targets} = ...")

    def visit_FunctionDef(self, node):
        """处理函数定义"""
        self.add_node(node, f"def {node.name}(...):")
        for statement in node.body:
            self.visit(statement)

    def visit_If(self, node):
        """处理if语句"""
        self.add_node(node, f"if {ast.dump(node.test)}:")
        self.last_condition = self.current_node
        for statement in node.body:
            self.visit(statement)

    def visit_While(self, node):
        """处理while循环"""
        self.add_node(node, f"while {ast.dump(node.test)}:")
        for statement in node.body:
            self.visit(statement)

    def visit_For(self, node):
        """处理for循环"""
        self.add_node(node, f"for {ast.dump(node.target)} in {ast.dump(node.iter)}:")
        for statement in node.body:
            self.visit(statement)

    def visit_Call(self, node):
        """处理函数调用"""
        self.add_node(node, f"{ast.dump(node.func)}(...)")

    def visit_Return(self, node):
        """处理return语句"""
        if node.value:
            self.add_node(node, f"return {ast.dump(node.value)}")
        else:
            self.add_node(node, "return")

    def visit_Try(self, node):
        """处理try语句"""
        self.add_node(node, "try:")
        for statement in node.body:
            self.visit(statement)
        for handler in node.handlers:
            self.visit(handler)
        for statement in node.orelse:
            self.visit(statement)
        for statement in node.finalbody:
            self.visit(statement)

    def visit_ExceptHandler(self, node):
        """处理except语句"""
        if node.type:
            self.add_node(node, f"except {node.type.id} as {node.name}:")
        else:
            self.add_node(node, "except:")
        for statement in node.body:
            self.visit(statement)

    def visit(self, node):
        """访问AST中的节点"""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor:
            visitor(node)

    def generate_graph(self, code):
        """根据给定的Python代码生成流程图"""
        tree = ast.parse(code)
        for node in ast.iter_child_nodes(tree):
            self.visit(node)
        return self.graph

    def draw_graph(self, code):
        """绘制给定Python代码的流程图"""
        graph = self.generate_graph(code)
        labels = nx.get_node_attributes(graph, 'label')
        plt.figure(figsize=(14, 12))
        pos = nx.spring_layout(graph, seed=42)
        nx.draw(graph, pos, with_labels=True, labels=labels,
                node_size=4500, node_color="lightblue", font_size=10,
                width=2, edge_color="gray")
        plt.show()


class DetailedCodeToGraph(RefinedCodeToGraph):

    def __init__(self):
        super().__init__()
        self.edge_styles = {}  # To store the style of edges (solid/dashed)

    def add_node(self, node, label, is_variable=False):
        """向图中添加节点并创建从当前节点到新节点的边"""
        prev_node = self.current_node
        self.current_node = label
        self.graph.add_node(self.current_node, label=label)
        if prev_node:
            self.graph.add_edge(prev_node, self.current_node)
            if is_variable:  # If this edge represents variable modification or assignment
                self.edge_styles[(prev_node, self.current_node)] = "dashed"
            else:
                self.edge_styles[(prev_node, self.current_node)] = "solid"
        if self.last_condition and node.__class__.__name__ not in ["If", "Elif", "Else"]:
            self.graph.add_edge(self.last_condition, self.current_node)
            self.edge_styles[(self.last_condition, self.current_node)] = "solid"
            self.last_condition = None

    def visit_Assign(self, node):
        """处理赋值语句，并使用虚线表示变量赋值"""
        targets = ' '.join([ast.dump(t) for t in node.targets])
        self.add_node(node, f"{targets} = ...", is_variable=True)

    def draw_graph(self, code):
        """绘制给定Python代码的流程图，考虑虚线和实线"""
        graph = self.generate_graph(code)
        labels = nx.get_node_attributes(graph, 'label')
        edge_colors = ["gray" if self.edge_styles[edge] == "solid" else "red" for edge in graph.edges()]
        edge_styles = ["solid" if self.edge_styles[edge] == "solid" else "dashed" for edge in graph.edges()]

        plt.figure(figsize=(14, 12))
        pos = nx.spring_layout(graph, seed=42)
        nx.draw(graph, pos, with_labels=True, labels=labels,
                node_size=4500, node_color="lightblue", font_size=10,
                width=2, edge_color=edge_colors, style=edge_styles)
        plt.show()


class CodeToD3JSON(DetailedCodeToGraph):

    def to_d3_json(self, code):
        """将给定的Python代码转换为适合D3.js的JSON格式"""
        graph = self.generate_graph(code)
        nodes = [{"id": node, "label": graph.nodes[node]['label']} for node in graph.nodes()]
        links = [{"source": edge[0], "target": edge[1], "type": self.edge_styles[edge]} for edge in graph.edges()]

        return json.dumps({"nodes": nodes, "links": links}, indent=4)
# 使用方法示例：
#generator = DetailedCodeToGraph()
#generator.draw_graph()


#generator = CodeToD3JSON()
#d3_json_data = generator.to_d3_json()
# print(d3_json_data)
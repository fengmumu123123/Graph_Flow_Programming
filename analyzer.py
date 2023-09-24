import ast

import networkx as nx


class CodeAnalyzer:

    def __init__(self):
        """初始化函数：创建一个有向图来表示代码流程和变量传递"""
        self.graph = nx.DiGraph()
        self.current_node = None
        self.last_condition = None

    def add_node(self, node, label, edge_type="execution"):
        """向图中添加节点并创建从当前节点到新节点的边"""
        prev_node = self.current_node
        self.current_node = label
        self.graph.add_node(self.current_node, label=label)
        if prev_node:
            self.graph.add_edge(prev_node, self.current_node, edge_type=edge_type)
        if self.last_condition and node.__class__.__name__ not in ["If", "Elif", "Else"]:
            self.graph.add_edge(self.last_condition, self.current_node, edge_type="execution")
            self.last_condition = None

    def visit_Import(self, node):
        for name in node.names:
            self.add_node(node, f"import {name.name}")

    def visit_ImportFrom(self, node):
        for name in node.names:
            self.add_node(node, f"from {node.module} import {name.name}")

    def visit_Assign(self, node):
        targets = ' '.join([ast.dump(t) for t in node.targets])
        self.add_node(node, f"{targets} = ...")

    def visit_FunctionDef(self, node):
        self.add_node(node, f"def {node.name}(...):")
        for statement in node.body:
            self.visit(statement)

    def visit_If(self, node):
        self.add_node(node, f"if {ast.dump(node.test)}:")
        self.last_condition = self.current_node
        for statement in node.body:
            self.visit(statement)

    def visit_While(self, node):
        self.add_node(node, f"while {ast.dump(node.test)}:")
        for statement in node.body:
            self.visit(statement)

    def visit_For(self, node):
        self.add_node(node, f"for {ast.dump(node.target)} in {ast.dump(node.iter)}:")
        for statement in node.body:
            self.visit(statement)

    def visit_Call(self, node):
        self.add_node(node, f"{ast.dump(node.func)}(...)")

    def visit_Return(self, node):
        if node.value:
            self.add_node(node, f"return {ast.dump(node.value)}")
        else:
            self.add_node(node, "return")

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

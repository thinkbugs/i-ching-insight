#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱 - 卦象语义网络
功能：构建卦象知识图谱、关系推理
"""

import argparse
import json
from collections import defaultdict

class KnowledgeGraph:
    """
    知识图谱
    """
    
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(list)
    
    def add_node(self, node_id, properties):
        """
        添加节点
        """
        self.nodes[node_id] = properties
    
    def add_edge(self, source, target, relation):
        """
        添加边
        """
        self.edges[source].append({
            "target": target,
            "relation": relation
        })
    
    def build_yijing_graph(self):
        """
        构建易经知识图谱
        """
        # 添加八卦节点
        bagua_nodes = {
            "乾": {"type": "八卦", "attribute": "天", "element": "金"},
            "坤": {"type": "八卦", "attribute": "地", "element": "土"},
            "坎": {"type": "八卦", "attribute": "水", "element": "水"},
            "离": {"type": "八卦", "attribute": "火", "element": "火"},
            "震": {"type": "八卦", "attribute": "雷", "element": "木"},
            "巽": {"type": "八卦", "attribute": "风", "element": "木"},
            "艮": {"type": "八卦", "attribute": "山", "element": "土"},
            "兑": {"type": "八卦", "attribute": "泽", "element": "金"}
        }
        
        for node_id, properties in bagua_nodes.items():
            self.add_node(node_id, properties)
        
        # 添加关系
        self.add_edge("乾", "坤", "错卦")
        self.add_edge("乾", "乾", "综卦")
        self.add_edge("坎", "离", "错卦")
        self.add_edge("震", "巽", "错卦")
        self.add_edge("艮", "兑", "错卦")
        
        return {
            "status": "success",
            "nodes_count": len(self.nodes),
            "edges_count": sum(len(edges) for edges in self.edges.values())
        }
    
    def query_relations(self, node_id):
        """
        查询节点关系
        """
        if node_id not in self.nodes:
            return {"error": "节点不存在"}
        
        relations = self.edges.get(node_id, [])
        
        return {
            "node": node_id,
            "properties": self.nodes[node_id],
            "relations": relations
        }
    
    def find_path(self, start, end, max_depth=3):
        """
        寻找路径
        """
        if start not in self.nodes or end not in self.nodes:
            return {"error": "节点不存在"}
        
        # BFS寻路
        from collections import deque
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current == end:
                return {"path": path}
            
            if len(path) >= max_depth:
                continue
            
            for edge in self.edges[current]:
                neighbor = edge["target"]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return {"path": None}
    
    def infer_knowledge(self, node_id):
        """
        推断知识
        """
        if node_id not in self.nodes:
            return {"error": "节点不存在"}
        
        # 简化推断：基于关系推断
        inferred = []
        
        for edge in self.edges[node_id]:
            target = edge["target"]
            relation = edge["relation"]
            
            if relation == "错卦":
                inferred.append(f"{node_id}与{target}阴阳相反")
            elif relation == "综卦":
                inferred.append(f"{node_id}与{target}倒置关系")
        
        return {
            "node": node_id,
            "inferred_knowledge": inferred
        }

def main():
    parser = argparse.ArgumentParser(description="知识图谱")
    parser.add_argument("--build", action="store_true", help="构建易经知识图谱")
    parser.add_argument("--query", type=str, help="查询节点关系")
    parser.add_argument("--path", nargs=2, help="寻找路径")
    parser.add_argument("--infer", type=str, help="推断知识")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    graph = KnowledgeGraph()
    
    if args.build:
        result = graph.build_yijing_graph()
    elif args.query:
        result = graph.query_relations(args.query)
    elif args.path and len(args.path) == 2:
        result = graph.find_path(args.path[0], args.path[1])
    elif args.infer:
        result = graph.infer_knowledge(args.infer)
    else:
        # 默认：构建知识图谱
        result = graph.build_yijing_graph()
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【知识图谱】")
        print("=" * 70)
        
        if "status" in result:
            print(f"\n【图谱构建】")
            print(f"  状态：{result['status']}")
            print(f"  节点数：{result['nodes_count']}")
            print(f"  边数：{result['edges_count']}")
        
        elif "node" in result:
            print(f"\n【节点查询】")
            print(f"  节点：{result['node']}")
            print(f"  属性：{result['properties']}")
            print(f"  关系：")
            for edge in result["relations"]:
                print(f"    {edge['relation']} → {edge['target']}")
        
        elif "path" in result:
            print(f"\n【路径查找】")
            if result["path"]:
                print(f"  路径：{' → '.join(result['path'])}")
            else:
                print(f"  路径：未找到")
        
        elif "inferred_knowledge" in result:
            print(f"\n【知识推断】")
            print(f"  节点：{result['node']}")
            print(f"  推断知识：")
            for knowledge in result["inferred_knowledge"]:
                print(f"    • {knowledge}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()

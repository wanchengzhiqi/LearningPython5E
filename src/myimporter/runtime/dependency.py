#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/15


class DependencyResolver:
    def __init__(self, registry):
        self.registry = registry

    def resolve(self):
        graph = {}
        for name in self.registry.all():
            graph[name] = self.registry.get_dependencies(name)

        return self._topological_sort(graph)

    def _topological_sort(self, graph):
        visited = set()
        temp_mark = set()
        result = []

        def visit(noders):
            if noders in temp_mark:
                raise RuntimeError(f"Circular dependency detected: {noders}")

            if noders not in visited:
                temp_mark.add(noders)

                for neighbor in graph.get(noders, []):
                    visit(neighbor)

                temp_mark.remove(noders)
                visited.add(noders)
                result.append(noders)

        for node in graph:
            visit(node)

        return result

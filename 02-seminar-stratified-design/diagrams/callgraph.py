"""Граф вызовов фильмотеки: строится по исходному коду, слои берутся из файла конфигурации.

Запуск (из папки 02-seminar-stratified-design):

    python3 diagrams/callgraph.py filmoteka diagrams/layers_after.py diagrams/callgraph-after
    dot -Tsvg diagrams/callgraph-after.dot -o diagrams/callgraph-after.svg

Что попадает в граф:
  * функции модулей и методы классов (вложенные функции и лямбды считаются частью
    функции, в которой написаны);
  * конструкторы классов (вызов Film(...) — стрелка к Film.__init__) и сеттеры свойств;
  * чтение полей сущностей — стрелка к узлу данных «Класс: поля»;
  * исключения предметной области — узлы данных;
  * встроенные функции, методы str/list/dict/файла и конструкции языка
    (for, индекс [ ], срез [:]) — нижний слой «Язык Python».
Ссылка на функцию без вызова (передача аргументом, таблица MAKERS) — тоже стрелка.

Категория узла:
  * действие — узел вызывает input/print/работу с файлами/часы напрямую или через
    другие функции (действия «распространяются» вверх по графу);
  * данные — поля сущностей и исключения;
  * вычисление — всё остальное.

Скрипт пишет <out>.dot и <out>.md (метрики) и печатает стрелки, которые идут не вниз.
"""

import ast
import builtins
import runpy
import sys
from fnmatch import fnmatchcase
from pathlib import Path

LANGUAGE_LAYER = "Язык Python"

# Методы встроенных типов: имя метода -> узел языка
BUILTIN_METHODS = {
    "split": "str.split", "strip": "str.strip", "lower": "str.lower", "join": "str.join",
    "splitlines": "str.splitlines", "append": "list.append", "pop": "list.pop",
    "setdefault": "dict.setdefault", "items": "dict.items", "get": "dict.get",
    "add": "set.add", "write": "file.write", "read": "file.read",
}
# Модули стандартной библиотеки: (модуль, функция) -> узел языка
STDLIB = {
    ("copy", "copy"): "copy.copy",
    ("traceback", "format_exc"): "traceback.format_exc",
    ("datetime", "now"): "datetime.now",
}
# Узлы языка, которые являются действиями: ввод-вывод, файлы, часы, состояние исключения
PRIMITIVE_ACTIONS = {"input()", "print()", "open()", "file.write", "file.read", "datetime.now",
                     "traceback.format_exc"}
BUILTIN_NAMES = set(dir(builtins))


class ClassInfo:
    def __init__(self, module, name, bases):
        self.module = module
        self.name = name
        self.bases = bases
        self.methods = set()
        self.properties = set()
        self.setters = set()
        self.fields = set()
        self.is_exception = False


class Project:
    """Символы всех модулей пакета."""

    def __init__(self, package_dir):
        self.trees = {}
        for path in sorted(Path(package_dir).glob("*.py")):
            if path.stem not in ("__init__", "__main__"):
                self.trees[path.stem] = ast.parse(path.read_text(encoding="utf-8"))
        self.functions = {}  # (модуль, имя) -> узел
        self.classes = {}    # имя класса -> ClassInfo
        self.constants = {}  # (модуль, имя) -> узел выражения (для таблиц функций)
        self.ambiguous = set()  # поля с одинаковым именем у разных классов
        for module, tree in self.trees.items():
            self.collect(module, tree)
        self.mark_exceptions()

    def collect(self, module, tree):
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                self.functions[(module, node.name)] = node
            elif isinstance(node, ast.ClassDef):
                info = ClassInfo(module, node.name, [ast.unparse(b) for b in node.bases])
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        decorators = [ast.unparse(d) for d in item.decorator_list]
                        if "property" in decorators:
                            info.properties.add(item.name)
                        elif any(d.endswith(".setter") for d in decorators):
                            info.setters.add(item.name)
                        else:
                            info.methods.add(item.name)
                        if item.name == "__init__":
                            for sub in ast.walk(item):
                                if (isinstance(sub, ast.Attribute) and isinstance(sub.ctx, ast.Store)
                                        and isinstance(sub.value, ast.Name) and sub.value.id == "self"):
                                    info.fields.add(sub.attr)
                    elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        info.fields.add(item.target.id)  # поля NamedTuple / dataclass
                self.classes[node.name] = info
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.constants[(module, target.id)] = node.value

    def mark_exceptions(self):
        for info in self.classes.values():
            info.is_exception = self.is_exception_class(info.name)

    def is_exception_class(self, name):
        info = self.classes.get(name)
        if info is None:
            return name in ("Exception", "BaseException")
        return any(self.is_exception_class(base) for base in info.bases)

    def mro(self, name):
        """Класс и его предки внутри проекта, от потомка к предку."""
        result = []
        while name in self.classes:
            result.append(self.classes[name])
            bases = [b for b in self.classes[name].bases if b in self.classes]
            name = bases[0] if bases else None
        return result

    def find_method(self, class_name, method):
        for info in self.mro(class_name):
            if method in info.methods:
                return f"{info.name}.{method}"
        return None

    def classes_with(self, attribute, kinds):
        return [info for info in self.classes.values() if attribute in getattr(info, kinds)]

    def root_of(self, infos):
        """Из нескольких классов иерархии — самый верхний (вызов полиморфный)."""
        names = {info.name for info in infos}
        roots = [info for info in infos if not any(base.name in names for base in self.mro(info.name)[1:])]
        return roots

    def field_owner(self, attribute):
        """Класс, которому принадлежит поле или свойство attribute (по имени)."""
        plain = attribute.lstrip("_")
        owners = [info for info in self.classes.values()
                  if not info.is_exception and (attribute in info.fields or plain in info.properties
                                                or attribute in info.properties)]
        roots = self.root_of(owners)
        if len(roots) > 1:
            self.ambiguous.add(attribute)
        return roots[0].name if len(roots) == 1 else None


class Collector(ast.NodeVisitor):
    """Стрелки из одной функции или метода."""

    def __init__(self, project, module, imports, current, class_name=None, local_names=()):
        self.project = project
        self.local_names = set(local_names)
        self.module = module
        self.imports = imports  # имя -> (модуль проекта, имя) или ("<stdlib>", модуль)
        self.current = current
        self.class_name = class_name
        self.edges = set()
        self.warnings = []

    def add(self, target):
        if target != self.current:
            self.edges.add(target)

    # --- имена ---

    def resolve_name(self, name, called=False):
        """Узел, на который ссылается имя, или None.

        Вызов класса — его конструктор; ссылка на класс без вызова (isinstance, таблица
        типов) — зависимость от его данных.
        """
        if (self.module, name) in self.project.functions:
            return f"{self.module}.{name}"
        if name in self.imports and self.imports[name][0] != "<stdlib>":
            module, original = self.imports[name]
            if (module, original) in self.project.functions:
                return f"{module}.{original}"
            name = original
        if name in self.project.classes:
            info = self.project.classes[name]
            if info.is_exception:
                return name
            if not called:
                return f"{name}: поля"
            init = self.project.find_method(name, "__init__")
            return init or f"{name}: поля"  # NamedTuple: вызов класса создаёт данные
        return None

    def constant_value(self, name):
        if (self.module, name) in self.project.constants:
            return self.project.constants[(self.module, name)]
        if name in self.imports and self.imports[name][0] != "<stdlib>":
            return self.project.constants.get(self.imports[name])
        return None

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in self.local_names:
            target = self.resolve_name(node.id)
            if target is not None:
                self.add(target)
            else:
                value = self.constant_value(node.id)
                if value is not None:
                    self.visit(value)  # таблица функций: стрелки к каждой функции таблицы

    # --- вызовы ---

    def visit_Call(self, node):
        func = node.func
        if isinstance(func, ast.Name):
            target = self.resolve_name(func.id, called=True)
            if target is not None:
                self.add(target)
            elif func.id in BUILTIN_NAMES:
                if func.id != "super":
                    self.add(f"{func.id}()")
            else:
                self.visit(func)
        elif isinstance(func, ast.Attribute):
            self.visit_method_call(func)
        else:
            self.visit(func)
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword.value)

    def visit_method_call(self, func):
        obj, method = func.value, func.attr
        # super().method()
        if isinstance(obj, ast.Call) and isinstance(obj.func, ast.Name) and obj.func.id == "super":
            bases = self.project.mro(self.class_name)[1:]
            target = self.project.find_method(bases[0].name, method) if bases else None
            self.add(target or f"{method}()")
            return
        if isinstance(obj, ast.Name):
            # self.method()
            if obj.id == "self" and self.class_name:
                target = self.project.find_method(self.class_name, method)
                if target:
                    self.add(target)
                    return
            # модуль проекта: console.success(...)
            if obj.id in self.imports and self.imports[obj.id][0] == "<module>":
                module = self.imports[obj.id][1]
                if (module, method) in self.project.functions:
                    self.add(f"{module}.{method}")
                    return
            # модуль стандартной библиотеки
            if obj.id in self.imports and self.imports[obj.id][0] == "<stdlib>":
                self.add(STDLIB.get((self.imports[obj.id][1], method), f"{obj.id}.{method}"))
                return
            # Класс.метод
            if obj.id in self.project.classes:
                target = self.project.find_method(obj.id, method)
                if target:
                    self.add(target)
                    return
        self.visit(obj)
        candidates = self.project.classes_with(method, "methods")
        if candidates:
            roots = self.project.root_of(candidates)
            if len(roots) > 1:
                self.warnings.append(f"{self.current}: метод .{method}() есть у нескольких классов, "
                                     "стрелки проведены ко всем")
            for root in roots:
                self.add(f"{root.name}.{method}")
            return
        if method in BUILTIN_METHODS:
            self.add(BUILTIN_METHODS[method])
            return
        self.warnings.append(f"{self.current}: не распознан вызов .{method}()")

    # --- поля и ссылки на методы без вызова ---

    def visit_Attribute(self, node):
        obj, attribute = node.value, node.attr
        # ссылка на функцию модуля без вызова или константа модуля: views.TITLE
        if isinstance(obj, ast.Name) and self.imports.get(obj.id, ("",))[0] == "<module>":
            module = self.imports[obj.id][1]
            if (module, attribute) in self.project.functions:
                self.add(f"{module}.{attribute}")
            elif (module, attribute) in self.project.constants:
                self.visit(self.project.constants[(module, attribute)])
            return
        if isinstance(obj, ast.Name) and obj.id in self.project.classes:
            target = self.project.find_method(obj.id, attribute)
            if target:
                self.add(target)  # Catalog.sorted_by_name передан как функция
                return
        if isinstance(node.ctx, ast.Store):
            # self.release = ... в конструкторе: сеттер свойства
            if isinstance(obj, ast.Name) and obj.id == "self" and self.class_name:
                for info in self.project.mro(self.class_name):
                    if attribute in info.setters:
                        self.add(f"{info.name}.{attribute}=")
                        return
            owner = self.project.field_owner(attribute)
            if owner:
                self.add(f"{owner}: поля")
            self.visit(obj)
            return
        owner = self.project.field_owner(attribute)
        if owner:
            self.add(f"{owner}: поля")
        self.visit(obj)

    # --- конструкции языка ---

    def visit_For(self, node):
        self.add("for")
        self.generic_visit(node)

    def visit_comprehension(self, node):
        self.add("for")
        self.generic_visit(node)

    def visit_Subscript(self, node):
        self.add("срез [:]" if isinstance(node.slice, ast.Slice) else "индекс [ ]")
        self.generic_visit(node)


def imports_of(tree):
    result = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            module = node.module.split(".")[-1]
            for alias in node.names:
                if node.module == "filmoteka":
                    result[alias.asname or alias.name] = ("<module>", alias.name)
                elif node.module.startswith("filmoteka"):
                    result[alias.asname or alias.name] = (module, alias.name)
                else:
                    result[alias.asname or alias.name] = ("<stdlib>", alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                result[alias.asname or alias.name] = ("<stdlib>", alias.name)
    return result


def local_names_of(function):
    """Параметры и локальные переменные функции (вместе с вложенными функциями и лямбдами)."""
    names = set()
    for node in ast.walk(function):
        if isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            names.add(node.id)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            names.add(node.name)
        elif isinstance(node, ast.FunctionDef) and node is not function:
            names.add(node.name)
    return names


def build_graph(package_dir, extra_edges=()):
    """(узлы, стрелки, предупреждения); узел -> {kind, module}.

    extra_edges — неявные вызовы, которых не видно в синтаксисе: str(film) вызывает
    __str__, sorted() — __lt__, len(playlist) — __len__, for по плейлисту — __iter__.
    """
    project = Project(package_dir)
    nodes, edges, warnings = {}, set(), []

    def walk(module, imports, name, body_node, class_name=None, kind="function"):
        nodes[name] = {"kind": kind, "module": module}
        collector = Collector(project, module, imports, name, class_name, local_names_of(body_node))
        for statement in body_node.body:
            collector.visit(statement)
        for decorator_arg in body_node.args.defaults:
            collector.visit(decorator_arg)
        edges.update((name, target) for target in collector.edges)
        warnings.extend(collector.warnings)

    for module, tree in project.trees.items():
        imports = imports_of(tree)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                walk(module, imports, f"{module}.{node.name}", node)
            elif isinstance(node, ast.ClassDef):
                info = project.classes[node.name]
                if info.is_exception:
                    nodes[node.name] = {"kind": "data", "module": module}
                    continue
                nodes[f"{node.name}: поля"] = {"kind": "data", "module": module}
                for item in node.body:
                    if not isinstance(item, ast.FunctionDef):
                        continue
                    decorators = [ast.unparse(d) for d in item.decorator_list]
                    if "property" in decorators:
                        continue  # геттер — это чтение поля, его заменяет узел «поля»
                    suffix = "=" if any(d.endswith(".setter") for d in decorators) else ""
                    walk(module, imports, f"{node.name}.{item.name}{suffix}", item, node.name)

    for source, target in extra_edges:
        if source not in nodes or target not in nodes:
            warnings.append(f"неявная стрелка с неизвестным узлом: {source} -> {target}")
        edges.add((source, target))
    for attribute in sorted(project.ambiguous):
        warnings.append(f"поле .{attribute} есть у нескольких классов, стрелка к данным не построена")
    # узлы, на которые есть стрелки, но которых нет среди функций: язык
    for _, target in list(edges):
        if target not in nodes:
            nodes[target] = {"kind": "language", "module": None}
    # методы без тела (абстрактные) и Класс.__init__ без явного конструктора остаются узлами
    return nodes, edges, warnings


def mark_actions(nodes, edges):
    """Действия «заражают» всех, кто их вызывает."""
    callers = {}
    for source, target in edges:
        callers.setdefault(target, set()).add(source)
    actions = set(PRIMITIVE_ACTIONS & nodes.keys())
    stack = list(actions)
    while stack:
        for caller in callers.get(stack.pop(), ()):
            if caller not in actions and nodes[caller]["kind"] != "language":
                actions.add(caller)
                stack.append(caller)
    for name, info in nodes.items():
        if info["kind"] == "language":
            info["category"] = "язык"
        elif info["kind"] == "data":
            info["category"] = "данные"
        elif name in actions:
            info["category"] = "действие"
        else:
            info["category"] = "вычисление"


def assign_layers(nodes, edges, layers):
    """Номер подуровня (снизу, язык — 0) для каждого узла.

    layers: [(назначение слоя, [шаблоны узлов]), ...] сверху вниз; язык всегда внизу.
    Если функции одного слоя вызывают друг друга, слой делится на подуровни:
    вызываемая функция стоит ниже вызывающей. Так все стрелки идут строго вниз.
    Возвращает (назначения слоёв, слой узла, подуровень узла, узлы без слоя, циклы).
    """
    titles = [title for title, _ in layers] + [LANGUAGE_LAYER]
    band, unmatched = {}, []
    for name, info in nodes.items():
        if info["kind"] == "language":
            band[name] = len(layers)
            continue
        exact = [i for i, (_, patterns) in enumerate(layers) if name in patterns]
        matched = exact or [i for i, (_, patterns) in enumerate(layers)
                            if any(fnmatchcase(name, p) for p in patterns)]
        if matched:
            band[name] = matched[0]
        else:
            unmatched.append(name)
    if unmatched:
        return titles, band, {}, unmatched, []
    inner = {}
    for source, target in edges:
        if band[source] == band[target]:
            inner.setdefault(source, set()).add(target)
    sub, cycles = {}, []

    def depth(name, path=()):
        if name in sub:
            return sub[name]
        if name in path:
            cycles.append(path + (name,))
            return 0
        sub[name] = 1 + max((depth(t, path + (name,)) for t in inner.get(name, ())), default=-1)
        return sub[name]

    for name in nodes:
        depth(name)
    # подуровни считаются снизу вверх, слой за слоем
    height, offset = {}, 0
    for index in range(len(titles) - 1, -1, -1):
        members = [n for n in nodes if band[n] == index]
        for name in members:
            height[name] = offset + sub[name]
        offset += 1 + max((sub[n] for n in members), default=-1) if members else 0
    return titles, band, height, unmatched, cycles


def metrics(nodes, edges, height, band, titles, top_layers, barrier):
    functions = [n for n, info in nodes.items() if info["kind"] == "function"]
    lengths = {(s, t): height[s] - height[t] for s, t in edges}
    longest = max(lengths.values())
    # стрелки к данным и языку есть у каждой ветки графа, поэтому длину считаем между функциями
    between = [(s, t) for s, t in edges if nodes[t]["kind"] == "function"]
    longest_in_layers = max(band[t] - band[s] for s, t in between)
    owners, inside = barrier
    breaches = sorted({(s, t) for s, t in edges
                       if any(fnmatchcase(t, p) for p in inside)
                       and not any(fnmatchcase(s, p) for p in owners)})
    to_language = sorted({s for s, t in edges if height[t] == 0})
    data_band = titles.index("Данные")
    top = {n for n in nodes if titles[band[n]] in top_layers}
    top_to_low = sorted({s for s, t in edges if s in top and band[t] >= data_band})
    by_category = {}
    for name in functions:
        by_category[nodes[name]["category"]] = by_category.get(nodes[name]["category"], 0) + 1
    return {
        "functions": len(functions),
        "by_category": by_category,
        "edges": len(edges),
        "bands": len(titles),
        "layers": max(height.values()) + 1,
        "longest": longest,
        "longest_edges": sorted(e for e, length in lengths.items() if length == longest),
        "longest_in_layers": longest_in_layers,
        "longest_layer_edges": sorted(e for e in between if band[e[1]] - band[e[0]] == longest_in_layers),
        "long_between": sorted(e for e in between if band[e[1]] - band[e[0]] >= 3),
        "breaches": breaches,
        "lengths": lengths,
        "to_language": to_language,
        "top_to_low": top_to_low,
    }


# --- вывод ---

COLORS = {
    "действие": ("#fbe1dd", "#c0392b"),
    "вычисление": ("#dcf2e1", "#1e8449"),
    "данные": ("#dbe8f8", "#2463a8"),
    "язык": ("#ececec", "#7a7a7a"),
}


def label(name, info):
    if info["kind"] == "function" and "." in name and name.split(".")[0] == info["module"]:
        func = name.split(".", 1)[1]
        return f'<{func}<BR/><FONT POINT-SIZE="8" COLOR="#555555">{info["module"]}</FONT>>'
    return '"' + name.replace('"', '\\"') + '"'


MAX_ROW = 9  # узлов в строке рисунка; длинные подуровни переносятся на несколько строк

LANGUAGE_ORDER = ["input()", "print()", "open()", "file.read", "file.write", "datetime.now",
                  "traceback.format_exc", "for", "индекс [ ]", "срез [:]"]


def row_order(name):
    """Порядок узлов в строке: сначала действия языка и синтаксис, потом остальное по имени."""
    return (LANGUAGE_ORDER.index(name) if name in LANGUAGE_ORDER else len(LANGUAGE_ORDER), name)


def to_dot(nodes, edges, height, band, titles, title, top_layers):
    """Граф для Graphviz: каждый слой — полоса со своим назначением, внутри — подуровни.

    Подуровень, в котором больше MAX_ROW узлов, рисуется в несколько строк: узлы одного
    подуровня друг друга не вызывают, поэтому стрелки всё равно идут вниз.
    """
    lines = [
        "digraph callgraph {",
        f'  label="{title}"; labelloc=t; fontsize=24; fontname="Helvetica";',
        "  rankdir=TB; newrank=true; nodesep=0.1; ranksep=0.3; concentrate=true;",
        '  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=10, height=0.3];',
        # положение узлов задают только слои; стрелки рисуются поверх и раскладку не двигают
        '  edge [constraint=false, arrowsize=0.45, color="#8a96a366", penwidth=0.8];',
    ]
    rows = []  # строки рисунка сверху вниз
    for index, layer_title in enumerate(titles):
        members = [n for n in nodes if band[n] == index]
        if not members:
            continue
        shade = "#f7f7f2" if index % 2 == 0 else "#eef2f7"
        lines.append(f"  subgraph cluster_{index} {{")
        lines.append(f'    label="{layer_title}"; labeljust=l; fontsize=15; fontname="Helvetica-Bold";')
        lines.append(f'    style=filled; fillcolor="{shade}"; color="#c8c8c8";')
        for level in sorted({height[n] for n in members}, reverse=True):
            row = sorted((n for n in members if height[n] == level), key=row_order)
            chunks = [row[i:i + MAX_ROW] for i in range(0, len(row), MAX_ROW)]
            for number, chunk in enumerate(chunks):
                marker = f"R{level}_{number}"
                text = str(level) if number == 0 else ""
                lines.append(f'    "{marker}" [shape=plaintext, style="", fontsize=11, fontcolor="#888888", '
                             f'label="{text}", width=0.2];')
                lines.append(f'    {{ rank=same; "{marker}"; ' + " ".join(f'"{m}";' for m in chunk) + " }")
                rows.append(marker)
        lines.append("  }")
    lines.append("  " + " -> ".join(f'"{r}"' for r in rows) + " [style=invis, weight=1000, constraint=true];")
    for name in sorted(nodes):
        info = nodes[name]
        fill, border = COLORS[info["category"]]
        shape = ", shape=ellipse" if info["kind"] == "language" else (
            ", shape=cylinder" if info["kind"] == "data" else "")
        lines.append(f'  "{name}" [label={label(name, info)}, fillcolor="{fill}", color="{border}"{shape}];')
    data_band = titles.index("Данные")
    for source, target in sorted(edges):
        style = ""
        if height[source] <= height[target]:
            style = ' [color="#e00000", penwidth=2.5]'
        elif titles[band[source]] in top_layers and band[target] >= data_band:
            style = ' [color="#e67e22", penwidth=1.3]'
        lines.append(f'  "{source}" -> "{target}"{style};')
    lines.append("}")
    return "\n".join(lines) + "\n"


def to_markdown(m, nodes, height, band, titles, title):
    out = [f"# Метрики графа: {title}", ""]
    out.append("Файл создан скриптом `callgraph.py`. Длина стрелки — на сколько подуровней она опускается.")
    out.append("")
    out.append("| Показатель | Значение |")
    out.append("|---|---|")
    out.append(f"| Слоёв с назначением (вместе с «{LANGUAGE_LAYER}») | {m['bands']} |")
    out.append(f"| Подуровней | {m['layers']} |")
    out.append(f"| Функций и методов | {m['functions']} |")
    for category in ("действие", "вычисление"):
        out.append(f"| — из них {category} | {m['by_category'].get(category, 0)} |")
    out.append(f"| Стрелок | {m['edges']} |")
    out.append(f"| Самая длинная стрелка между функциями, слоёв | {m['longest_in_layers']} |")
    out.append(f"| Стрелок между функциями через 3 слоя и больше | {len(m['long_between'])} |")
    out.append(f"| Самая длинная стрелка вообще, подуровней | {m['longest']} |")
    out.append(f"| Функций, напрямую использующих конструкции языка | {len(m['to_language'])} |")
    out.append(f"| Функций верхних слоёв, напрямую зависящих от данных и языка | {len(m['top_to_low'])} |")
    out.append(f"| Обращений к внутренностям каталога и плейлиста извне | {len(m['breaches'])} |")
    out.append("")
    out.append("## Слои сверху вниз")
    out.append("")
    for index, layer_title in enumerate(titles):
        members = sorted((n for n in nodes if band[n] == index), key=lambda n: (-height[n], n))
        if not members:
            continue
        levels = sorted({height[n] for n in members}, reverse=True)
        span = f"подуровни {levels[-1]}–{levels[0]}" if len(levels) > 1 else f"подуровень {levels[0]}"
        out.append(f"**{layer_title}** ({span}, узлов: {len(members)}): "
                   + ", ".join(f"`{x}`" for x in members))
        out.append("")
    out.append("## Стрелки между функциями через 3 слоя и больше")
    out.append("")
    for source, target in sorted(m["long_between"], key=lambda e: (band[e[0]] - band[e[1]], e)):
        out.append(f"- `{source}` ({titles[band[source]]}) → `{target}` ({titles[band[target]]}), "
                   f"слоёв: {band[target] - band[source]}")
    out.append("")
    out.append("## Обращения к внутренностям каталога и плейлиста извне")
    out.append("")
    for source, target in m["breaches"]:
        out.append(f"- `{source}` → `{target}`")
    if not m["breaches"]:
        out.append("Нет.")
    out.append("")
    out.append("## Функции верхних слоёв, напрямую зависящие от данных и языка")
    out.append("")
    for name in m["top_to_low"]:
        out.append(f"- `{name}`")
    if not m["top_to_low"]:
        out.append("Нет.")
    out.append("")
    return "\n".join(out)


def main(package_dir, layers_file, out):
    config = runpy.run_path(layers_file)
    nodes, edges, warnings = build_graph(package_dir, config.get("IMPLICIT_CALLS", ()))
    mark_actions(nodes, edges)
    titles, band, height, unmatched, cycles = assign_layers(nodes, edges, config["LAYERS"])
    for warning in warnings:
        print("предупреждение:", warning)
    if unmatched:
        print("нет слоя у узлов:", ", ".join(sorted(unmatched)))
        sys.exit(1)
    for cycle in cycles:
        print("цикл внутри слоя:", " -> ".join(cycle))
    upward = sorted((s, t) for s, t in edges if band[s] > band[t])
    for source, target in upward:
        print(f"стрелка вверх: {source} ({titles[band[source]]}) -> {target} ({titles[band[target]]})")
    m = metrics(nodes, edges, height, band, titles, config["TOP_LAYERS"], config["BARRIER"])
    Path(out + ".dot").write_text(to_dot(nodes, edges, height, band, titles, config["TITLE"], config["TOP_LAYERS"]), encoding="utf-8")
    Path(out + ".md").write_text(to_markdown(m, nodes, height, band, titles, config["TITLE"]), encoding="utf-8")
    print(f"узлов {len(nodes)}, функций {m['functions']}, стрелок {m['edges']}, слоёв {m['bands']}, "
          f"подуровней {m['layers']}, самая длинная между функциями {m['longest_in_layers']} сл., "
          f"через 3+ слоя {len(m['long_between'])}, "
          f"барьер {len(m['breaches'])}, "
          f"к языку {len(m['to_language'])}, верх->данные/язык {len(m['top_to_low'])}, вверх {len(upward)}")


if __name__ == "__main__":
    main(*sys.argv[1:4])

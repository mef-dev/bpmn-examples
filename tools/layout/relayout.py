"""Lays every diagram out top to bottom and rewrites its BPMNDiagram section.

The generator places nodes left to right and puts both data elements at the same
point, so they sit on top of each other. This pass throws the diagram away and
draws it again from the process graph: the main path runs downwards in one
column, each branch that leaves a boundary event gets a column of its own to the
right, and data elements sit to the left of the node they belong to.
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"

NODE_TAGS = {
    "startEvent": (36, 36), "endEvent": (36, 36),
    "intermediateThrowEvent": (36, 36), "intermediateCatchEvent": (36, 36),
    "boundaryEvent": (36, 36),
    "task": (100, 80), "callActivity": (100, 80), "subProcess": (140, 90),
    "exclusiveGateway": (50, 50), "parallelGateway": (50, 50),
    "eventBasedGateway": (50, 50),
    "dataObjectReference": (36, 50), "dataStoreReference": (50, 50),
}

COL_FIRST = 300                  # центр першої колонки
COL_STEP = 320                   # відстань між колонками
ROW_STEP = 130                   # відстань між рядами
TOP = 80
DATA_X = 110                     # колонка для елементів даних


def column_x(index: int) -> int:
    return COL_FIRST + index * COL_STEP


def local(tag):
    return tag.split("}", 1)[-1]


class Plane:
    """Одна площина діаграми: процес або згорнутий Sub Process."""

    def __init__(self, element, element_id):
        self.element = element
        self.id = element_id
        self.nodes = {}
        self.order = []
        self.flows = []
        for child in element:
            name = local(child.tag)
            if name in NODE_TAGS:
                nid = child.get("id")
                self.nodes[nid] = (name, child)
                self.order.append(nid)
            elif name == "sequenceFlow":
                self.flows.append((child.get("id"), child.get("sourceRef"),
                                   child.get("targetRef")))
        self.pos = {}

    def layout(self):
        outgoing = {}
        for _, src, dst in self.flows:
            outgoing.setdefault(src, []).append(dst)
        boundary_hosts = {
            nid: node.get("attachedToRef")
            for nid, (name, node) in self.nodes.items() if name == "boundaryEvent"
        }

        # головний ланцюг: від старту, не заходячи в гілки граничних подій
        starts = [nid for nid, (name, _) in self.nodes.items()
                  if name == "startEvent"]
        placed = set()
        main = []
        cursor = starts[0] if starts else None
        while cursor and cursor not in placed:
            main.append(cursor)
            placed.add(cursor)
            nxt = [d for d in outgoing.get(cursor, []) if d not in placed]
            cursor = nxt[0] if nxt else None

        row = 0
        for nid in main:
            self._place(nid, column_x(0), TOP + row * ROW_STEP)
            row += 1

        # гранична подія сидить на межі своєї задачі, а не в колонці
        for nid, host in boundary_hosts.items():
            hx, hy, hw, hh = self.pos.get(host, (column_x(0), TOP, 100, 80))
            self._place(nid, hx + hw, hy + hh - 18)
            placed.add(nid)

        # Кожне відгалуження — власна колонка, що починається на рівні свого
        # джерела: і паралельна гілка від шлюзу, і гілка від граничної події.
        column = 1
        progress = True
        while progress:
            progress = False
            for source in list(self.pos):
                for target in outgoing.get(source, []):
                    if target in placed:
                        continue
                    x = column_x(column)
                    y = self.pos[source][1] + ROW_STEP
                    cursor = target
                    while cursor and cursor not in placed:
                        placed.add(cursor)
                        self._place(cursor, x, y)
                        y += ROW_STEP
                        nxt = [d for d in outgoing.get(cursor, [])
                               if d not in placed]
                        cursor = nxt[0] if nxt else None
                    column += 1
                    progress = True

        # усе, що лишилось поза ланцюгами
        leftover_y = TOP + max(row, 1) * ROW_STEP
        for nid, (name, _) in self.nodes.items():
            if nid in self.pos:
                continue
            if name in ("dataObjectReference", "dataStoreReference"):
                continue
            self._place(nid, column_x(column), leftover_y)
            leftover_y += ROW_STEP

        # елементи даних — ліворуч, навпроти краю процесу
        data_ids = [nid for nid, (name, _) in self.nodes.items()
                    if name in ("dataObjectReference", "dataStoreReference")]
        for index, nid in enumerate(data_ids):
            self._place(nid, DATA_X, TOP + index * 110)

    def _place(self, nid, cx, cy, centred=True):
        name, _ = self.nodes[nid]
        w, h = NODE_TAGS[name]
        if centred:
            self.pos[nid] = (cx - w // 2, cy, w, h)
        else:
            self.pos[nid] = (cx - w // 2, cy, w, h)

    def render(self):
        lines = [f'  <bpmndi:BPMNDiagram id="Di_{self.id}">',
                 f'    <bpmndi:BPMNPlane id="Dp_{self.id}" bpmnElement="{self.id}">']
        for nid in self.order:
            if nid not in self.pos:
                continue
            x, y, w, h = self.pos[nid]
            name, _ = self.nodes[nid]
            extra = ' isExpanded="false"' if name == "subProcess" else ""
            lines += [
                f'      <bpmndi:BPMNShape id="Sh_{nid}" bpmnElement="{nid}"{extra}>',
                f'        <omgdc:Bounds x="{x}" y="{y}" width="{w}" height="{h}" />',
                "      </bpmndi:BPMNShape>",
            ]
        for fid, src, dst in self.flows:
            if src not in self.pos or dst not in self.pos:
                continue
            sx, sy, sw, sh = self.pos[src]
            tx, ty, tw, th = self.pos[dst]
            start = (sx + sw // 2, sy + sh)
            end = (tx + tw // 2, ty)
            lines.append(f'      <bpmndi:BPMNEdge id="Ed_{fid}" bpmnElement="{fid}">')
            if start[0] == end[0]:
                points = [start, end]
            else:
                mid = start[1] + 30
                points = [start, (start[0], mid), (end[0], mid), end]
            for px, py in points:
                lines.append(f'        <di:waypoint x="{px}" y="{py}" />')
            lines.append("      </bpmndi:BPMNEdge>")
        lines += ["    </bpmndi:BPMNPlane>", "  </bpmndi:BPMNDiagram>"]
        return "\n".join(lines)


def relayout(path: pathlib.Path) -> str:
    raw = path.read_text(encoding="utf-8")
    ET.register_namespace("", BPMN)
    root = ET.fromstring(raw)

    planes = []
    for process in root.iter():
        if local(process.tag) == "process":
            planes.append(Plane(process, process.get("id")))
        elif local(process.tag) == "subProcess":
            planes.append(Plane(process, process.get("id")))
    for plane in planes:
        plane.layout()

    diagrams = "\n".join(plane.render() for plane in planes)
    without = re.sub(r"  <bpmndi:BPMNDiagram.*?</bpmndi:BPMNDiagram>\n", "",
                     raw, flags=re.S)
    return without.replace("</definitions>", diagrams + "\n</definitions>")


if __name__ == "__main__":
    targets = [pathlib.Path(a) for a in sys.argv[1:]]
    for target in targets:
        target.write_bytes(relayout(target).encode("utf-8"))
        print(f"  переверстано: {target.name}")

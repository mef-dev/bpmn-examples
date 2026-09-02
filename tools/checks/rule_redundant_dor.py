"""Правило 11: елемент даних не повторює тип, уже оголошений на межі.

Кінцева і початкова події несуть свій DOR — з нього рушій виводить типізовану
межу процесу. Gateway тип не змінює. Тому DOR на задачі, від якої до межі
ведуть самі лише гейтвеї, дублює вже сказане і засмічує схему.
"""
import xml.etree.ElementTree as ET

GATEWAYS = ("exclusiveGateway", "parallelGateway", "inclusiveGateway",
            "eventBasedGateway", "complexGateway")
TASKS = ("task", "serviceTask", "scriptTask", "businessRuleTask", "userTask",
         "manualTask", "sendTask", "receiveTask", "callActivity", "subProcess")


def local(tag):
    return tag.split("}", 1)[-1]


def redundant_data_objects(root: ET.Element):
    kind, dor_type = {}, {}
    for el in root.iter():
        if el.get("id"):
            kind[el.get("id")] = local(el.tag)
        if local(el.tag) == "dataObjectReference":
            dor_type[el.get("id")] = (el.get("name") or "").strip()

    out_flows, in_flows = {}, {}
    for el in root.iter():
        if local(el.tag) == "sequenceFlow":
            out_flows.setdefault(el.get("sourceRef"), []).append(el.get("targetRef"))
            in_flows.setdefault(el.get("targetRef"), []).append(el.get("sourceRef"))

    boundary = {}
    for el in root.iter():
        if local(el.tag) not in ("endEvent", "startEvent"):
            continue
        for child in el.iter():
            if local(child.tag) == "dataInputAssociation":
                boundary[el.get("id")] = dor_type.get(
                    (child.findtext("{*}sourceRef") or "").strip(), "")
            elif local(child.tag) == "dataOutputAssociation":
                boundary[el.get("id")] = dor_type.get(
                    (child.findtext("{*}targetRef") or "").strip(), "")

    def reach(node, forward):
        edges = out_flows if forward else in_flows
        seen, stack, found = set(), list(edges.get(node, [])), []
        while stack:
            nid = stack.pop()
            if nid in seen:
                continue
            seen.add(nid)
            if kind.get(nid) in GATEWAYS:
                stack.extend(edges.get(nid, []))
            elif kind.get(nid) in ("endEvent", "startEvent"):
                found.append(nid)
            else:
                return []
        return found

    hits = []
    for el in root.iter():
        if local(el.tag) not in TASKS:
            continue
        for child in list(el):
            tag = local(child.tag)
            if tag == "dataOutputAssociation":
                ref = (child.findtext("{*}targetRef") or "").strip()
                ends = reach(el.get("id"), True)
            elif tag == "dataInputAssociation":
                ref = (child.findtext("{*}sourceRef") or "").strip()
                ends = reach(el.get("id"), False)
            else:
                continue
            mine = dor_type.get(ref)
            if ends and mine and all(boundary.get(e) == mine for e in ends):
                hits.append(f"{ref} ({mine}) біля {el.get('id')}: те саме вже "
                            f"оголошено на {', '.join(ends)}")
    return hits

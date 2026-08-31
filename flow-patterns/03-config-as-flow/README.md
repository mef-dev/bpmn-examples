# 03 · Configuration as a separate Flow

Connection strings, addresses, and mail settings do not belong in the process model. This group shows how to move them into a separate Flow and plug it in through a Call Activity — and what the same process looked like before the refactoring.

## When to use

As soon as a Flow contains even one connection string or stand address.

## Files

| File | What it shows |
|---|---|
| `get-config.bpmn` | the target configuration Flow: three elements, returns a typed object |
| `send-links.bpmn` | the consumer: Call Activity → `Parse Config` → everything else takes its values from `Root.Parameters.config` |
| `send-links-before.bpmn` | **how it was**: the connection string in the model, a hand-written `HttpClient`, a hard-coded mail address |

## Platform functions used

`RestApi/Download`

## Reserved words

`Root.Parameters` · `#Previous` · `Input` · `DataAssociations`

## What to watch out for

- Compare `send-links-before` and `send-links` side by side — it is the same
  task before and after the configuration was moved out.
- The configuration type is declared by **both** sides: in `get-config` as its
  own, in `send-links` as external (`types://external/…`).
- `Root.Parameters` — `Root` specifically, because the values are read from sub
  processes; a plain `Parameters` inside a Sub Process points at its own.
- A reference to an external Flow has **two forms**: mnemonic
  (`activities://bpmn-mnemo/<libType>/<libName>/<flowName>/#latest`) and numeric
  (`activities://bpmn/<libType>/<libId>/<flowId>/<version>`). The first is
  readable, the second pins a specific version.

---
For the data types in these examples, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).

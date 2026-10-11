# 07 · What starts a process

A Flow does not have to wait for someone to press Run. Declaring a route on the
start event turns the model into an HTTP endpoint.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| `StartSignalRoute` on the start event | the element parameter on `Ev_Start` |
| Choosing method and path | `{"method": "POST", "route": "webhook"}` |
| Escaping a C# keyword used as a field | `Input.@event` in `T_Accept` |
| The same typed boundary as any other Flow | the data elements on start and end |

## The model

```
start (POST /webhook) → Get Config → Parse Config → accept the call → end
                                           ↓
                                    handle Exception → end
```

The only difference from [01 · Basics](../01-basics/) is the parameter on the
start event. Everything downstream is unchanged — which is the point: how a Flow
is triggered is a property of its start, not of its body.

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `WebhookRequest` | inner, JSON Schema | the process boundary. `event` names what happened, `payload` carries the detail |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure |
| `ExternalConfig` | external | the configuration type |

`event` is a reserved word in C#. The declared field keeps its natural name, and
the code escapes it as `Input.@event`. Naming a field `type`, `class`, `base`,
`event` or `default` is legal in the schema and needs the `@` in every snippet
that touches it — one good reason to avoid such names when you can.

## What you should get back

Started directly, it echoes what it received:

```
{ "event": "order.created", "payload": "{}" }   →   HTTP 200
{"event":"order.created","payload":"{}"}
```

The run log carries `received 'order.created' on the declared route`.

Once the Flow is published, the same process is also reachable at its declared
route, and the caller does not need to know the Flow's name or version.

## Two ways to address a compiled Flow

```
POST /api/v0/bpmn/flowdefinitions/{libraryType}/{libraryName}/{flowName}/Start.json?run=auto
POST /api/v0/bpmn/flowdefinitions/{id}/Start/{version}
```

The first resolves by name and follows the latest compiled version. The second
pins a numeric id and version that exist in one environment only. Prefer the
first for anything you intend to share.

Two things decide whether the call runs at all: `run=auto` — any other value
registers the instance and returns its id **without** running it — and the last
compilation having succeeded. A Flow whose latest compile failed answers
`Last compilation of workflow '…' failed`.

## Why it is built this way

**The route lives on the diagram, not in a gateway configuration.** Reading the
model tells you how it is reached.

**The trigger changes nothing downstream.** The same Flow can be started by hand
during development and by a route in production, with no edit in between.

## Where newcomers stumble

- **`run=auto` is compared as an exact string.** `AUTO` does not run.
- **The route is claimed at publication.** Two Flows declaring the same method
  and path collide; pick a path that names what it accepts.
- **A body is required.** An empty request answers `428 A non-empty request body
  is required` — send `{}` if there is nothing to say.

## Run it

Import `service-config.bpmn` from [03 · Configuration](../03-config-as-flow/)
into a **tenant** library first, under the name `flow-patterns-config`. Then
import this file and compile it.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).

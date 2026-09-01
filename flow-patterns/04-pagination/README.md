# 04 · Handling a result set page by page

More rows than fit in one answer. One step plans the pages, a Sub Process walks
them.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| Sub Process with Multi Instance | `SP_Page` and its `multiInstanceLoopCharacteristics` |
| A collection handed to the Sub Process | the data element `DO_Pages`, named `PageInfo[]` |
| `PackSize` — how many instances run together | the element parameter on `SP_Page` |
| A Sub Process with its own typed boundary | `SP_DO_In` / `SP_DO_Out` inside it |
| `Input` meaning **one element** inside the loop | `T_Page`, first line |
| `Transition.Counter` — which pass this is | the log line in `T_Page` |
| Reaching the outer scope with `Root.` | `Root.Parameters.config.listUrl` in `T_Page` |

## The model

```
start → Get Config → Parse Config → plan the pages → [ handle one page ] → end
                          ↓                            (Multi Instance)
                   handle Exception → end
```

Inside the Sub Process:

```
start → read one page → end
```

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `PageInfo` | inner, **native C#** | one page: `number`, `startIndex`, `size`. The planning step builds a `List<PageInfo>`; the Sub Process receives **one** of them per instance |
| `PageRequest` | inner, JSON Schema | the process boundary; `Input.total` is how many rows exist |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure |
| `ExternalConfig` | external | the configuration type; `pageSize` and `listUrl` come from it |

The `[]` on the data element name is not decoration. `PageInfo[]` is what tells
the engine this element carries a collection. Drop the brackets and the Sub
Process receives the whole list as a single item and runs exactly once — no
error, no warning, just one pass where you expected three.

## What you should get back

```
{ "total": 25 }
```
```
HTTP 200
[{"number":1,"startIndex":0,"size":10},
 {"number":2,"startIndex":10,"size":10},
 {"number":3,"startIndex":20,"size":10}]
```

Twenty-five rows at ten per page make three pages, the last one short. The run
log carries one line per page, each naming the URL that page would read:
`page 2 would read https://jsonplaceholder.typicode.com/posts?_start=10&_limit=10, pass 2`.

## Why it is built this way

**Planning and walking are separate steps.** The planning step is pure
arithmetic: it decides how many pages there are and what each one covers. Only
then does the Sub Process start. That separation is what allows the pages to run
in parallel — a loop that discovers the next page from the previous answer cannot.

**The page size comes from the configuration.** It is a setting, not a constant:
one place decides it, and every Flow that pages agrees.

**The Sub Process declares its own input and output types.** Without them the
compiler stops with `WorkflowNodeSubProcessGenerator::Generate: input or output
type is empty`. A Sub Process is a process: it has a boundary like any other.

## Where newcomers stumble

- **`Input` inside the Sub Process is one element, not the set.** Cast it to the
  element type (`(PageInfo)Input`) and work with that.
- **`Parameters` inside a Sub Process is not the outer one.** Reach the parent
  scope through `Root.` — `Root.Parameters.config.listUrl`.
- **Sequential or parallel is a property of the Sub Process, not of the code.**
  Horizontal bars mean one after another, vertical bars mean together. `PackSize`
  caps how many run at once.

## Run it

Import `service-config.bpmn` from [03 · Configuration](../03-config-as-flow/)
into a **tenant** library first, under the name `flow-patterns-config`. Then
import this file and compile it.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).

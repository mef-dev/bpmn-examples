# 06 · Streaming responses and SSE

Reading a response that arrives in chunks, and sending each chunk out to clients immediately.

## When to use

LLM streaming, Server-Sent Events, any long response that cannot be waited for in full.

## Files

| File | What it shows |
|---|---|
| `llm-stream.bpmn` | branching on "stream / no stream" by `Content-Type`, line-by-line reading, stop flag |
| `sse-roundtrip.bpmn` | the full cycle: subscribe, send, receive, verify what was received |

## Platform functions used

`RestApi` · `RestApi/GET`

## Reserved words

`#Previous.Reader` · `#Previous.IsStreamResponse` · `#Previous.StatusCode` · `#Previous.Headers[…]` · `Action.BoundaryEvents[].Raise()` · `Parameters`

## What to watch for

- `#Previous.Reader.ReadLine()` reads one line; at the end always call
  `.Dispose()`, otherwise the connection stays open.
- The branch condition checks `Content-Type`. If the service adds `charset`, a
  strict equality test will not match — check for containment instead.
- Reading is stopped through a flag parameter that the chunk handler sets.
- Delivery goes through `ThrowMessageEvent` with `tsk_ProcessName: "Server-side events"`;
  it requires the `Platform` library to be linked.

---
For the data types in these examples, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).

# 04 · Paginating large result sets

When there is more data than fits into one response: the list of pages is prepared by a separate step, and each page is handled by a Sub Process.

## When to use

A result set that does not fit into a single request, or the processing of a set of files.

## Files

| File | What it shows |
|---|---|
| `sync-folder-paged.bpmn` | a Sub Process with Multi Instance, `PackSize`, nested Call Activities |

## Platform functions used

`RestApi` · `JsonPath`

## Reserved words

`Input` (an element of the set) · `Transition.Counter` · `PackSize`

## What to watch out for

- A Sub Process with Multi Instance receives **one element** of the set in
  `Input`, not the whole set. If it ran only once, the `[]` was forgotten on the
  data element.
- `PackSize` sets the pack size; sequential mode (horizontal bars) versus
  parallel mode (vertical bars) is a property of the Sub Process, not of the
  code.
- The pass counter is `Transition.Counter` (also known as `#PassCounter`).

---
For the data types in these examples, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).

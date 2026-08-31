# 08 · Agent scenarios

Calling a language model, and preparing a Structured Prompt for it.

## When to use

An LLM inside a process; assembling a prompt from a template and data.

## Files

| File | What it shows |
|---|---|
| `compile-structured-prompt.bpmn` | **pure logic**: seven Expression steps, no functions and no storage — working with JSON, templates and substitution |
| `ai-completions.bpmn` | a call to `AI/Completions`, two Call Activity nodes with different reference formats |

## Platform functions used

`AI/Completions`

## Reserved words

`Parameters` as an accumulator · `#Previous` · `Logger`

## What to watch for

- `compile-structured-prompt` is the best example for the section on types:
  it shows how `Parameters.result` accumulates the result across seven steps, and how
  `new JSON(x).JsonPath(expr)` takes a value out of an arbitrary structure.
- Errors here are a `throw` with a code (`template_not_found`,
  `structured_prompt_not_declared`). The error code is part of the contract, not text
  for a human to read.
- The `Functions` block in the file is a **snapshot** of the signature at the moment of
  saving, not a contract. The contract is defined by the platform: at compile time the
  signature is taken from there. If an example does not build, save it again in the
  current designer.

---
For the data types in these examples, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).

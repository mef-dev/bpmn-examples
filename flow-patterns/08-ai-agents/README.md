# 08 · A prompt is data, not a string

The step that talks to a model is the easy half. The half worth learning is
building the request as typed data, so it can be reviewed, tested and changed
without rereading a wall of concatenation.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| A platform type reached by reference | `types://external/ai/UCP.Common.AI.ChatCompletionsRequestMessageViewModel` |
| Declaring a platform library | the `ai` entry in `UsedLibs` |
| Giving an external type a short alias | `ChatMessage` in `ExternalTypes` |
| Building a message list instead of a string | `T_Compose` |
| Returning a collection as the process result | the `return messages;` at the end |

## The model

```
start → Get Config → Parse Config → compose the prompt → end
                          ↓
                   handle Exception → end
```

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `ChatMessage` | external → `types://external/ai/UCP.Common.AI.ChatCompletionsRequestMessageViewModel` | the platform's own chat message. Aliased short so the code stays readable; the full name lives in one line of `ExternalTypes` |
| `PromptRequest` | inner, JSON Schema | the process boundary; `question` and `tone` |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure |
| `ExternalConfig` | external | the configuration type |

Two different external types sit side by side here, and the difference matters.
`ExternalConfig` reaches into **another Flow** (`types://external/<alias>/<Type>`
where the alias is bound to a Call Activity). `ChatMessage` reaches into a
**platform library** (`types://external/ai/<full .NET name>` where `ai` is bound
to `libs://common/ai`). Same syntax, two sources.

## What you should get back

```
{ "question": "What is BPMN?", "tone": "plain" }
```
```
HTTP 200
[{"role":"system","content":"Answer in a plain tone.","tool_calls":null,
  "tool_call_id":null,"name":null},
 {"role":"user","content":"What is BPMN?","tool_calls":null,
  "tool_call_id":null,"name":null}]
```

The fields you never set come back as `null` — that is the platform's own type
answering, not a shape this file invented. Feeding that array to a model is one
more step; getting the array right is what this example is for.

## What this example does not do

**It does not call the model.** The `AI/Completions` built-in exists and is
declared in the platform catalogue, but its body reaches for
`Action.BoundaryEvents` and a cancellation token that are not in scope where the
engine inlines it, so a model that calls it fails to compile with:

```
error CS0117: 'Action' does not contain a definition for 'BoundaryEvents'
error CS0103: The name 'CT' does not exist in the current context
```

That is a gap in the platform, not something you can work around in the diagram.
The example therefore stops where it can still be honest: at a correctly built,
correctly typed request.

## Why it is built this way

**Messages are a list, not a concatenation.** The system message sets behaviour,
the user message asks. Kept apart, either can be changed, reviewed or tested
alone; glued into one string, neither can.

**The type is referenced, not copied.** Declaring your own `ChatMessage` class
would work until the platform's version gains a field. The reference cannot drift.

**The alias is short on purpose.** `ChatCompletionsRequestMessageViewModel` in
every line would bury the logic; the long name appears once.

## Where newcomers stumble

- **Forgetting the library.** `types://external/ai/…` resolves only if `ai` is in
  `UsedLibs`. Without it the alias silently becomes `#error` and the failure
  arrives later, as an unrelated-looking compile error.
- **Building the prompt in the caller.** Then two callers drift apart. Let the
  Flow own the shape.
- **Expecting the platform type to be minimal.** It has fields you will not use;
  they come back as `null` and that is correct.

## Run it

Import `service-config.bpmn` from [03 · Configuration](../03-config-as-flow/)
into a **tenant** library first, under the name `flow-patterns-config`. Then
import this file and compile it.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).

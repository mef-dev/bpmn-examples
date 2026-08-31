# Type design in BPMN Flow

This section is not about C#. It is about **how to design the data of your
process** so that the diagram stays readable and errors do not appear in the
middle of a run.

Read it before you draw the first element: the type chosen at the start
determines how much code you will have to write later.

---

## 1. Why this is a problem at all

Every element of the diagram receives data from the previous one and passes its
own data on. The platform does not ask "what type is this" every time — it
determines the type **once, at compile time**, from what you declared in the type
editor and in the parameters.

Hence the rule that explains almost every beginner's error:

> If you have not said which type travels along the pipeline, the platform works
> with it as "something" (`object` / `Json`). That compiles, but it fails on the
> first attempt to access a field.

Three typical symptoms:

| What the author sees | What actually happened |
|---|---|
| `Cannot access property 'id' of object` | an untyped `object` travels along the pipeline |
| `Unable to cast object of type 'JObject' to …` | the data arrived as JSON, but the code expects a class |
| `Object reference not set to an instance` | the field is in the schema, but it was absent from the input data |

None of the three is a "platform bug"; each is a **skipped type design step**.

---

## 2. Four ways to declare a type — and when to use which

In the **Types** editor a type is defined in one of four ways. They are not
equivalent: each has its own area of use.

| Way | What it looks like | When to use it |
|---|---|---|
| **JSON Schema** | `{"$schema": "http://json-schema.org/draft-06/schema#", …}` | a contract with the outside world: process input, REST response body, queue message |
| **C# class** | `public class PageInfo { public int StartIndex {get;set;} … }` | an internal structure of the process that nobody outside sees |
| **External type** | `types://external/<flow>/<Type>` | a type already declared in another Flow or library — so as not to duplicate it |
| **Platform type** | `types://core/System.Exception` | system types |

**Rule of thumb.** The process boundary is JSON Schema. Everything that lives
inside and does not cross the boundary is a C# class: it is shorter, more
readable, and gives hints in the editor.

```
        ┌──────────── process boundary ────────────┐
JSON →  │  class  →  class  →  class   →  class    │ → JSON
Schema  │      (internal workings)                 │  Schema
        └──────────────────────────────────────────┘
```

---

## 3. Seven recommendations on type design

### 3.1 One step — one type

Do not build a "universal" object that is dragged through the whole process and
half of whose fields are empty at every step. Let every step have its own input
and its own output — the diagram then reads without comments.

Bad: `ProcessData` with 20 fields, of which 3 are filled in at each step.
Good: `PageInfo` → `FileLinkInfo[]` → `EmailBody`.

### 3.2 An accumulator is a parameter, not the result of a step

If you need to collect a result piece by piece, declare a process **parameter**
of the required type and add to it, and send along the pipeline what the next
step actually needs.

```
Parameters.result.structuredPrompt = template;   // accumulate
return Parameters.result;                        // and pass it on
```

That is how `08-ai-agents/compile-structured-prompt.bpmn` is built: seven steps
in a row add to a single `CompilationResult`.

### 3.3 A collection is a type with `[]`, not "an array of something"

If a data element is named `FileLinkInfo[]`, the platform knows it is a set, and
a Sub Process with Multi Instance will receive **one element** in `Input`, not
the whole array. Forgetting the `[]` is the most common reason for "why did my
loop run only once".

### 3.4 Do not mix JSON and a class in one step

If JSON arrives at the input and a class is needed further on, make a
**separate conversion step** and name it honestly (`Parse Config`,
`Json Convert`). Do not hide the conversion inside a step that does something
else: when it fails, you will look for the error in the wrong place.

```
var cfg = ((JSON)#Previous).Cast<ExternalConfig>();   // a separate step
Parameters.config = cfg;
return cfg;
```

### 3.5 An external type is declared by both sides

If Flow A calls Flow B and passes an object, the type has to be declared **in
both** — in B as its own, in A as external
(`types://external/<flowB>/<Type>`). Otherwise A gets an `object` back, and
field access will fail at run time.

### 3.6 Mark an optional field explicitly

In JSON Schema — by leaving it out of `required`; in C# — with `?` for value
types (`int?`, `DateTime?`). An empty field that the platform treats as required
gives `Object reference not set` at the most inconvenient moment.

### 3.7 A type at the boundary is the documentation of your API

The input schema of a process is what an integrator will see in Swagger. Name
the fields the way the domain names them (`serviceOrderId`, not `id2`), and add
`title` — it ends up in the generated specification.

---

## 4. Type casting — when it is needed and how not to fear it

A cast is when you tell the platform: "what arrived as something generic is in
fact this type". It is needed in exactly three situations.

### 4.1 The data arrived from outside as JSON

```
var cfg = ((JSON)#Previous).Cast<ExternalConfig>();
```

`#Previous` here is "something". `(JSON)` says: this is JSON.
`.Cast<ExternalConfig>()` says: lay it out into the fields of this type. **If the
structure does not match, the fields will be empty rather than an error.** So
right after a Cast it is worth logging a key field:

```
Logger.LogInformation($"connection str = '{cfg.db_connection_str}'");
```

### 4.2 The data arrived after a parallel gateway

After a parallel gateway `#Previous` is a **dictionary**, not an object. Access
it by node name:

```
var list = (List<string>)#Previous["Activity_Read_Response"];
```

Without the node name you get a dictionary and will not understand why "the
field is missing".

### 4.3 Data from SQL

`Collection` is a set of rows with dynamic fields. The fields are accessed by
column name, and the compiler does not check them (it does not know them):

```
var rows = DataAssociations.p_get_grid.Query<TreeNodeGridData>();
```

By specifying the type in `Query<T>()` you get a typed set straight away — and
then work without casts. That is better than `Query()` without a type.

---

## 5. Checklist before the first run

- [ ] The process input is described by JSON Schema, with fields named as in the domain
- [ ] Every data object on the diagram has a type (not empty)
- [ ] Collections have `[]` in the name
- [ ] The JSON → class conversion is moved into a separate step
- [ ] External types are declared on both sides of the call
- [ ] Optional fields are not in `required` / are marked with `?`
- [ ] After every Cast there is a `Logger.LogInformation` with a key field
- [ ] After a parallel gateway, access goes through `#Previous["node-name"]`

---

## 6. Where to look next

| Question | Example |
|---|---|
| A minimal pipeline with types | `01-basics/echo-agent.bpmn` |
| JSON → typed configuration | `03-config-as-flow/get-config.bpmn` |
| An accumulator in a parameter | `08-ai-agents/compile-structured-prompt.bpmn` |
| A collection + Multi Instance | `04-pagination/sync-folder-paged.bpmn` |
| A cast after a parallel gateway | `05-events-and-signals/boundary-event-fanout.bpmn` |
| External types between Flows | `03-config-as-flow/send-links.bpmn` |

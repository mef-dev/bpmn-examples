# Flow patterns

BPMN Flow examples for the MEF.DEV platform, grouped by the problem they
solve. Each group is self-contained: open the one that matches your
situation.

All examples are anonymized: addresses look like `http://servername:port/resource`,
passwords are empty, and connection strings are read from configuration. Substitute
your own values before running them.

| Group | About | Key |
|---|---|---|
| [01 · Basics](01-basics/) | the data pipeline from input to output | `#Previous`, `Global` |
| [02 · Errors](02-error-handling/) | an error as a separate branch of the diagram | `#PreviousData`, `StatusCode` |
| [03 · Configuration](03-config-as-flow/) | moving settings into a separate Flow | `Root.Parameters` |
| [04 · Pagination](04-pagination/) | large result sets and sets of files | Multi Instance, `PackSize` |
| [05 · Events](05-events-and-signals/) | signal versus message; an event raised from code | `Action.BoundaryEvents[].Raise()` |
| [06 · Streaming](06-streaming-sse/) | streaming responses and SSE | `#Previous.Reader` |
| [07 · Triggers](07-triggers/) | what starts a process | `StartSignalRoute` |
| [08 · Agents](08-ai-agents/) | LLMs and structured prompts | `AI/Completions` |

**Before your first Flow**, read [TYPE-DESIGN.md](TYPE-DESIGN.md) — on how to
design data types. Most errors that look like a platform failure are a skipped
type design step.

## Companion Flows

A Flow takes its settings from a separate configuration Flow, reached through a
Call Activity (`activities://bpmn-mnemo/<libType>/<libName>/<flowName>/#latest`),
and it declares the shared types of that Flow as external
(`types://external/<lib>/<Type>`). The indirection is deliberate: it is what keeps
a model independent of the environment it runs in, and what keeps one declaration
of a type instead of a copy inside every Flow that touches it.

The consequence for you: an example that references a companion Flow will not
compile until that companion exists in the target library, under the name the
reference uses. Import the companion first.

| Example | Import first |
|---|---|
| `03-config-as-flow/send-links.bpmn` | `03-config-as-flow/get-config.bpmn`, named `test-config` |
| `01-basics/echo-agent.bpmn` | `ama_base_agent` |
| `02-error-handling/event-error-routing.bpmn` | `EVENT_BankFeed_Sync_config` |
| `04-pagination/sync-folder-paged.bpmn` | `sharepoint-get-folders` |
| `08-ai-agents/ai-completions.bpmn` | `Create_Config_Yiz_Http` |
| `06-streaming-sse/sse-roundtrip.bpmn` | a Kafka configuration named `eventHub-operator` on the stand |

Only the first companion ships with this repository; the others belong to the
environment you import into. Every other example in the table of contents above
compiles on its own.

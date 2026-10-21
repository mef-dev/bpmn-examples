# Smoke test

One Flow that calls every flow-patterns example and answers with a report: which
capabilities work on the platform that ran it, and the error for each one that
does not.

| Answer | Meaning |
|---|---|
| HTTP 200, the report | every check passed |
| HTTP 500, the report | at least one check failed; each failed line says why |

The report names the platform version that ran the test, taken from the process
itself: the product name and version, the same as on the API's Swagger page.

## What it checks

Each example is called as it is in this repository, with its own example input,
through a Call Activity to the Flow of the same name in the tenant library.

| Check | Example | What a pass proves |
|---|---|---|
| `Parse Config` | the test's own configuration call | the settings returned by a Call Activity are read into `ExternalConfig` |
| `01 first-flow` | `first-flow` | the caller's payload reaches the Flow and comes back |
| `02 error-as-branch, valid order` | `error-as-branch` | a valid request passes the step that may throw |
| `02 error-as-branch, empty order` | `error-as-branch` | a thrown exception ends on the error branch with `orderId is required` |
| `03 bpmn-examples-config` | `service-config.bpmn` | the configuration Flow returns the settings |
| `03 use-config` | `use-config` | a consumer reads the settings through a Call Activity |
| `04 paged-fetch` | `paged-fetch` | Multi Instance Sub Process, one instance per page |
| `05 raise-event` | `raise-event` | a step raises a message boundary event and keeps working |
| `06 stream-response` | `stream-response` | a streamed response is read chunk by chunk |
| `07 http-start` | `http-start` | a Flow with an HTTP start event |
| `08 structured-prompt` | `structured-prompt` | a prompt built as typed chat messages |
| `09 archive-and-link` | `archive-and-link` | a file in a store, an archive and a link to it |

`Parse Config` is in the report only when it fails; the other eleven checks are
always there. A check fails when the example answers from its failure branch,
answers nothing, or answers without the expected marker. When a call itself
throws, its error boundary event records the exception and the test goes on, so
one run reports every failure, not only the first.

## How the model is built

- **One row per example:** an input step, the Call Activity, a check step. The
  input step returns the example input as a JSON string; the called Flow parses
  it into its own input type.
- **The report is a global parameter**, `Parameters.report` of type
  `SmokeReport`. Every step adds to it.
- **The verdict sets the HTTP status** through
  `WorkflowEnvironment.Variables["StatusCode"]`. The body is the report in
  both cases.

## Run it

1. Import `03-config-as-flow/service-config.bpmn` into a tenant library as
   `bpmn-examples-config`, and each example under its own name (`first-flow`,
   `error-as-branch`, …) into the same library. Compile them.
2. Import `smoke-test.bpmn` into that library and compile it.
3. Start it with `{"run":"<label>"}`. The label comes back in the report.

The examples have to be in the library under their own names: a Call Activity
resolves the called Flow by name and binds to its class when the test is
compiled. For the same reason, an example that does not compile stops the test
from compiling — the compiler error names that example and the cause.

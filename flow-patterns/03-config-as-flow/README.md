# 03 · Configuration as a separate Flow

Two files. One holds the settings, the other uses them and never learns which
environment it is running in.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| A Flow whose whole job is to answer with settings | `service-config.bpmn` |
| Call Activity by mnemonic reference | `Get Config` in `use-config.bpmn` |
| `activities://bpmn-mnemo/<libType>/<libName>/<flowName>/#latest` | the `ExternalDefinitionLink` element parameter |
| An external type instead of a copied one | `types://external/ConfigActivity/Config` |
| Casting the answer and parking it | `Parse Config`, which fills `Parameters.config` |
| A native C# type as a declared type | the `Config` class in `service-config.bpmn` |

## The two models

```
service-config.bpmn:   start → resolve the settings → end
                                      ↓ (on error)
                               handle Exception → end

use-config.bpmn:       start → Get Config → Parse Config → build the call → end
                                                 ↓ (on error)
                                          handle Exception → end
```

`Get Config` is a Call Activity: it runs the other Flow and hands back its
answer. `Parse Config` casts that answer once, into `Parameters.config`, so every
later step reads a typed object rather than loose JSON.

## Types it declares

| Type | Where | Kind | How it is used |
|---|---|---|---|
| `Config` | `service-config.bpmn` | inner, **native C#** | the settings themselves: `ratesUrl`, `listUrl`, `login`, `password`, `pageSize`. Declared here and nowhere else |
| `ExternalConfig` | `use-config.bpmn` | external → `types://external/ConfigActivity/Config` | the same type, reached by reference. `ConfigActivity` is the alias bound in `UsedLibs` to the configuration Flow |
| `LookupRequest` | `use-config.bpmn` | inner, JSON Schema | the process boundary of the consumer |
| `ErrorResponse` | both | inner, JSON Schema | the shape of a failure |

**This is the mechanism worth understanding.** The alias in `UsedLibs` points at
a Flow; `types://external/<alias>/<Type>` then reaches inside that Flow for a
type it declares. No copy is made. If `Config` grows a field, consumers see it
after a recompile — and if it loses one, they fail to compile instead of failing
at midnight.

## What you should get back

The configuration Flow answers with the settings:

```
{}   →   HTTP 200
{"ratesUrl":"https://api.frankfurter.dev/v1",
 "listUrl":"https://jsonplaceholder.typicode.com/posts",
 "login":"","password":"","pageSize":10}
```

The consumer builds a call out of them:

```
{ "key": "EUR" }   →   HTTP 200
{"key":"https://api.frankfurter.dev/v1/latest?base=EUR"}
```

Note what the consumer never contains: the host name. Move the Flow to another
environment, point the configuration Flow somewhere else, and this reply changes
without the consumer being touched.

## Why it is built this way

**The reference is mnemonic, not numeric.** `activities://bpmn-mnemo/tenant/…`
resolves by *name* and follows `#latest`. The numeric form
`activities://bpmn/<libType>/<libId>/<flowId>/<version>` pins identifiers that
exist in exactly one environment, and it carries no name — it will not resolve
anywhere else. Prefer the mnemonic form in anything you intend to share.

**The library type is `tenant`, not `personal`.** A personal library resolves
only for the account that created it: the platform filters by creator unless the
library type is Tenant. A `personal/…` reference in a shared Flow works for its
author and for nobody else.

**The settings are one type, not five parameters.** Adding a field then means
editing one class, not hunting for every Flow that reads settings.

## Where newcomers stumble

- **The companion must exist before the consumer compiles.** Import
  `service-config.bpmn` first, into a **tenant** library, under the name
  `flow-patterns-config`. Otherwise the consumer fails with `cant resolve class
  name for uri 'activities://bpmn-mnemo/…'`.
- **The alias name must match.** `UsedLibs` binds the alias `ConfigActivity`;
  `types://external/ConfigActivity/Config` uses that exact word. Rename one and
  the type silently becomes `#error`.
- **Passwords belong here, empty or filled — never in the consumer.** Both
  sources used by this group are public, so `login` and `password` stay empty. A
  real deployment fills them in this one file.

## Run it

Import `service-config.bpmn` into a tenant library as `flow-patterns-config` and
compile it. Then import `use-config.bpmn` and compile that.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).

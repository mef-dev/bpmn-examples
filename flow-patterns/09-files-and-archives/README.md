# 09 · Files, folders and a link to the archive

A file is not a variable. It lives in a store, it is reached through a binding
on the diagram, and what you hand back is a link — not the bytes.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| A **Folder** data store | `DS_Folder`, `storeParameters` with `"type": "Folder"` |
| A **File** data store | `DS_File`, `"type": "File"` |
| Binding a store to the step that uses it | `dataInputAssociation` inside `T_Folder` and `T_Archive` |
| Creating a folder before writing into it | `T_Folder`, `IsExists()` then `CreateFolder()` |
| A built-in that writes a file | `T_Write`, `actionType: Function`, `action: IO/Local/File` |
| Packing a file into a zip | `T_Archive`, `GetFile().AddToZip("archive.zip")` |
| A download link the platform issues | `T_Archive`, `archive.CreateLink()` |

## The model

```
start → Get Config → Parse Config → make sure the folder is there
                                          → write one file into it
                                          → pack it and issue a link → end
```

Two stores hang off the steps that use them: the folder off `T_Folder`, the
file off `T_Archive`.

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `ArchiveRequest` | inner, JSON Schema | the process boundary; `Input.note` is the content to write |
| `ArchiveResult` | inner, C# class | what comes back: the folder and the link |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure |
| `ExternalConfig` | external | the configuration Flow, imported the same way as everywhere |

`LocalFolder` and `LocalFile` are not declared by you. They are what the store
bindings answer with: `DataAssociations.DS_Folder.GetFolder()` and
`DataAssociations.DS_File.GetFile()`.

## What you should get back

```
{ "note": "quarterly summary" }   →   HTTP 200

{"folder":"flow-patterns/archive-demo",
 "url":"https://<stand>/s/tenant/21b744842fe98a2329ebd4cb422b21d8"}
```

The link is live: it carries its own authorisation, so it can be handed to
someone who has no session on the stand.

## Why it is built this way

**A folder is a path, not an object of its own.** There is no folder API in the
engine's catalogue — `IO/Local/File` and `IO/Local/Archive` are the only file
functions there is. `flow-patterns/archive-demo` is one string, two levels deep,
and the store treats it as a folder because its `type` says `Folder`.

**The folder is made before anything is written.** Writing does not bring a
missing folder into being; the store answers

```
DirectoryNotFoundException: Could not find a part of the path
'/storage/…/documents/tenant/flow-patterns/archive-demo/note.txt'
```

That is why `T_Folder` comes first, and why it asks `IsExists()` before calling
`CreateFolder()`.

**A store's `object` is taken literally.** Substitution works in the arguments
of a function — `fileContent` here is `{Input.note}` and arrives filled in — but
not in a data store. Measured on a stand with three stores in one run:

```
braced={Input.folder}   bare=Input.folder   literal=reports/2026-09
```

Neither form is replaced. So the location lives in the model and only the
content comes from the caller. Put a path in a store expecting `Input` to reach
it and you will get a folder literally named `{Input.folder}`.

**Every store is bound to a step.** The engine walks the declared stores and
keeps only those found among the node's input associations
(`WorkflowNodeAnalyzer.cs:67`). A store nobody is bound to compiles and then is
not there — `DataAssociations` simply has no such member.

**The archive is made from the file, not the folder.** `LocalFolder` does offer
`AddFolderToZip`, and it would be the better call — but it takes a
`CompressionLevel`, and `System.IO.Compression` is not among the assemblies the
Flow compiler references. The line that would add it is commented out in
`WorkflowReferencesCollection.cs:145`. Until that changes, `LocalFile.AddToZip`
is the reachable route: it takes only a name.

## Where newcomers stumble

- **Expecting `IO/Local/File` to answer with the file.** It writes and returns
  nothing. The next step reaches the file through its own store binding.
- **One property for two stores.** Each `dataInputAssociation` needs its own
  `__targetRef_placeholder` property; they cannot share one.
- **Sending the bytes back.** The result of the process is the link. A file
  travels as a link, not as a payload.

## Run it

Import `service-config.bpmn` from [03 · Configuration](../03-config-as-flow/)
into a **tenant** library first, under the name `flow-patterns-config`. Then
import this file and compile it. It needs no outbound access: everything it
touches is the stand's own document store.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).

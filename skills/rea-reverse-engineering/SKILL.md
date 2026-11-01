---
name: rea-reverse-engineering
description: Use REA to inspect packaged or running software when its behavior cannot be established from a complete source tree, including Electron apps, browser behavior, and native binaries. Use the findings to explain or reconstruct one feature with evidence. Skip for ordinary source-repository analysis.
---

# REA reverse engineering

Use REA when the question depends on a shipped application, package, binary, or observed runtime behavior. For a complete source repository, use normal code search, tracing, and tests first.

Only inspect software the user owns or is authorized to examine. Keep the investigation focused on one feature or behavior.

## Choose an inspection path

- **JavaScript or Electron app:** inspect the application directory or ASAR. Static analysis can trace modules and Electron IPC without launching the app.
- **Native executable or library:** check which analysis provider is available and supported for the target. Native analysis needs a configured engine such as Hopper, Ghidra, or IDA.
- **Browser behavior or network activity:** inspect the selected page and capture a bounded interaction. Use a separate browser profile when connecting to a local debugging endpoint.
- **Other targets:** use the matching guide in the [REA documentation](https://rea.tools/get-started/) to confirm prerequisites and supported platforms.

## Investigate and report

1. State the behavior to explain and identify the target by path or URL, version when known, and relevant platform.
2. Check the REA tools available in this session and read their current input schemas. Tool names and capabilities can vary by REA release.
3. Trace from the user-visible action through the relevant entry point, calls, messages, or requests. Use runtime evidence only when static evidence cannot establish what executes.
4. Separate direct evidence from inference. Cite source locations, functions or addresses, and captured requests or observations. Note ambiguous paths and unexamined code.
5. Check recovered rules against representative inputs. If rebuilding the feature, compare its behavior with the original when that is practical and authorized.
6. Report the answer, evidence, validation performed, and remaining uncertainty. Do not treat an unexamined path as proof that behavior is absent.

## Connection and setup

REA's MCP connection and its investigation skill are separate. Check for available REA tools before diagnosing setup. If the tools are missing, continue with useful source analysis and consult the [setup guide](https://rea.tools/get-started/).

Setup changes the coding agent's configuration and installs the matching REA skill. Do not run setup, install an analysis provider, or change client configuration unless the user has authorized that change. Review the setup plan and verify the connection after an authorized setup. When MCP is unavailable, use an existing REA CLI only if it is installed and within scope.

## References

- [REA setup and target guides](https://rea.tools/get-started/)
- [JavaScript and Electron guide](https://rea.tools/guides/javascript/)
- [Browser and network guide](https://rea.tools/guides/browser/)
- [Native binary guide](https://rea.tools/guides/native/)
- [REA FAQ](https://rea.tools/faq/)

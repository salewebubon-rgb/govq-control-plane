# Source Provenance

## Initial public source baseline

GOVQ Core v0.1.0 begins from a bounded extract of a separately maintained private implementation.

This record establishes source traceability only. It is not a claim that the complete private runtime, the complete public repository, or future modifications share the same qualification status.

## `src/govq/protocol.py`

Private-source baseline SHA-256:

```text
E783D00E078380758D1710104767EB4C231DF496F6BD59FA1A17366723B4DDBC
```

Initial public sanitized SHA-256:

```text
43FE0AE672F07F8CC91D022B713F6DCC01F0C01021D8CD194EE4CC6C7B4EB692
```

The initial public extraction changed wording only:

1. internal phase wording in the module description was replaced by a public GOVQ description;
2. an internal phase identifier in a transport-limit comment was replaced by a generic HTTP-boundary description.

No protocol logic, limits, error taxonomy or validation behavior was intentionally changed during this sanitization.

## `src/govq/providers/model_input.py`

Private-source baseline SHA-256:

```text
27660946D30FB6EE320697BF1AB60F09D51F7205DC15A590303686D6C397B7B1
```

Initial public SHA-256:

```text
27660946D30FB6EE320697BF1AB60F09D51F7205DC15A590303686D6C397B7B1
```

The initial public file is byte-identical to the reviewed source baseline.

## Boundary of the provenance claim

These hashes establish source identity for the two files above.

They do not establish:

- qualification of unrelated modules;
- production deployment status;
- complete runtime qualification;
- security of future adapters;
- network-adapter behavior;
- persistence across process restart;
- research-result validity; or
- qualification of future modified versions.

Every subsequent behavior-changing modification requires its own review and testing.
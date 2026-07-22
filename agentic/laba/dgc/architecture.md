# Think Like an Architect

A common mistake is to place all security logic into one large engine.

The DGC intentionally avoids this.

Instead, every policy has its own evaluator.

```
Policy Engine
        │
        ├── latest_tag.py
        ├── privileged_container.py
        ├── host_network.py
        ├── root_user.py
        └── image_signature.py
```

This plug-in architecture allows new governance checks to be added without
modifying the Policy Engine.

The engine simply discovers the evaluator, executes it, and receives a
PolicyResult.

This design follows the **Open/Closed Principle**:

- **Open for extension** by adding new evaluators.
- **Closed for modification** because the Policy Engine does not need to
  change when new policies are introduced.
  

          AI Agent
               ↓
          Kong Gateway
               ↓
          mTLS Gateway
               ↓
          MCP Server
               ↓
          Deterministic Governance Core (Policy Decision)
               ↓
          Approved Tool
               ↓
          Execution

The MCP Server doesn't decide whether a tool is allowed—it asks the DGC.

That is a very enterprise-friendly pattern because it cleanly separates:

                    Protocol (MCP)
                    Security & Policy (DGC)
                    Execution (the tool)

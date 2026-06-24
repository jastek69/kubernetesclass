

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

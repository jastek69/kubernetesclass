Lab 1C — Introduction to the Model Context Protocol (MCP)
What is MCP?

Imagine you have a very intelligent AI assistant.

It can reason, write code, explain Kubernetes, and answer questions.

But there is one major limitation.

It only knows what you tell it.

It cannot automatically:

    inspect your Kubernetes cluster
    read your Jira tickets
    query your cloud environment
    retrieve files
    execute approved administrative tasks

unless something provides those capabilities.

This is where the Model Context Protocol (MCP) comes in.

Think of MCP Like a USB Port

A laptop is useful by itself.

But when you plug in:

    a keyboard
    a webcam
    an external drive

the laptop gains new capabilities.

MCP works similarly for AI.

It provides a standardized way for AI models to connect to external tools and services.

Instead of every AI vendor inventing a different API for every application, MCP defines a common protocol that allows AI systems to discover and use tools consistently.

Why Was MCP Created?

Before MCP:

    Claude ---- Custom API ---- Jira
    Claude ---- Different API ---- GitHub
    Claude ---- Another API ---- Kubernetes
    Claude ---- Yet Another API ---- AWS

Every integration was unique.

Every company wrote custom code.

Every security review was different.

With MCP:

    Claude
          |
          |
         MCP
          |
    ------------------------------------
    |        |         |         |
    GitHub  Jira     Kubernetes  AWS

Now AI systems communicate with external services using a common protocol.

This makes integrations easier to build, easier to secure, and easier to maintain.

What Problems Does MCP Solve?

Without MCP:

    Every tool requires a custom integration.
    AI developers repeatedly solve the same problem.
    Security policies are inconsistent.
    Authentication differs between applications.

With MCP:

    Standard communication protocol
    Standard tool discovery
    Standard request format
    Easier security controls
    Easier auditing

What Does an MCP Server Actually Do?

Think of the MCP Server as a tool broker.

It answers questions like:

What tools are available?

What parameters does this tool require?

Is this user authorized?

Execute this approved request.

The AI itself does not directly access Kubernetes or Jira.

Instead:

    AI
     |
     | Request
     |
     v
    MCP Server
    
     |
     | Authorized Tool
     |
     v
    Kubernetes

The MCP Server becomes the trusted intermediary.

Example

A user asks: "How many pods are running in namespace app01?"

The AI does not know.

Instead: 

    User
    ↓
    Claude
    ↓
    MCP Server
    ↓
    kubectl get pods -n app01
    ↓
    Results Returned
    ↓
    Claude Explains Results

The AI reasons about the output.

The MCP Server performs the action.

Why This Matters for Security

Imagine an AI connected directly to your Kubernetes cluster.

That would be dangerous.

Instead, the MCP Server provides security controls such as:

    Authentication
    Authorization
    Tool restrictions
    Logging
    Auditing
    Rate limiting

In our architecture we add even more protection:

    AI Agent
    ↓
    mTLS Gateway
    ↓
    MCP Server
    ↓
    OPA Policy Check
    ↓
    Approved Tool
    ↓
    Kubernetes

Notice that several security layers exist before any command reaches the cluster.




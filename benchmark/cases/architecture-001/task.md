# Review task: Invoice service shared by HTTP and worker

Review the supplied JavaScript modules for architecture, runtime correctness, and reliability.

## Contract
- InvoiceService is a framework-independent application service.
- It is invoked by both an HTTP controller and a background worker.
- Both entry points must create an invoice for an explicitly supplied customer ID.
- Authorization is performed at the appropriate entry boundary; the service must not depend on an HTTP request object.
- Do not report stylistic preferences as defects. Explain concrete failure conditions and impacts. Do not modify files or claim execution.

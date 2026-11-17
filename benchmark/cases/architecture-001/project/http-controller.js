import { InvoiceService } from "./invoice-service.js";

const invoiceService = new InvoiceService();

export async function createInvoiceHttp(req, res) {
  if (!req.user?.permissions?.includes("invoice:create")) {
    return res.status(403).end();
  }
  const invoice = await invoiceService.createInvoice(req, req.body);
  return res.status(201).json(invoice);
}

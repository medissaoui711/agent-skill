import { InvoiceService } from "./invoice-service.js";

const invoiceService = new InvoiceService();

export async function createScheduledInvoice(job) {
  return invoiceService.createInvoice(undefined, job.invoice);
}

import { invoiceRepository } from "./invoice-repository.js";

export class InvoiceService {
  async createInvoice(req, invoiceInput) {
    const customerId = req.user.id;
    return invoiceRepository.insert({
      customerId,
      amount: invoiceInput.amount,
      currency: invoiceInput.currency
    });
  }
}

import { Prisma, PrismaClient } from "@prisma/client";

export class InvoiceService {
  constructor(private readonly prisma: PrismaClient) {}

  async getInvoice(id: string): Promise<
    Prisma.InvoiceGetPayload<{ include: { items: true } }> | null
  > {
    return this.prisma.invoice.findUnique({
      where: { id },
      include: { items: true },
    });
  }
}

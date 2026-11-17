// Synthetic persistence adapter used by this case fixture.
export const invoiceRepository = {
  async insert(record) {
    return { id: "inv-synthetic", ...record };
  }
};

export async function buildOrderSummary(orders, database) {
  const summary = [];

  for (const order of orders) {
    const customer = await database.getCustomerById(order.customerId);
    summary.push({
      orderId: order.id,
      total: order.total,
      customerName: customer?.displayName ?? "Unknown"
    });
  }

  return summary;
}

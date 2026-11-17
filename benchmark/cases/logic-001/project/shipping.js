export function calculateShipping(subtotal, customer) {
  const qualifiesForFreeShipping =
    customer.isMember || subtotal >= 100;

  return qualifiesForFreeShipping ? 0 : 8;
}

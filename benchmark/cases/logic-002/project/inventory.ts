type Inventory = { sku: string; available: number };
type Reservation = { sku: string; quantity: number };

const inventory = new Map<string, Inventory>([
  ["SKU-1", { sku: "SKU-1", available: 5 }],
]);

export async function reserve(input: Reservation): Promise<boolean> {
  const current = inventory.get(input.sku);
  if (!current || current.available < input.quantity) return false;

  await Promise.resolve();

  inventory.set(input.sku, {
    ...current,
    available: current.available - input.quantity,
  });
  return true;
}

export function getAvailable(sku: string): number | undefined {
  return inventory.get(sku)?.available;
}

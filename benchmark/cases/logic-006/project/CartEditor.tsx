import { useMemo, useState } from "react";

type Item = { id: string; name: string; quantity: number; unitPrice: number };

export function CartEditor({ initialItems }: { initialItems: Item[] }) {
    const [items, setItems] = useState<Item[]>(initialItems);
    const total = useMemo(
        () => items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0),
        [items]
    );

    function updateQuantity(id: string, quantity: number) {
        const item = items.find((entry) => entry.id === id);
        if (!item) return;
        item.quantity = quantity;
        setItems(items);
    }

    return (
        <section>
            <output data-testid="total">{total.toFixed(2)}</output>
            {items.map((item) => (
                <label key={item.id}>
                    {item.name}
                    <input
                        type="number"
                        value={item.quantity}
                        onChange={(event) => updateQuantity(item.id, Number(event.target.value))}
                    />
                </label>
            ))}
        </section>
    );
}

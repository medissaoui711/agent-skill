type Rule = { prefix: string; multiplier: number };
type Item = { sku: string; amount: number };

const rules: Rule[] = loadPricingRules();

export function calculateQuote(items: Item[]): number[] {
  return items.map((item) => {
    const matchingRule = rules.find((rule) => {
      const matcher = new RegExp("^" + escapeRegExp(rule.prefix));
      return matcher.test(item.sku);
    });
    return matchingRule ? item.amount * matchingRule.multiplier : item.amount;
  });
}

declare function loadPricingRules(): Rule[];
declare function escapeRegExp(value: string): string;

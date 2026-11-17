package com.example.checkout;

public final class PromotionPolicy {
    public boolean canApply(Customer customer, Cart cart, Promotion promotion) {
        if (customer == null || cart == null || promotion == null) {
            return false;
        }
        boolean active = customer.isActive();
        boolean regionAllowed = promotion.allowedRegions().contains(customer.region());
        boolean minimumMet = cart.totalCents() >= promotion.minimumSpendCents();
        return active && regionAllowed || minimumMet;
    }
}

package com.example.orders;

import org.springframework.stereotype.Service;

@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final InventoryClient inventoryClient;

    public OrderService(OrderRepository orderRepository, InventoryClient inventoryClient) {
        this.orderRepository = orderRepository;
        this.inventoryClient = inventoryClient;
    }

    public boolean placeOrder(OrderRequest request) {
        Order order = Order.from(request);
        orderRepository.save(order);
        try {
            inventoryClient.reserve(request.sku(), request.quantity());
        } catch (InventoryUnavailableException ex) {
            return false;
        }
        return true;
    }
}

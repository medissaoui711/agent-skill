package com.example.orders;

import com.example.users.UserService;
import org.springframework.stereotype.Service;

@Service
public class OrderService {
    private final UserService userService;
    private final OrderRepository orderRepository;

    public OrderService(UserService userService, OrderRepository orderRepository) {
        this.userService = userService;
        this.orderRepository = orderRepository;
    }

    public boolean hasOpenOrders(long userId) {
        if (!userService.userExists(userId)) return false;
        return orderRepository.existsByUserIdAndStatus(userId, "OPEN");
    }
}

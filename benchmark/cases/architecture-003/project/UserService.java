package com.example.users;

import com.example.orders.OrderService;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    private final OrderService orderService;
    private final UserRepository userRepository;

    public UserService(OrderService orderService, UserRepository userRepository) {
        this.orderService = orderService;
        this.userRepository = userRepository;
    }

    public boolean userExists(long userId) {
        return userRepository.existsById(userId);
    }

    public boolean canCloseAccount(long userId) {
        return !orderService.hasOpenOrders(userId);
    }
}

package com.example.users;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

@RestController
@RequestMapping("/api/profile")
public final class UserProfileController {
    private final UserRepository users;

    public UserProfileController(UserRepository users) {
        this.users = users;
    }

    @PutMapping("/{id}")
    public ResponseEntity<User> update(
            @PathVariable Long id,
            @RequestBody User user) {
        user.setId(id);
        return ResponseEntity.ok(users.save(user));
    }
}

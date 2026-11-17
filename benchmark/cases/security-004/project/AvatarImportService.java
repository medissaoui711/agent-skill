package com.example.avatar;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class AvatarImportService {
    private final RestClient restClient;

    public AvatarImportService(RestClient.Builder builder) {
        this.restClient = builder.build();
    }

    public byte[] importAvatar(String imageUrl) {
        return restClient.get()
                .uri(imageUrl)
                .retrieve()
                .body(byte[].class);
    }
}

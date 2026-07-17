package com.stadiumsense.ai.controller;

import com.stadiumsense.ai.dto.ChatRequest;
import com.stadiumsense.ai.dto.ChatResponse;
import com.stadiumsense.ai.service.ChatService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/chat")
public class ChatController {

    private final ChatService chatService;

    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    @PostMapping
    public ResponseEntity<ChatResponse> chat(@Valid @RequestBody ChatRequest request) {
        ChatResponse response = chatService.processChat(request);
        return ResponseEntity.ok(response);
    }
}

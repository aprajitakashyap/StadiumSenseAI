package com.stadiumsense.ai.service;

import com.stadiumsense.ai.dto.ChatRequest;
import com.stadiumsense.ai.dto.ChatResponse;
import org.springframework.stereotype.Service;

@Service
public class ChatService {

    private final ContextService contextService;
    private final GeminiService geminiService;

    public ChatService(ContextService contextService, GeminiService geminiService) {
        this.contextService = contextService;
        this.geminiService = geminiService;
    }

    public ChatResponse processChat(ChatRequest request) {
        String dbContext = contextService.buildContext(request.message());
        String aiResponse = geminiService.chat(request.message(), dbContext, request.language());
        return new ChatResponse(aiResponse);
    }
}

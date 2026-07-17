package com.stadiumsense.ai.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

public record ChatRequest(
        @NotBlank(message = "Message must not be blank")
        String message,

        @Pattern(regexp = "en|es|fr", message = "Language must be 'en', 'es', or 'fr'")
        String language
) {
    // Default language to English if not provided
    public String language() {
        return (language == null || language.isBlank()) ? "en" : language;
    }
}

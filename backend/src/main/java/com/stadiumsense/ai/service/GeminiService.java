package com.stadiumsense.ai.service;

import com.google.genai.Client;
import com.google.genai.types.GenerateContentResponse;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class GeminiService {

    private static final Logger log = LoggerFactory.getLogger(GeminiService.class);

    private static final String SYSTEM_PROMPT =
        "You are StadiumSense AI. Your responsibility is to assist visitors inside FIFA World Cup stadiums. " +
        "Answer politely. Provide accurate stadium information. " +
        "Recommend accessible routes whenever required. " +
        "If information is unavailable, clearly state that instead of guessing. " +
        "Respond only in the requested language.";

    @Value("${gemini.api.key:}")
    private String apiKey;

    @Value("${gemini.model:gemini-1.5-flash}")
    private String modelName;

    private Client geminiClient;

    @PostConstruct
    public void init() {
        if (apiKey == null || apiKey.isBlank()) {
            log.warn("GEMINI_API_KEY is not set. Chat endpoint will return a fallback response.");
            return;
        }
        this.geminiClient = new Client.Builder().apiKey(apiKey).build();
        log.info("Gemini client initialized with model: {}", modelName);
    }

    /**
     * Sends a chat message to Gemini with injected DB context and system prompt.
     *
     * @param userMessage  the user's question
     * @param dbContext    retrieved context from the database
     * @param language     target language code: en, es, fr
     * @return AI-generated response string
     */
    public String chat(String userMessage, String dbContext, String language) {
        if (geminiClient == null) {
            return getFallbackResponse(language);
        }

        String languageInstruction = getLanguageInstruction(language);
        String fullPrompt = buildFullPrompt(dbContext, userMessage, languageInstruction);

        try {
            GenerateContentResponse response = geminiClient.models.generateContent(
                modelName,
                fullPrompt,
                null
            );
            String text = response.text();
            return text != null ? text.trim() : getFallbackResponse(language);
        } catch (Exception e) {
            log.error("Error calling Gemini API: {}", e.getMessage(), e);
            return getErrorResponse(language);
        }
    }

    private String buildFullPrompt(String dbContext, String userMessage, String languageInstruction) {
        return SYSTEM_PROMPT + "\n\n" +
               languageInstruction + "\n\n" +
               "=== STADIUM DATABASE CONTEXT ===\n" +
               dbContext + "\n" +
               "=== USER QUESTION ===\n" +
               userMessage;
    }

    private String getLanguageInstruction(String language) {
        return switch (language) {
            case "es" -> "IMPORTANT: You MUST respond entirely in Spanish (Español).";
            case "fr" -> "IMPORTANT: You MUST respond entirely in French (Français).";
            default   -> "IMPORTANT: You MUST respond entirely in English.";
        };
    }

    private String getFallbackResponse(String language) {
        return switch (language) {
            case "es" -> "Lo siento, el servicio de IA no está disponible en este momento. Por favor, consulte al personal del estadio.";
            case "fr" -> "Désolé, le service IA n'est pas disponible pour le moment. Veuillez consulter le personnel du stade.";
            default   -> "Sorry, the AI service is not configured. Please ask stadium staff for assistance.";
        };
    }

    private String getErrorResponse(String language) {
        return switch (language) {
            case "es" -> "Ocurrió un error al procesar su solicitud. Por favor, inténtelo de nuevo.";
            case "fr" -> "Une erreur s'est produite lors du traitement de votre demande. Veuillez réessayer.";
            default   -> "An error occurred while processing your request. Please try again.";
        };
    }
}

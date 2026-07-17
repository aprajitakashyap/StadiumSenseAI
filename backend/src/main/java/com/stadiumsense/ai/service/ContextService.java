package com.stadiumsense.ai.service;

import com.stadiumsense.ai.model.Faq;
import com.stadiumsense.ai.model.Location;
import com.stadiumsense.ai.repository.FaqRepository;
import com.stadiumsense.ai.repository.LocationRepository;
import com.stadiumsense.ai.repository.StadiumRepository;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ContextService {

    private final LocationRepository locationRepository;
    private final FaqRepository faqRepository;
    private final StadiumRepository stadiumRepository;

    public ContextService(LocationRepository locationRepository,
                          FaqRepository faqRepository,
                          StadiumRepository stadiumRepository) {
        this.locationRepository = locationRepository;
        this.faqRepository = faqRepository;
        this.stadiumRepository = stadiumRepository;
    }

    /**
     * Builds a context string by extracting keywords from the user message
     * and pulling relevant locations and FAQs from the database.
     */
    public String buildContext(String userMessage) {
        StringBuilder ctx = new StringBuilder();

        // Stadium info
        stadiumRepository.findAll().stream().findFirst().ifPresent(stadium -> {
            ctx.append("=== STADIUM INFO ===\n");
            ctx.append("Name: ").append(stadium.getStadiumName()).append("\n");
            ctx.append("City: ").append(stadium.getCity()).append("\n");
            ctx.append("Country: ").append(stadium.getCountry()).append("\n\n");
        });

        // Keyword-matched locations
        List<Location> matchedLocations = findRelevantLocations(userMessage);
        if (!matchedLocations.isEmpty()) {
            ctx.append("=== RELEVANT LOCATIONS ===\n");
            matchedLocations.forEach(loc ->
                ctx.append("- ").append(loc.getLocationName())
                   .append(" [").append(loc.getCategory()).append("]\n")
            );
            ctx.append("\n");
        } else {
            // Provide all locations as fallback context
            List<Location> allLocations = locationRepository.findAll();
            ctx.append("=== ALL STADIUM LOCATIONS ===\n");
            allLocations.forEach(loc ->
                ctx.append("- ").append(loc.getLocationName())
                   .append(" [").append(loc.getCategory()).append("]\n")
            );
            ctx.append("\n");
        }

        // Keyword-matched FAQs
        List<Faq> matchedFaqs = findRelevantFaqs(userMessage);
        if (!matchedFaqs.isEmpty()) {
            ctx.append("=== RELEVANT FAQs ===\n");
            matchedFaqs.forEach(faq ->
                ctx.append("Q: ").append(faq.getQuestion()).append("\n")
                   .append("A: ").append(faq.getAnswer()).append("\n\n")
            );
        }

        return ctx.toString();
    }

    private List<Location> findRelevantLocations(String message) {
        List<String> keywords = extractKeywords(message);
        return keywords.stream()
                .flatMap(kw -> locationRepository.findByKeyword(kw).stream())
                .distinct()
                .collect(Collectors.toList());
    }

    private List<Faq> findRelevantFaqs(String message) {
        List<String> keywords = extractKeywords(message);
        return keywords.stream()
                .flatMap(kw -> faqRepository.findByKeyword(kw).stream())
                .distinct()
                .collect(Collectors.toList());
    }

    private List<String> extractKeywords(String message) {
        // Split on whitespace/punctuation and filter short words
        return Arrays.stream(message.toLowerCase().split("[\\s,\\.!?;:]+"))
                .filter(word -> word.length() > 3)
                .distinct()
                .collect(Collectors.toList());
    }
}

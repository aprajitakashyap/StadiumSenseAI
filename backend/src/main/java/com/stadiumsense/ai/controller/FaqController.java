package com.stadiumsense.ai.controller;

import com.stadiumsense.ai.model.Faq;
import com.stadiumsense.ai.repository.FaqRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/faq")
public class FaqController {

    private final FaqRepository faqRepository;

    public FaqController(FaqRepository faqRepository) {
        this.faqRepository = faqRepository;
    }

    @GetMapping
    public ResponseEntity<List<Faq>> getAllFaqs() {
        return ResponseEntity.ok(faqRepository.findAll());
    }
}

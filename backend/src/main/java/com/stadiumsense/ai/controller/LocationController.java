package com.stadiumsense.ai.controller;

import com.stadiumsense.ai.model.Location;
import com.stadiumsense.ai.repository.LocationRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/locations")
public class LocationController {

    private final LocationRepository locationRepository;

    public LocationController(LocationRepository locationRepository) {
        this.locationRepository = locationRepository;
    }

    @GetMapping
    public ResponseEntity<List<Location>> getAllLocations() {
        return ResponseEntity.ok(locationRepository.findAll());
    }
}

package com.stadiumsense.ai.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "stadium")
@Getter @Setter @NoArgsConstructor
public class Stadium {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "stadium_name", nullable = false)
    private String stadiumName;

    @Column(nullable = false)
    private String city;

    @Column(nullable = false)
    private String country;
}

package com.stadiumsense.ai.repository;

import com.stadiumsense.ai.model.Location;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LocationRepository extends JpaRepository<Location, Long> {

    @Query("SELECT l FROM Location l WHERE LOWER(l.locationName) LIKE LOWER(CONCAT('%', :keyword, '%')) " +
           "OR LOWER(l.category) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<Location> findByKeyword(@Param("keyword") String keyword);
}

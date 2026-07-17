package com.stadiumsense.ai.repository;

import com.stadiumsense.ai.model.Faq;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FaqRepository extends JpaRepository<Faq, Long> {

    @Query("SELECT f FROM Faq f WHERE LOWER(f.question) LIKE LOWER(CONCAT('%', :keyword, '%')) " +
           "OR LOWER(f.answer) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<Faq> findByKeyword(@Param("keyword") String keyword);
}

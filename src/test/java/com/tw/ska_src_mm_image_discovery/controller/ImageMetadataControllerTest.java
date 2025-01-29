package com.tw.ska_src_mm_image_discovery.controller;

import org.junit.jupiter.api.Test;

import java.util.Objects;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ImageMetadataControllerTest {

    @Test
    void health() {
        ImageMetadataController imageMetadataController = new ImageMetadataController();
        assertEquals("{health=up}", Objects.requireNonNull(imageMetadataController.health().getBody()).toString());
    }

}
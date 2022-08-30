package com.ronoaldo;

import java.util.Arrays;

import org.apache.beam.sdk.expansion.service.ExpansionService;
import org.apache.beam.sdk.transforms.FlatMapElements;
import org.apache.beam.sdk.transforms.PTransform;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.sdk.values.TypeDescriptors;

public class SplitWordsFromJava extends PTransform<PCollection<String>, PCollection<String>> {

    public static SplitWordsFromJava create() {
        return new SplitWordsFromJava();
    }

    @Override
    public PCollection<String> expand(PCollection<String> input) {
        return input.apply(FlatMapElements.into(TypeDescriptors.strings())
                .via((String line) -> Arrays.asList(line.split("[^\\p{L}]+"))));
    }

    // Bundle the Java expansion server.
    public static void main(String[] args) throws Exception {
        ExpansionService.main(args);
    }
}

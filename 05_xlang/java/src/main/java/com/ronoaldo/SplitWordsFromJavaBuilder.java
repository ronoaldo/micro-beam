package com.ronoaldo;

import org.apache.beam.sdk.transforms.ExternalTransformBuilder;
import org.apache.beam.sdk.transforms.PTransform;
import org.apache.beam.sdk.values.PCollection;

import com.ronoaldo.SplitWordsFromJavaRegistrar.Configuration;

public class SplitWordsFromJavaBuilder implements ExternalTransformBuilder<Configuration, PCollection<String>, PCollection<String>> {

    @Override
    public PTransform<PCollection<String>, PCollection<String>> buildExternal(Configuration configuration) {
        return new SplitWordsFromJava();
    }
}

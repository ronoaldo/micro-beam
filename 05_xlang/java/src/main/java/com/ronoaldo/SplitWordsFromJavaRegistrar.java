package com.ronoaldo;

import java.util.Map;

import org.apache.beam.sdk.expansion.ExternalTransformRegistrar;
import org.apache.beam.sdk.transforms.ExternalTransformBuilder;
import com.google.common.collect.ImmutableMap;
import com.google.auto.service.AutoService;

@AutoService(ExternalTransformRegistrar.class)
public class SplitWordsFromJavaRegistrar implements ExternalTransformRegistrar {

    static final String URN = "beam:transform:ronoaldo:split_java:v1";

    @Override
    public Map<String, ExternalTransformBuilder<?, ?, ?>> knownBuilderInstances() {
        return ImmutableMap.of(URN, new SplitWordsFromJavaBuilder());
    }

    public static class Configuration {}
}

package com.ronoaldo;

import java.util.Comparator;
import java.util.List;

import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.Description;
import org.apache.beam.sdk.options.Default;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.Count;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.transforms.Top;
import org.apache.beam.sdk.values.KV;
import org.apache.beam.sdk.values.TypeDescriptors;

class CompareCounts implements Comparator<KV<String, Long>>, java.io.Serializable {
    public int compare(KV<String, Long> a, KV<String, Long> b) {
        return a.getValue().compareTo(b.getValue());
    }
}

public class WordCountPipeline {

    public interface Opts extends PipelineOptions {
        @Description("Output to write the results to")
        @Default.String("data/out/counted-from-java")
        String getOutput();
        void setOutput(String file);
    }

    public static void main(String[] args) {
        Opts options = PipelineOptionsFactory.fromArgs(args).withValidation().as(Opts.class);
        Pipeline p = Pipeline.create(options);

        p.apply(TextIO.read().from("gs://dataflow-samples/shakespeare/kinglear.txt"))
                .apply(new SplitWordsFromJava())
                .apply(Count.perElement())
                .apply(Top.of(5, new CompareCounts()).withoutDefaults())
                .apply(MapElements.into(TypeDescriptors.strings())
                        .via((List<KV<String, Long>> wordCounts) -> listToString(wordCounts)))
                .apply(TextIO.write().to(options.getOutput()));

        p.run().waitUntilFinish();
    }

    private static String listToString(List<KV<String, Long>> list) {
        StringBuilder sb = new StringBuilder();
        list.forEach(e -> sb.append(e.getKey() + ": " + e.getValue() + "\n"));
        return sb.toString();
    }

}

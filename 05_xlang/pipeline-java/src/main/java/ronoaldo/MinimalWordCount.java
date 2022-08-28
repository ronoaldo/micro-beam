package ronoaldo;

import java.util.Arrays;
import java.util.List;
import java.util.Comparator;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.Count;
import org.apache.beam.sdk.transforms.Filter;
import org.apache.beam.sdk.transforms.FlatMapElements;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.transforms.Top;
import org.apache.beam.sdk.transforms.SerializableComparator;
import org.apache.beam.sdk.values.KV;
import org.apache.beam.sdk.values.TypeDescriptors;
import org.apache.beam.sdk.values.PCollection;

class CompareCounts implements Comparator<KV<String,Long>>, java.io.Serializable {
    public int compare(KV<String,Long> a, KV<String,Long> b) {
      return a.getValue().compareTo(b.getValue());
    }
}

public class MinimalWordCount {

  public static void main(String[] args) {
    PipelineOptions options = PipelineOptionsFactory.create();
    Pipeline p = Pipeline.create(options);

    p.apply(TextIO.read().from("gs://dataflow-samples/shakespeare/kinglear.txt"))
      .apply(FlatMapElements.into(TypeDescriptors.strings())
                .via((String line) -> Arrays.asList(line.split("[^\\p{L}]+"))))
      .apply(Filter.by((String word) -> !word.isEmpty()))
      .apply(Count.perElement())
      .apply(Top.of(5, new CompareCounts()).withoutDefaults())
      .apply(MapElements.into(TypeDescriptors.strings())
                .via((List<KV<String, Long>> wordCounts) -> listToString(wordCounts)))
      .apply(TextIO.write().to("data/out/counted-from-java"));

    p.run().waitUntilFinish();
  }

  private static String listToString(List<KV<String, Long>> list) {
    StringBuilder sb = new StringBuilder();
    list.forEach(e -> sb.append(e.getKey() + ": " + e.getValue() + "\n"));
    return sb.toString();
  }

}

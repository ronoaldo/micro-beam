package main

import (
	"context"
	"flag"
	"fmt"
	"reflect"
	"regexp"
	"strings"

	"github.com/apache/beam/sdks/v2/go/pkg/beam"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/core/typex"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/core/util/reflectx"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/io/textio"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/log"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/transforms/stats"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/transforms/top"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/x/beamx"
)

var (
	// Input to load data from
	file = "gs://dataflow-samples/shakespeare/kinglear.txt"

	// Output to write into
	output string

	// Word split regular expression
	wordRE = regexp.MustCompile(`[a-zA-Z]+('[a-z])?`)

	// Expansion server for Python
	pythonExpansionAddr string

	// Expansion server for Java
	javaExpansionAddr string
)

func SplitWordsFromGoFn(line string, emit func(string)) {
	words := wordRE.FindAllString(line, -1)
	for _, w := range words {
		emit(strings.TrimSpace(w))
	}
}

func FormatCountsFn(top []CountedWord, emit func(string)) {
	for _, e := range top {
		emit(fmt.Sprintf("%s: %v", e.Word, e.Count))
	}
}

func mapkeys(m map[string]beam.PCollection) (keys []string) {
	for k, _ := range m {
		keys = append(keys, k)
	}
	return
}

func SplitTransform(ctx context.Context, s beam.Scope, lines beam.PCollection) beam.PCollection {
	if pythonExpansionAddr != "" {
		log.Infof(ctx, "Using external transform SplitWordsFromPython at %v", pythonExpansionAddr)
		s = s.Scope("xlang.split")

		// Wire up the external tranform
		urn := "beam:transform:ronoaldo:split_python:v1"
		// Call xlang using the provided expansion service
		input := beam.UnnamedInput(lines)
		outType := beam.UnnamedOutput(typex.New(reflectx.String))
		output := beam.CrossLanguage(s,
			urn,
			nil,
			pythonExpansionAddr,
			input,
			outType)
		return output[beam.UnnamedOutputTag()]
	} else if javaExpansionAddr != "" {
		log.Infof(ctx, "Using external transform SplitWordsFromJava at %v", javaExpansionAddr)
		s = s.Scope("xlang.split")

		// Wire up the external tranform
		urn := "beam:transform:ronoaldo:split_java:v1"
		// Call xlang using the provided expansion service
		input := beam.UnnamedInput(lines)
		outType := beam.UnnamedOutput(typex.New(reflectx.String))
		output := beam.CrossLanguage(s,
			urn,
			nil,
			javaExpansionAddr,
			input,
			outType)
		return output[beam.UnnamedOutputTag()]
	}

	log.Infof(ctx, "Using Go native SplitWordsFromGoFn")
	return beam.ParDo(s, SplitWordsFromGoFn, lines)
}

type CountedWord struct {
	Word  string
	Count int
}

func ToStruct(w string, c int) CountedWord {
	return CountedWord{w, c}
}

func WordCountComparator(l, r CountedWord) bool {
	return l.Count < r.Count
}
func init() {
	// Register pipeline input/output flags
	flag.StringVar(&pythonExpansionAddr, "python_expansion_addr", "",
		"The expansion server address for Python SDK")
	flag.StringVar(&javaExpansionAddr, "java_expansion_addr", "",
		"The expansion server address for Java SDK")
	flag.StringVar(&output, "output", "data/out/counted-from-go",
		"The output file to write into")

	// Register Type
	beam.RegisterType(reflect.TypeOf((*CountedWord)(nil)).Elem())

	// Register DoFn with Go
	beam.RegisterDoFn(SplitWordsFromGoFn)
	beam.RegisterDoFn(FormatCountsFn)
	beam.RegisterDoFn(ToStruct)

}

func main() {
	ctx := context.Background()
	flag.Parse()
	beam.Init()

	p := beam.NewPipeline()
	s := p.Root()
	lines := textio.Read(s, file)
	words := SplitTransform(ctx, s, lines)
	counts := stats.Count(s, words)
	comparableCount := beam.ParDo(s, ToStruct, counts)
	topFive := top.Largest(s, comparableCount, 5, WordCountComparator)
	formatted := beam.ParDo(s, FormatCountsFn, topFive)
	textio.Write(s, output, formatted)

	if err := beamx.Run(context.Background(), p); err != nil {
		log.Fatalf(ctx, "Failed to execute job: %v", err)
	}
}

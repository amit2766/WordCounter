package threads;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.regex.Pattern;

public class WordsCounter {

    public static void main(String[] args) {
        String filePath = System.getProperty("user.dir")+ "\\src\\threads\\gnu_license.txt";;
        long startTime = System.nanoTime();
        Map<String, Integer> wordOccurrences = countWordOccurrences(filePath, 4);
        wordOccurrences.forEach((word, count) -> System.out.println(word + ":" + count));
        long endTime = System.nanoTime();
        long duration = (endTime - startTime);
        System.out.println("Total time taken: "+ duration);
    }

    public static Map<String, Integer> countWordOccurrences(String filePath, int numThreads) {
        ConcurrentHashMap<String, Integer> wordCount = new ConcurrentHashMap<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {

            String line;
            ExecutorService executorService = Executors.newFixedThreadPool(numThreads);
            while ((line = reader.readLine()) != null) {
                executorService.execute(new WordCountTask(line, wordCount));
            }

            executorService.shutdown();
            executorService.awaitTermination(1, TimeUnit.MINUTES);
        } catch (IOException e) {
            System.out.println("An error occurred while reading the file.");
        } catch (InterruptedException e) {
            System.out.println("Thread execution was interrupted.");
        }

        return wordCount;
    }

    static class WordCountTask implements Runnable {
        private final String contents;
        private final Map<String, Integer> wordCount;

        public WordCountTask(String contents,  Map<String, Integer> wordCount) {
            this.contents = contents;
            this.wordCount = wordCount;
        }

        @Override
        public void run() {
            String[] words = Pattern.compile("\\W+").splitAsStream(contents.toLowerCase())
                    .filter(word -> !word.isEmpty())
                    .toArray(String[]::new);
            for (int i = 0; i < words.length; i++) {
                wordCount.compute(words[i], (key, value) -> (value == null) ? 1 : value + 1);
            }
        }
    }
}

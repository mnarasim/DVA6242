package edu.gatech.cse6242;
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4 {
  public static class TokenizerMapper
         extends Mapper<Object, Text, IntWritable, IntWritable>{
      private final static IntWritable degree = new IntWritable();
      private IntWritable node = new IntWritable();
      public void map(Object key, Text value, Context context
                      ) throws IOException, InterruptedException {
        StringTokenizer itr = new StringTokenizer(value.toString());
        while (itr.hasMoreTokens()) {
          //itr.nextToken();
          node.set(Integer.parseInt(itr.nextToken()));
          degree.set(1);
          context.write(node,degree);
          node.set(Integer.parseInt(itr.nextToken()));
          degree.set(-1);
          context.write(node,degree);
      }

      }
    }

    public static class IntSumReducer
         extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
      private IntWritable result = new IntWritable();

      public void reduce(IntWritable key, Iterable<IntWritable> values,
                         Context context
                         ) throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable val : values) {
          sum += val.get();
        }
        result.set(sum);
        context.write(key, result);
      }
    }
    public static class TokenizerMapper2
           extends Mapper<Object, Text, IntWritable, IntWritable>{
        private final static IntWritable count = new IntWritable();
        private IntWritable diff = new IntWritable();
        public void map(Object key, Text value, Context context
                        ) throws IOException, InterruptedException {
          StringTokenizer itr = new StringTokenizer(value.toString());
          while (itr.hasMoreTokens()) {
            itr.nextToken();
            diff.set(Integer.parseInt(itr.nextToken()));
            count.set(1);
	    //System.out.println(diff);
	    //System.out.println(count);
            context.write(diff,count);
        }

        }
      }

      public static class IntSumReducer2
           extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(IntWritable key, Iterable<IntWritable> values,
                           Context context
                           ) throws IOException, InterruptedException {
          int sum = 0;
          for (IntWritable val : values) {
            sum += val.get();
          }
          result.set(sum);
          context.write(key, result);
        }
      }
  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q4");
    job.setJarByClass(Q4.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);
    
    Path temp_out = new Path("./data/temp");
    FileSystem hdfs = FileSystem.get(conf);
    if (hdfs.exists(temp_out)) {
    	hdfs.delete(temp_out, true);
    }

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path("./data/temp"));
    job.waitForCompletion(true);

    Configuration conf2 = new Configuration();
    Job job2 = Job.getInstance(conf2, "Q4");
    job2.setJarByClass(Q4.class);
    job2.setMapperClass(TokenizerMapper2.class);
    job2.setCombinerClass(IntSumReducer2.class);
    job2.setReducerClass(IntSumReducer2.class);
    job2.setOutputKeyClass(IntWritable.class);
    job2.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job2, new Path("./data/temp"));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));

    System.exit(job2.waitForCompletion(true) ? 0 : 1);
  }
}

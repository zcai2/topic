import cc.mallet.util.*;
import cc.mallet.types.*;
import cc.mallet.pipe.*;
import cc.mallet.pipe.iterator.*;
import cc.mallet.topics.*;

 
import java.util.*;
import java.util.regex.*;
import java.io.*;
import java.nio.file.*;
import java.net.*;

import java.sql.*;


public class Modeling
{
    private static int iterations = 100;
    private static int numTopics = 10;
    private static int numThreads = 4;
    private static double alpha_t = 1.0;
    private static double beta_w = .01;
    private static int numRuns = 1;
    
    private static Connection c = null;
    private static Statement statement = null;
        
    private static Path path_contents = null;
    private static Path path_descript = null;
    private static Path database_path = Paths.get("../database");
    private static InstanceList instances_contents = null;
    private static InstanceList instances_descript = null;
    
    
    public static void main(String args[]) throws IOException , SQLException
    {

    	// Sets all the path variables
    	System.out.println("Setting all the path variables");
    	
		path_contents= Paths.get("Datastore/Contents/files/");
		path_descript = Paths.get("Datastore/Descript/files/");
		
		File contents_dir = new File(path_contents.toString());
		File descript_dir = new File(path_descript.toString());
		
		boolean writeFiles = false;
		if(!contents_dir.exists())
		{
			contents_dir.mkdirs();
			writeFiles = true;
		}
    	if(!descript_dir.exists())
    	{
			descript_dir.mkdirs();
			writeFiles = true;
		}
		
		
		if(args.length > 0)
		{
			System.out.println("Setting the variables");
			alpha_t = Double.parseDouble(args[0]);
			beta_w = Double.parseDouble(args[1]);
			numTopics = Integer.parseInt(args[2]);
			iterations = Integer.parseInt(args[3]);
		}
    	// Connects to database
    	System.out.println("Connecting to the database");
    	try
    	{
    		Class.forName("org.sqlite.JDBC");
    	    c = DriverManager.getConnection("jdbc:sqlite:" + database_path.toString());
    		c.setAutoCommit(false);    	    
    	} catch(Exception e)
    	{
    		System.err.println(e.getClass().getName() + " : " + e.getMessage() );
    		System.exit(0);	
    	}
    	
    	if(writeFiles)
    	{
		    System.out.println("Porting the database to files");
			writeToFiles();
		}
		else
		{
			System.out.println("Proceeding with previous data");
		}
		
		System.out.println("------------------------------");
    	System.out.println("Database connected successfully");
		System.out.println("Starting the modeling");
		
    	runProgram(alpha_t, beta_w, numTopics);	
   	
        System.out.println("Program ended successfully");
    	c.commit();
    	c.close();
    }
    
    
    public static void runProgram(double alpha_t , double beta_w , int numTopics) throws IOException , SQLException
    {
    	    	
    	String base_dir = new File(".").getCanonicalPath();
    	
 	
        System.out.println("Building the pipe");
        Pipe pipe = pipeBuilder();
        
        System.out.println("The pipe has been successfully built");
        
        System.out.println("Now gathering files");
        FileIterator fileIterator_contents = iteratorBuilder(path_contents.toString());
        FileIterator fileIterator_descript = iteratorBuilder(path_descript.toString());
        
        System.out.println("Files have been gathered successfully");
    
        System.out.println("Now creating the models");
        System.out.print("The table of contents : ");
        ParallelTopicModel model_contents = modelBuilder(pipe, fileIterator_contents , alpha_t , beta_w , numTopics);
        System.out.print("The description : " );
        ParallelTopicModel model_descript = modelBuilder(pipe , fileIterator_descript , alpha_t , beta_w , numTopics);
        
        instances_contents.addThruPipe(fileIterator_contents);
        model_contents.addInstances(instances_contents);
        
        instances_descript.addThruPipe(fileIterator_descript);
        model_descript.addInstances(instances_descript);
        
        System.out.println("Models successfully created");
        System.out.println("Training Models");
        
        System.out.println("Starting with Table of Contents first");
        System.out.println("----------");
        model_contents.estimate();
        
        System.out.println("Model successfully trained");        
        try
        {
            saveResults(model_contents,instances_contents , "toc_book_topics" , .1 , path_contents.toString() , numTopics );
        }
        catch (FileNotFoundException e)
        {
        	System.out.println("Could not output to the file, closing all");
        	System.exit(1);
        }
		
        System.out.println("Continuing on Description of the books");
        System.out.println("----------");
        model_descript.estimate();
        
        System.out.println("Model successfully trained");
        System.out.println("Writing to files results now");
        try
        {
            saveResults(model_descript,instances_descript , "descript_book_topics" , .1 , path_descript.toString(), numTopics);
        }
        catch (FileNotFoundException e)
        {
        	System.out.println("Could not output to the file, closing all");
        	System.exit(1);
        }
    }
    
    private static void writeToFiles() throws SQLException , FileNotFoundException
    {
		System.out.println("Starting with the descriptions");
		statement = c.createStatement();
        ResultSet rs = statement.executeQuery("select * from book_info;");
        while(rs.next())
        {
			if(rs.getString("descript_raw")!= null && !rs.getString("descript_raw").equals("Description Not Found"))
			{
				PrintWriter writer = new PrintWriter(path_descript.toString() + "/" + rs.getString("isbn") + ".txt");
				writer.println(rs.getString("descript_raw"));
				writer.close();
			}
			
			if(rs.getString("toc_raw")!= null && !rs.getString("toc_raw").equals("Table Not Found"))
			{
				PrintWriter writer = new PrintWriter(path_contents.toString() + "/" + rs.getString("isbn") + ".txt");
				writer.println(rs.getString("toc_raw"));
				writer.close();
			}
			
		}
		
	}
    
    private static Pipe pipeBuilder()
    {
        // Creates the pipe
    	ArrayList<Pipe> pipeList = new ArrayList<Pipe>();
        pipeList.add( new Input2CharSequence("UTF-8") );
        pipeList.add( new CharSequence2TokenSequence(Pattern.compile("\\p{L}[\\p{L}\\p{P}]+\\p{L}")) );
        pipeList.add( new TokenSequenceLowercase() );
        pipeList.add( new TokenSequenceRemoveStopwords() );
        pipeList.add( new TokenSequence2FeatureSequence() );
        
        SerialPipes pipe = new SerialPipes(pipeList);
        instances_contents = new InstanceList(pipe);
        instances_descript = new InstanceList(pipe);
       
        return pipe;
    }
    
    private static FileIterator iteratorBuilder(String path)
    {
    	File dir = new File(path);
        return new FileIterator(dir);
    }
    
    
    private static ParallelTopicModel modelBuilder(Pipe pipe, FileIterator fileIterator , double alpha , double beta, int numTopics)
    {
        ParallelTopicModel model = new ParallelTopicModel(numTopics,alpha,beta);
        model.setNumThreads(numThreads);
        model.setNumIterations(iterations);
        return model;
         
    }
    
    private static void saveResults(ParallelTopicModel model , InstanceList instances , String table , double margin, String files_path , int topics) 
    		throws FileNotFoundException , SQLException
    {
    	int counter = 1;
        Alphabet dataAlphabet = instances.getDataAlphabet();
        System.out.println("Saving results to " + table);
        for(int doc = 0; doc < model.getData().size(); doc ++)
        {
        	String isbn = getBookIsbn((URI)instances.get(doc).getName() , files_path);
        	
        	PreparedStatement statement2 = c.prepareStatement("select * from book_info where isbn = ?");
        	statement2.setString(1 , isbn);
        	String title = statement2.executeQuery().getString("title");
        	int id = statement2.executeQuery().getInt("id");
        	
        	Formatter topic_words = new Formatter(new StringBuilder() , Locale.US);
        	double[] topicDistribution = model.getTopicProbabilities(doc);
        	ArrayList<TreeSet<IDSorter>> topicSortedWords = model.getSortedWords();
        	
            // Show top 5 words in topics with proportions for the first document
            int rank = 0;
            for (int topic = 0; topic < topics; topic++) 
            {
            	Iterator<IDSorter> iterator = topicSortedWords.get(topic).iterator();
            	if(topicDistribution[topic] < margin )
            	{
            		continue;
            	}
    			while (iterator.hasNext() && rank < 5) 
    			{
    				IDSorter idCountPair = iterator.next();
    			 	topic_words.format("%s ", dataAlphabet.lookupObject(idCountPair.getID()));
    			 	rank++;
    			}
    			
    			String sql = "INSERT INTO " + table + "(id,title,isbn,topic_id,topic_distribution,topic_words) " +
    		            "VALUES (" + id + ",\"" + title + "\",\"" + isbn + "\",\"" + topic + "\",\"" + topicDistribution[topic] + "\",\"" + topic_words + "\");";
    			
    			statement = c.createStatement();
    			statement.executeUpdate(sql);
    			
    			// Adding to the descript or toc topic tables
				String source_info = table.split("_")[0];
    			statement2 = c.prepareStatement("SELECT COUNT(*) as total from " + source_info + "_topics where id = ?");
    			statement2.setString(1 , Integer.toString(topic));
    			int number_topics = statement2.executeQuery().getInt("total");
				
				if (number_topics == 0)
				{
					sql = "Insert into " + source_info + "_topics (id, topic_words , book_count) values (\"" + topic + "\",\"" + topic_words + "\", \"1\");";
					statement.executeUpdate(sql);
				}
				
				else
				{
					statement2 = c.prepareStatement("select * from " + source_info + "_topics where id = ?");
					statement2.setString(1 , Integer.toString(topic));
					int number_books = statement2.executeQuery().getInt("book_count");
					sql = "update "+ source_info +"_topics set book_count = " + ++number_books + " where id = \"" + topic + "\"";
					statement.executeUpdate(sql);
				}
    			
    			counter++;
                
            }
            
          }
    }
      	
    private static String getBookIsbn(URI filePath , String path)
    {
    	String bookIsbn = "";
    	Path paths = Paths.get(filePath);
    	bookIsbn = paths.getFileName().toString().replace(".txt" , "");
    	return bookIsbn;
    }
    
}

        

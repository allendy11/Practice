import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field.Store;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

public class NCBIIndexer {
	private String output_path;
	private String input_path;
	
	private Directory index;
	private StandardAnalyzer analyzer;
	private IndexWriterConfig iwc;
	private IndexWriter iw;
	private IndexReader ir;
	private BufferedReader reader;
	private Query query;

	public static void main(String[] args) {
		String input_path = "/home/neuroears/Java_NCBIIndexer/taxdmp/names.dmp";
		String output_path = "/home/neuroears/Java_NCBIIndexer/output";
		
		NCBIIndexer indexer = new NCBIIndexer();
		
		indexer.set_input_path(input_path);
		indexer.set_output_path(output_path);
		
		indexer.loader();
		
		
		indexer.parse();
		String word = "Buchnera Aphidicola Tabriz.1";
		NCBITerm searchResult = indexer.searcher(word);
		System.out.println("DocID: " + searchResult.docId);
		System.out.println("TaxID: " + searchResult.taxId);
		System.out.println("TaxDetail: " + searchResult.taxDetail);
		
		indexer.closer();
		
	}

	private NCBITerm searcher(String word) {
		try {
			int hitsPerPage = 10;
			query = new QueryParser("TaxDetail", analyzer).parse(word);
			IndexSearcher searcher = new IndexSearcher(ir);
			TopDocs topDocs = searcher.search(query, hitsPerPage);
			ScoreDoc[] hits = topDocs.scoreDocs;
			
			for(ScoreDoc hit : hits) {
				int docId = hit.doc;
				Document doc = searcher.doc(docId);
				return new NCBITerm(docId, doc.get("TaxID"), doc.get("TaxDetail"));
			}
		} catch (ParseException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return new NCBITerm(-1, "", "");
	}

	private void closer() {
		try {
			if(this.iw != null) {
				this.iw.close();				
			}
			if(this.ir != null) {
				this.ir.close();				
			}
			if(this.reader != null) {
				this.reader.close();
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}



	private void loader() {
		try {
			this.index = FSDirectory.open(Paths.get(output_path));
			this.analyzer = new StandardAnalyzer();
			this.iwc = new IndexWriterConfig(analyzer);
			this.iw = new IndexWriter(index, iwc);
			this.ir = DirectoryReader.open(index);
			this.reader = new BufferedReader(new FileReader(input_path));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
	}

	private void parse() {
		File file = new File(output_path);
		File[] files = file.listFiles();
		if(files.length > 2) return;
		try {
			String str;
			while((str = reader.readLine()) != null) {
				if(!str.contains("scientific name")) continue;
				
				ArrayList<String> list = new ArrayList<>();
				String[] arr = str.split("\\|");
				for(int i = 0 ; i < arr.length ; i++) {
					list.add(arr[i].trim());
				}
				String taxId = list.get(0);
				String taxDetail = list.get(1);
				String taxDetail_2 = list.get(2);
				
				if(taxDetail_2.length() > 0) {
					taxDetail += " " + taxDetail_2;
				}
				
				addDoc(iw, taxId, taxDetail);

				
			}
			reader.close();
			
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private void addDoc(IndexWriter writer, String taxId, String taxDetail) throws IOException {
		Document doc = new Document();
		doc.add(new StringField("TaxID", taxId, Store.YES));
		doc.add(new TextField("TaxDetail", taxDetail, Store.YES));
		
		writer.addDocument(doc);
	}



	private void set_output_path(String output_path) {
		this.output_path = output_path;
	}

	private void set_input_path(String input_path) {
		this.input_path = input_path;
	}

}

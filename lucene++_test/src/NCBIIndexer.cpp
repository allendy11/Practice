/*
 * NCBIIndexer.cpp
 *
 *  Created on: Sep 6, 2022
 *      Author: allen
 */

#include "NCBIIndexer.hpp"

NCBIIndexer::NCBIIndexer()
{
  // TODO Auto-generated constructor stub
}

NCBIIndexer::~NCBIIndexer()
{
  // TODO Auto-generated destructor stub
}

void NCBIIndexer::set_input_path(String input_path)
{
  this->input_path = input_path;
}
void NCBIIndexer::set_index_directory(String output_directory_index)
{
  this->output_directory_index = output_directory_index;
}

void NCBIIndexer::parse()
{
  HashSet<String> dirList(HashSet<String>::newInstance());
  FileUtils::listDirectory(output_directory_index, true, dirList);
  if (dirList.size() > 0)
  {
    cout << "Parsing already" << endl;
    return;
  }
  int64_t start = MiscUtils::currentTimeMillis();

  IndexWriterPtr writer = newLucene<IndexWriter>(
      FSDirectory::open(output_directory_index),
      newLucene<StandardAnalyzer>(LuceneVersion::LUCENE_CURRENT), true,
      IndexWriter::MaxFieldLengthLIMITED);

  boost::filesystem::fstream data;
  data.open(input_path, ios::in);
  string line;

  while (getline(data, line))
  {
    if (line.find("scientific name") == string::npos)
    {
      continue;
    }
    vector<string> list;
    boost::split(list, line, boost::is_any_of("\\|"));

    for (long unsigned int i = 0; i < list.size(); i++)
    {
      boost::trim(list[i]);
    }
    string taxId_str = list[0];
    string taxDetail_str = list[1];
    string subTaxDetail_str = list[2];

    if (!subTaxDetail_str.empty())
    {
      taxDetail_str += " " + subTaxDetail_str;
    }
    String taxId = StringUtils::toUnicode(taxId_str);
    String taxDetail = StringUtils::toUnicode(taxDetail_str);

    writer->addDocument(fileDocument(taxId, taxDetail));
  }
  //	writer->optimize();
  writer->close();
  int64_t time = (MiscUtils::currentTimeMillis() - start) / 1000;
  int64_t min = time / 60;
  int64_t sec = time % 60;
  cout << "Parsing finised" << endl;
  wcout << L"Time: " << min << L"m " << sec << L"s\n";
}

DocumentPtr NCBIIndexer::fileDocument(String taxId, String taxDetail)
{
  DocumentPtr doc = newLucene<Document>();
  doc->add(
      newLucene<Field>(L"TaxID", taxId, Field::STORE_YES,
                       Field::INDEX_ANALYZED));
  doc->add(
      newLucene<Field>(L"TaxDetail", taxDetail, Field::STORE_YES,
                       Field::INDEX_ANALYZED));
  return doc;
}
String NCBIIndexer::search(String species)
{
  String result_taxId = L"-1";
  int32_t hitsPerPage = 10;
  try
  {
    IndexReaderPtr reader = IndexReader::open(
        FSDirectory::open(output_directory_index), true);
    SearcherPtr searcher = newLucene<IndexSearcher>(reader);
    AnalyzerPtr analyzer = newLucene<StandardAnalyzer>(
        LuceneVersion::LUCENE_CURRENT);
    QueryParserPtr parser = newLucene<QueryParser>(
        LuceneVersion::LUCENE_CURRENT, L"TaxDetail", analyzer);

    boost::trim(species);
    QueryPtr query = parser->parse(species);
    wcout << L"Searching for: " << query->toString(L"TaxDetail") << L"\n";

    TopScoreDocCollectorPtr collector = TopScoreDocCollector::create(
        5 * hitsPerPage, false);
    searcher->search(query, collector);
    Collection<ScoreDocPtr> hits = collector->topDocs()->scoreDocs;

    int32_t numTotalHits = collector->getTotalHits();

    if (numTotalHits > 0)
    {
      wcout << numTotalHits << L" total matching documents\n";

      for (int i = 0; i < hitsPerPage; i++)
      {
        int docId = hits[i]->doc;
        DocumentPtr doc = searcher->doc(docId);
        String taxId = doc->get(L"TaxID");
        String taxDetail = doc->get(L"TaxDetail");

        wcout << L"docId: " << docId << endl;
        wcout << L"taxId: " << taxId << endl;
        wcout << L"taxDetail: " << taxDetail << endl;
        result_taxId = taxId;
        break;
      }
    }
    else
    {
      wcout << L"Not Found: " << species << endl;
    }
    reader->close();
  }
  catch (LuceneException &e)
  {
    wcout << L"Eception: " << e.getError() << L"\n";
  }
  return result_taxId;
}
void NCBIIndexer::add_custom_species(String species)
{
  // change format species for exact match
  string exact_species_str = "\"" + StringUtils::toUTF8(species) + "\"";
  String exact_species_unicode = StringUtils::toUnicode(exact_species_str);
  try
  {
    String tax_id = NCBIIndexer::search(exact_species_unicode);
    //		wcout << StringUtils::toInt(tax_id) << L"\n";
    // already exist
    if (StringUtils::toInt(tax_id) != -1)
    {
      wcout << L"Exist already: " << species << L"\n";
      return;
    }
    wcout << L"Add start: " << species << endl;

    IndexWriterPtr writer = newLucene<IndexWriter>(
        FSDirectory::open(output_directory_index),
        newLucene<StandardAnalyzer>(LuceneVersion::LUCENE_CURRENT),
        true, IndexWriter::MaxFieldLengthLIMITED);
    IndexReaderPtr reader = IndexReader::open(
        FSDirectory::open(output_directory_index), true);

    int32_t maxDocId = reader->maxDoc() - 1;
    String maxTaxId = reader->document(maxDocId)->get(L"TaxID");
    int32_t newTaxId_int = StringUtils::toInt(maxTaxId) + 1;
    String newTaxId = StringUtils::toUnicode(to_string(newTaxId_int));

    writer->addDocument(NCBIIndexer::fileDocument(newTaxId, species));

    writer->close();
    reader->close();
    wcout << L"add complete" << endl;
    wcout << L"newDocId: " << maxDocId + 1 << endl;
    wcout << L"newTaxId: " << newTaxId << endl;
    wcout << L"newTaxDetail: " << species << endl;
  }
  catch (LuceneException &e)
  {
    wcout << L"Eception: " << e.getError() << L"\n";
  }
  return;
}
void NCBIIndexer::getMaxDoc()
{
  IndexReaderPtr reader = IndexReader::open(
      FSDirectory::open(output_directory_index), true);
  int32_t maxDocId = reader->maxDoc() - 1;
  if (maxDocId == -1)
  {
    cout << "No data" << endl;
  }
  String taxId = reader->document(maxDocId)->get(L"TaxID");
  String taxDetail = reader->document(maxDocId)->get(L"TaxDetail");

  wcout << L"maxDocId: " << maxDocId << endl;
  wcout << L"maxTaxId: " << taxId << endl;
  wcout << L"maxTaxDetail: " << taxDetail << endl;

  reader->close();
  return;
}

void NCBIIndexer::delete_custom_species(String species)
{
  String s = StringUtils::toUnicode(
      "\"" + StringUtils::toUTF8(species) + "\"");
  String tax_id = NCBIIndexer::search(species);
  if (StringUtils::toInt(tax_id) == -1)
  {
    wcout << L"Not found" << endl;
    return;
  }
  try
  {
    IndexWriterPtr writer = newLucene<IndexWriter>(
        FSDirectory::open(output_directory_index),
        newLucene<StandardAnalyzer>(LuceneVersion::LUCENE_CURRENT),
        true, IndexWriter::MaxFieldLengthLIMITED);
    IndexReaderPtr reader = IndexReader::open(
        FSDirectory::open(output_directory_index), true);
    SearcherPtr searcher = newLucene<IndexSearcher>(reader);
    AnalyzerPtr analyzer = newLucene<StandardAnalyzer>(
        LuceneVersion::LUCENE_CURRENT);
    QueryParserPtr parser = newLucene<QueryParser>(
        LuceneVersion::LUCENE_CURRENT, L"TaxDetail", analyzer);

    boost::trim(species);
    QueryPtr query = parser->parse(species);
    writer->deleteDocuments(query);
    writer->commit();
    writer->close();
    reader->close();
    wcout << "Delete complete: " << species << endl;
    return;
  }
  catch (LuceneException &e)
  {
    wcout << L"Eception: " << e.getError() << L"\n";
  }
}

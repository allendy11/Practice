/*
 * NCBIIndexer.cpp
 *
 *  Created on: Sep 20, 2022
 *      Author: neuroears
 */

#include "NCBIIndexer.hpp"

using namespace std;
using namespace Lucene;

NCBIIndexer::NCBIIndexer()
{
  // TODO Auto-generated constructor stub
}

NCBIIndexer::~NCBIIndexer()
{
  // TODO Auto-generated destructor stub
}
void NCBIIndexer::set_input_path(String path)
{
  this->input_path = path;
}
void NCBIIndexer::set_index_directory(String path)
{
  this->output_directory_index = path;
}
void NCBIIndexer::parse()
{
  HashSet<String> dirList(HashSet<String>::newInstance());
  FileUtils::listDirectory(output_directory_index, true, dirList);
  if (dirList.size() > 5)
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
    vector<string> arr;
    boost::split(arr, line, boost::is_any_of("\\|"));

    for (long unsigned int i = 0; i < arr.size(); i++)
    {
      boost::trim(arr[i]);
    }

    string taxId_str = arr[0];
    string taxDetail_str = arr[1];
    string subTaxDetail_str = arr[2];

    if (!subTaxDetail_str.empty())
    {
      taxDetail_str += " " + subTaxDetail_str;
    }
    //		cout << taxId << " " << taxDetail << endl;
    String taxId = StringUtils::toUnicode(taxId_str);
    String taxDetail = StringUtils::toUnicode(taxDetail_str);

    writer->addDocument(NCBIIndexer::fileDocument(taxId, taxDetail));
  }
  writer->close();
  int64_t time = (MiscUtils::currentTimeMillis() - start) / 1000;
  int64_t min = time / 60;
  int64_t sec = time % 60;
  wcout << L"Time: " << min << L"m" << sec << L" s\n";
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
  int32_t hitsPerPage = 1;
  String field_taxId = L"TaxID";
  String field_taxDetail = L"TaxDetail";
  try
  {
    IndexReaderPtr reader = IndexReader::open(
        FSDirectory::open(output_directory_index), true);
    SearcherPtr searcher = newLucene<IndexSearcher>(reader);
    AnalyzerPtr analyzer = newLucene<StandardAnalyzer>(
        LuceneVersion::LUCENE_CURRENT);
    QueryParserPtr parser = newLucene<QueryParser>(
        LuceneVersion::LUCENE_CURRENT, field_taxDetail, analyzer);

    boost::trim(species);
    QueryPtr query = parser->parse(species);
    wcout << L"Searching for: " << query->toString(field_taxDetail)
          << L"\n";

    TopScoreDocCollectorPtr collector = TopScoreDocCollector::create(
        hitsPerPage, false);
    searcher->search(query, collector);
    Collection<ScoreDocPtr> hits = collector->topDocs()->scoreDocs;
    int32_t numTotalHits = collector->getTotalHits();
    if (numTotalHits > 0)
    {
      wcout << numTotalHits << L" total matching documents\n";
      for (int32_t i = 0; i < hitsPerPage; i++)
      {
        int docId = hits[i]->doc;
        DocumentPtr doc = searcher->doc(docId);
        String taxId = doc->get(field_taxId);
        String taxDetail = doc->get(field_taxDetail);
        wcout << L"docId: " << docId << L"\n";
        wcout << L"taxId: " << taxId << L"\n";
        wcout << L"taxDetail: " << taxDetail << L"\n";
        return taxId;
      }
    }
    else
    {
      wcout << L"Can't matching document : " << species << L"\n";
    }
    reader->close();
  }
  catch (LuceneException &e)
  {
    wcout << L"Eception: " << e.getError() << L"\n";
  }
  return L"-1";
}
void NCBIIndexer::add_custom_species(String species)
{
  // change format species for exact match
  string exact_species_str = "\"" + StringUtils::toUTF8(species) + "\"";
  String exact_species_unicode = StringUtils::toUnicode(exact_species_str);
  String tax_id = NCBIIndexer::search(exact_species_unicode);
  //	wcout << StringUtils::toInt(tax_id) << L"\n";
  // already exist
  if (StringUtils::toInt(tax_id) != -1)
  {
    wcout << L"Exist already: " << species << L"\n";
  }

  IndexWriterPtr writer = newLucene<IndexWriter>(
      FSDirectory::open(output_directory_index),
      newLucene<StandardAnalyzer>(LuceneVersion::LUCENE_CURRENT), true,
      IndexWriter::MaxFieldLengthLIMITED);
  IndexReaderPtr reader = IndexReader::open(
      FSDirectory::open(output_directory_index), true);

  // get newTaxId = maxTaxId +1 (need maxDocId)
  int32_t maxDocId = reader->maxDoc() - 1;
  String maxTaxId = reader->document(maxDocId)->get(L"TaxID");
  writer->addDocument(NCBIIndexer::fileDocument(maxTaxId, species));
}

/*
 * NCBIIndexer.cpp
 *
 *  Created on: Sep 20, 2022
 *      Author: neuroears
 */

#include "NCBIIndexer.hpp"

using namespace Lucene;

NCBIIndexer::NCBIIndexer()
{
  // TODO Auto-generated constructor stub
}

NCBIIndexer::~NCBIIndexer()
{
  // TODO Auto-generated destructor stub
}
void NCBIIndexer::set_input_path(string path)
{
  this->input_path = path;
}
void NCBIIndexer::set_index_directory(string path)
{
  this->output_directory_index = path;
}
void NCBIIndexer::parse()
{
  IndexWriterPtr writer = newLucene<IndexWriter>(
      FSDirectory::open(StringUtils::toUnicode(output_directory_index)),
      newLucene<StandardAnalyzer>(LuceneVersion::LUCENE_CURRENT), true,
      IndexWriter::MaxFieldLengthLIMITED);
  fstream data;
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

    string taxId = arr[0];
    string taxDetail = arr[1];
    string subTaxDetail = arr[2];

    if (!subTaxDetail.empty())
    {
      taxDetail += " " + subTaxDetail;
    }
    //		cout << taxId << " " << taxDetail << endl;

    writer->addDocument(NCBIIndexer::fileDocument(taxId, taxDetail));
  }
  writer->close();
}
DocumentPtr NCBIIndexer::fileDocument(string taxId, string taxDetail)
{
  DocumentPtr doc = newLucene<Document>();
  doc->add(
      newLucene<Field>(L"TaxID", taxId, Field::STORE_YES,
                       Field::INDEX_NOT_ANALYZED));
  doc->add(
      newLucene<Field>(L"TaxDetail", taxDetail, Field::STORE_YES,
                       Field::INDEX_NOT_ANALYZED));
  return doc;
}

string NCBIIndexer::search(String species)
{
  int32_t hitsPerPage = 1;
  String field_taxId = L"TaxID";
  String field_taxDetail = L"TaxDetail";
  try
  {
    IndexReaderPtr reader = IndexReader::open(FSDirectory::open(index),
                                              true);
    SearcherPtr searcher = newLucene<IndexSearcher>(reader);
    AnalyzerPtr analyzer = newLucene<Standardanalyzer>(
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
    wcout << numTotalHits << L" total matching documents\n";

    //		collector = TopScoreDocCollector::create(numTotalhits, false);
    //		searcher->search(query, collector);
    //		hits = collector->topDocs()->scoreDocs;

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
    reader->close();
  }
  catch (LuceneException &e)
  {
    wcout << L"Eception: " << e.getError() << L"\n";
    return "";
  }
}

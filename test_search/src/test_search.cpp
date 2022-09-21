#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif

#ifndef NOMINMAX
#define NOMINMAX
#endif

#include "targetver.h"
#include <iostream>
#include <boost/algorithm/string.hpp>
#include "LuceneHeaders.h"
#include "FilterIndexReader.h"
#include "MiscUtils.h"

using namespace Lucene;
using namespace std;

int main()
{
  string output_path_str = "/home/neuroears/output";
  String output_path = StringUtils::toUnicode(output_path_str);
  String line = L"Buchnera Aphidicola Tabriz.1";
  String field = L"TaxDetail";
  int32_t hitsPerPage = 1;

  try
  {
    IndexReaderPtr reader = IndexReader::open(
        FSDirectory::open(output_path), true);
    SearcherPtr searcher = newLucene<IndexSearcher>(reader);
    AnalyzerPtr analyzer = newLucene<StandardAnalyzer>(
        LuceneVersion::LUCENE_CURRENT);
    QueryParserPtr parser = newLucene<QueryParser>(
        LuceneVersion::LUCENE_CURRENT, field, analyzer);

    boost::trim(line);
    QueryPtr query = parser->parse(line);
    wcout << L"Searching for: " << query->toString(field) << L"\n";

    TopScoreDocCollectorPtr collector = TopScoreDocCollector::create(1,
                                                                     false);
    searcher->search(query, collector);
    Collection<ScoreDocPtr> hits = collector->topDocs()->scoreDocs;
    int32_t numTotalHits = collector->getTotalHits();
    wcout << numTotalHits << L" total matching documents\n";

    collector = TopScoreDocCollector::create(numTotalHits, false);
    searcher->search(query, collector);
    hits = collector->topDocs()->scoreDocs;

    for (int32_t i = 0; i < hitsPerPage; i++)
    {
      wcout << L"doc=" << hits[i]->doc << L" score=" << hits[i]->score
            << L"\n";
      DocumentPtr doc = searcher->doc(hits[i]->doc);
      String taxId = doc->get(L"TaxID");
      String taxDetail = doc->get(L"TaxDetail");

      wcout << L"taxId: " << taxId << L"\n";
      wcout << L"taxDetail: " << taxDetail << L"\n";
    }
    reader->close();
  }
  catch (LuceneException &e)
  {
    wcout << L"Eception: " << e.getError() << L"\n";
    return 1;
  }
  return 0;
}
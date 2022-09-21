//============================================================================
// Name        : test_parse4.cpp
// Author      : Dae-hee Yoon @Neuroears Ltd.
// Version     :
// Copyright   : All rights reserved by Dae-hee Yoon and Neuroears Ltd.
// Description : Hello World in C++, Ansi-style
//============================================================================

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif

#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <iostream>
#include <fstream>
#include <sstream>
#include <regex>

#include "targetver.h"
#include "LuceneHeaders.h"
#include "FileUtils.h"
#include "MiscUtils.h"
#include <boost/algorithm/string.hpp>

#include "Lucene.h"
#include "StringUtils.h"

using namespace Lucene;
using namespace std;

string input_path = "/home/neuroears/taxdmp/names.dmp";
string output_path = "/home/neuroears/output";

int main()
{
  IndexWriterPtr writer = newLucene<IndexWriter>(
      FSDirectory::open(StringUtils::toUnicode(output_path)),
      newLucene<StandardAnalyzer>(LuceneVersion::LUCENE_CURRENT), true,
      IndexWriter::MaxFieldLengthLIMITED);
  fstream data;
  data.open(input_path, ios::in);

  string line;

  int64_t start = MiscUtils::currentTimeMillis();

  while (getline(data, line))
  {
    if (line.find("scientific name") == string::npos)
    {
      continue;
    }
    vector<string> result;
    boost::split(result, line, boost::is_any_of("\\|"));

    for (int32_t i = 0; i < result.size(); i++)
    {
      boost::trim(result[i]);
    }
    string taxId = result[0];
    string taxDetail = result[1];
    string subTaxDetail = result[2];
    if (!subTaxDetail.empty())
    {
      taxDetail += " " + subTaxDetail;
    }

    DocumentPtr doc = newLucene<Document>();
    doc->add(
        newLucene<Field>(L"TaxID", StringUtils::toUnicode(taxId),
                         Field::STORE_YES, Field::INDEX_ANALYZED));
    doc->add(
        newLucene<Field>(L"TaxDetail",
                         StringUtils::toUnicode(taxDetail), Field::STORE_YES,
                         Field::INDEX_ANALYZED));

    writer->addDocument(doc);

    //		string s;
    //		istringstream iss(line);
    //		string arr[4];
    //		int i = 0;

    //		while (getline(iss, s, '|')) {
    ////			s = regex_replace(s, regex("\\s+"), "");
    //			boost::trim(s);
    //			cout << s << endl;
    //
    //
    ////			arr[i++] = s;
    //		}
    //		string taxId = arr[0];
    //		string taxDetail = arr[1];
    //		string subTaxDetail = arr[2];
    //		if (!subTaxDetail.empty()) {
    //			taxDetail += " " + subTaxDetail;
    //		}
    //
    ////		DocumentPtr doc = newLucene<Document>();
    ////		doc->add(
    ////				newLucene<Field>(L"TaxID", StringUtils::toUnicode(taxId),
    ////						Field::STORE_YES, Field::INDEX_NOT_ANALYZED));
    ////		doc->add(
    ////				newLucene<Field>(L"TaxDetail",
    ////						StringUtils::toUnicode(taxDetail), Field::STORE_YES,
    ////						Field::INDEX_NOT_ANALYZED));
    ////
    ////		writer->addDocument(doc);
  }
  writer->close();
  int64_t time_s = (MiscUtils::currentTimeMillis() - start) / 1000;
  int64_t min = time_s / 60;
  int64_t sec = time_s % 60;
  wcout << L"Time: " << min << L"m " << sec << L"s\n";
}

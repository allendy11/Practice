//============================================================================
// Name        : test_fileRead.cpp
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

#include "Lucene.h"
#include "StringUtils.h"

using namespace Lucene;
using namespace std;

string input_path = "/home/neuroears/taxdmp/names.dmp";
string output_path = "/home/neuroears/test_index";
string test_path = "/home/neuroears/test/test.txt";

int main()
{
  IndexWriterPtr writer = newLucene<IndexWriter>(
      FSDirectory::open(StringUtils::toUnicode(output_path)),
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
    string s;
    istringstream iss(line);
    string arr[4];
    int i = 0;
    while (getline(iss, s, '|'))
    {
      s = regex_replace(s, regex("\\s+"), "");
      arr[i++] = s;
    }
    string taxId = arr[0];
    string taxDetail = arr[1];
    string subTaxDetail = arr[2];
    if (!subTaxDetail.empty())
    {
      taxDetail += " " + subTaxDetail;
    }

    DocumentPtr doc = newLucene<Document>();
    doc->add(
        newLucene<Field>(L"TaxID", StringUtils::toUnicode(taxId),
                         Field::STORE_YES, Field::INDEX_NOT_ANALYZED));
    doc->add(
        newLucene<Field>(L"TaxDetail",
                         StringUtils::toUnicode(taxDetail), Field::STORE_YES,
                         Field::INDEX_NOT_ANALYZED));

    writer->addDocument(doc);
  }
}

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
String output_directory_index;
String species = L"Test_Custom_Species_db1"

    int
    main()
{
  try
  {
    DirectoryPtr index = FSDirectory::open(output_directory_index);

    // we don't want read-only because we are about to delete
    IndexReaderPtr reader = IndexReader::open(index, false);

    TermPtr term = newLucene<Term>(L"TaxDetail", species);
    reader->deleteDocument(2438087);
    reader->close();
    index->close();
  }
  catch (LuceneException &e)
  {
    std::wcout << L"Exception: " << e.getError() << L"\n";
    return;
  }
}
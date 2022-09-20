//============================================================================
// Name        : lucene++_test.cpp
// Author      : Dae-hee Yoon @Neuroears Ltd.
// Version     :
// Copyright   : All rights reserved by Dae-hee Yoon and Neuroears Ltd.
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include "NCBIIndexer.hpp"
using namespace std;
using namespace Lucene;

int main()
{
  setlocale(LC_ALL, "utf-8");
  string input_path_str = "/home/neuroears/taxdmp/names.dmp";
  String input_path = StringUtils::toUnicode(input_path_str);

  string output_directory_index_str = "/home/neuroears/output";
  String output_directory_index = StringUtils::toUnicode(
      output_directory_index_str);

  NCBIIndexer indexer;

  indexer.set_input_path(input_path_str);
  indexer.set_index_directory(output_directory_index_str);

  indexer.parse();
}

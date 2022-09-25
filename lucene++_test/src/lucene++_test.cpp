//============================================================================
// Name        : lucene++_test.cpp
// Author      :
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include "NCBIIndexer.hpp"

using namespace std;
using namespace Lucene;

int main()
{
  setlocale(LC_ALL, "utf-8");
  string input_path_str = "/home/allen/Downloads/taxdmp/names.dmp";
  String input_path = StringUtils::toUnicode(input_path_str);

  string output_directory_index_str =
      "/home/allen/eclipse-workspace/lucene/ncbi_index_plus_plus";
  String output_directory_index = StringUtils::toUnicode(
      output_directory_index_str);
  NCBIIndexer indexer;
  indexer.set_input_path(input_path);
  indexer.set_index_directory(output_directory_index);

  //	cout << [Parse];
  //	indexer.parse();
  //	cout << endl;

  //	cout << [Load];
  //	indexer.load();
  //	cout << endl;

  //	cout << [Search];
  String tax_id = indexer.search(L"Buchnera aphidicola Tabriz.1");
  //	String tax_id2 = indexer.search(L"Test_Custom_Species_db2");
  //	cout << endl;

  //	cout << [Add];
  //	indexer.add_custom_species(L"Buchnera aphidicola Tabriz.1");
  //	indexer.add_custom_species(L"Buchnera aphidicola");
  //	indexer.add_custom_species(L"Test_Custom_Species_db1");
  //	cout << endl;

  //	cout << [Delete]
  indexer.delete_custom_species(L"Test_Custom_Species_db1");
  cout << endl;

  //  for test
  //	int32_t docId = indexer.getMaxDoc();
}

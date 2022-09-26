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

  cout << "[Parse]" << endl;
  indexer.parse();
  cout << endl;

  //	cout << "[Load]" << endl;
  //	indexer.load();
  //	cout << endl;

  cout << "[Search]" << endl;
  //	String tax_id = indexer.search(L"Buchnera aphidicola Tabriz.1");
  //	String tax_id2 = indexer.search(L"Test_Custom_Species_db2");
  //	String tax_id = indexer.search(L"Melanina Melanina <ascomycete fungi>");
  cout << endl;

  cout << "[Add]" << endl;
  //	indexer.add_custom_species(L"Buchnera aphidicola Tabriz.1");
  //	indexer.add_custom_species(L"Buchnera aphidicola");
  indexer.add_custom_species(L"Test_Custom_Species_db1");
  indexer.add_custom_species(L"Test_Custom_Species_db2");
  indexer.add_custom_species(L"Test_Custom_Species_db3");
  indexer.add_custom_species(L"Test_Custom_Species_db4");
  cout << endl;

  cout << "[Delete]" << endl;
  //	indexer.delete_custom_species(L"Test_Custom_Species_db1");
  //	indexer.delete_custom_species(L"Test_Custom_Species_db2");
  //	indexer.delete_custom_species(L"Test_Custom_Species_db3");
  //	indexer.delete_custom_species(L"Test_Custom_Species_db4");
  cout << endl;

  cout << "[MaxDoc]" << endl;
  indexer.getMaxDoc();
  cout << endl;
  //	maxDocId: 2438086
  //	maxTaxId: 2971678
  //	maxTaxDetail: Melanina Melanina <ascomycete fungi>
}

/*
 * NCBIIndexer.hpp
 *
 *  Created on: Sep 20, 2022
 *      Author: neuroears
 */
#include <iostream>
#include <fstream>
//#include <sstream>
//#include <string>
//#include <regex>

#include "Lucene.h"
#include "StringUtils.h"

#include "targetver.h"
#include "LuceneHeaders.h"
#include "FileUtils.h"
#include "MiscUtils.h"
#include <boost/algorithm/string.hpp>

#ifndef NCBIINDEXER_HPP_
#define NCBIINDEXER_HPP_

using namespace std;
using namespace Lucene;

class NCBIIndexer
{
public:
  NCBIIndexer();
  virtual ~NCBIIndexer();
  void set_input_path(String path);
  void set_index_directory(String path);
  void parse();
  String search(String species);
  DocumentPtr fileDocument(String taxId, String taxDetail);
  void add_custom_species(String species);

private:
  String input_path;
  String output_directory_index;
};

#endif /* NCBIINDEXER_HPP_ */

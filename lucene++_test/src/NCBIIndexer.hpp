/*
 * NCBIIndexer.hpp
 *
 *  Created on: Sep 20, 2022
 *      Author: neuroears
 */
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <regex>

#include "Lucene.h"
#include "StringUtils.h"
#include "Directory.h"
#include "FSDirectory.h"
#include "Analyzer.h"
#include "IndexWriter.h"

#ifndef NCBIINDEXER_HPP_
#define NCBIINDEXER_HPP_

using namespace std;

class NCBIIndexer
{
public:
  NCBIIndexer();
  virtual ~NCBIIndexer();
  void set_input_path(string path);
  void set_index_directory(string path);
  void parse();

private:
  string input_path;
  string output_directory_index;
};

#endif /* NCBIINDEXER_HPP_ */

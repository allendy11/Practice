/*
 * NCBIIndexer.hpp
 *
 *  Created on: Sep 6, 2022
 *      Author: allen
 */

#ifndef NCBIINDEXER_HPP_
#define NCBIINDEXER_HPP_

#include <iostream>
#include <string>

#include "Lucene.h"
#include "StringUtils.h"

#include "targetver.h"
#include <iostream>
#include "LuceneHeaders.h"
#include "FileUtils.h"
#include "MiscUtils.h"
#include <boost/algorithm/string.hpp>

#include "FilterIndexReader.h"

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
  DocumentPtr fileDocument(String taxId, String taxDetail);
  String search(String species);
  void add_custom_species(String species);
  int32_t getMaxDoc();
  void delete_custom_species(String species);

private:
  String input_path;
  String output_directory_index;
};

#endif /* NCBIINDEXER_HPP_ */

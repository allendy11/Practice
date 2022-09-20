//============================================================================
// Name        : test_fileRead.cpp
// Author      : Dae-hee Yoon @Neuroears Ltd.
// Version     :
// Copyright   : All rights reserved by Dae-hee Yoon and Neuroears Ltd.
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <fstream>
#include <sstream>
#include <regex>

using namespace std;

string input_path = "/home/neuroears/taxdmp/names.dmp";
string output_path = "/home/neuroears/test/test.txt";

int main()
{
  fstream data;
  data.open(input_path, ios::in);
  string line;

  fstream test;
  test.open(output_path, ios::app);
  int n = 1000;

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
    cout << taxId << " " << taxDetail << endl;
    if (n > 0)
    {
      test << taxId << " " << taxDetail << endl;
      n--;
    }
    else
    {
      return -1;
    }
  }
}

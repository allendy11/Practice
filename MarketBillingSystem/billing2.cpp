//============================================================================
// Name        : MarketBillingSystem.cpp
// Author      : Allen.D.Y
// Version     :
// Copyright   : All rights reserved by Allen.D.Y
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <fstream>
#include <regex>
using namespace std;

class shopping
{
private:
  string uname; // username (admin/guest)
  string pcode; // product code
  string pname; // product name
  string price; // product price

public:
  void menu(); // start menu
               //	void _menu(); // close menu
  void greeting();
  void admin();
  void buyer();
  void search();
  void searcher(string code); // re-useable method
  void add();
  void modify();
  void del();
  void test(); // for test
};

void shopping::menu()
{
m:
  int choice;
  string email;
  string password;

  cout << " ___________________________ " << endl;
  cout << "|                           |" << endl;
  cout << "|   SuperMarket Main Menu   |" << endl;
  cout << "|___________________________|" << endl;
  cout << "|                           |" << endl;
  cout << "| 1) Admin                  |" << endl;
  cout << "|                           |" << endl;
  cout << "| 2) Buyer                  |" << endl;
  cout << "|                           |" << endl;
  cout << "| 3) Exit                   |" << endl;
  cout << "|___________________________|" << endl;
  cout << endl;
  cout << "Please select : ";
  cin >> choice;

  switch (choice)
  {
  case 1:
    cout << " ___________________________ " << endl;
    cout << "|                           |" << endl;
    cout << "|       Please Login        |" << endl;
    cout << "|___________________________|" << endl;
    cout << endl;
    cout << "Email : ";
    cin >> email;
    cout << "Password: ";
    cin >> password;
    cout << endl;

    if (email == "1231" && password == "1231")
    {
      uname = "Admin";
      greeting();
      admin();
    }
    else
    {

      cout << " ___________________________ " << endl;
      cout << "|                           |" << endl;
      cout << "| Invalid email or password |" << endl;
      cout << "|___________________________|" << endl;
      break;
    }
    exit(0);
  case 2:
    int num;
    uname = "Guest#";
    srand(time(NULL));
    num = rand() % 90000 + 10000;
    uname.append(to_string(num));
    greeting();
    buyer();
    exit(0);
  case 3:
    cout << " ___________________________ " << endl;
    cout << "|                           |" << endl;
    cout << "|      Martket closed       |" << endl;
    cout << "|___________________________|" << endl;
    exit(0);
  default:
    cout << " ___________________________ " << endl;
    cout << "|                           |" << endl;
    cout << "| Invalid choice.Try again. |" << endl;
    cout << "|___________________________|" << endl;
  }
  goto m;
}

// NOT FINISHED : NEED SOMETHING FOR SPECIFY MENU
// void shopping::_menu() {
//	//
//	n:
//	//
//	int choice;
//	cout << endl;
//	cout << " ___________________________" << endl;
//	cout << "|                           |" << endl;
//	cout << "| 1) Again                  |" << endl;
//	cout << "|                           |" << endl;
//	cout << "| 2) Administaor menu       |" << endl;
//	cout << "|                           |" << endl;
//	cout << "| 3) Main menu              |" << endl;
//	cout << "|                           |" << endl;
//	cout << "| 4) Exit                   |" << endl;
//	cout << "|___________________________|" << endl;
//	cout << "Please select : ";
//	cin >> choice;
//	switch (choice) {
//	case 1:
//		goto m;
//	case 2:
//		shopping::admin();
//	case 3:
//		shopping::menu();
//	case 4:
//		exit(0);
//	default:
//		cout << " ___________________________ " << endl;
//		cout << "|                           |" << endl;
//		cout << "| Invalid choice.Try again. |" << endl;
//		cout << "|___________________________|" << endl;
//		goto n;
//	}
//}

void shopping::greeting()
{
  cout << " ___________________________ " << endl;
  cout << "|                           |" << endl;
  if (uname == "Admin")
  {
    cout << "|       Welcome " << uname << "       |" << endl;
  }
  else
  {
    cout << "|   Welcome " << uname << "     |" << endl;
  }
  cout << "|___________________________|" << endl;
  cout << endl;
}
void shopping::admin()
{
m:
  int choice;
  cout << " ___________________________ " << endl;
  cout << "|                           |" << endl;
  cout << "|    Administrator Menu     |" << endl;
  cout << "|___________________________|" << endl;
  cout << "|                           |" << endl;
  cout << "| 1) Search the product     |" << endl;
  cout << "|                           |" << endl;
  cout << "| 2) Add the product        |" << endl;
  cout << "|                           |" << endl;
  cout << "| 3) Modify the product     |" << endl;
  cout << "|                           |" << endl;
  cout << "| 4) Delete the product     |" << endl;
  cout << "|                           |" << endl;
  cout << "| 5) Go back                |" << endl;
  cout << "|___________________________|" << endl;
  cout << "Please select : ";
  cin >> choice;

  switch (choice)
  {
  case 1:
    search();
    break;
  case 2:
    add();
    break;
  case 3:
    modify();
    break;
  case 4:
    del();
    break;
  case 5:
    menu();
    break;
  default:
    cout << " ___________________________ " << endl;
    cout << "|                           |" << endl;
    cout << "| Invalid choice.Try again. |" << endl;
    cout << "|___________________________|" << endl;
  }
  goto m;
}
void shopping::buyer()
{
  exit(0);
}

void shopping::searcher(string code)
{

  // 1) read data
  fstream test;
  test.open("./test.txt", ios::in);
  char str[100];

  // 1-1) split line
  while (test.getline(str, sizeof(str)))
  {
    istringstream iss(str);
    char separator = '|';
    string s;
    string arr[3];
    int i = 0;
    // 1-2) remove space
    while (getline(iss, s, separator))
    {
      regex r("\\s+");
      s = regex_replace(s, r, "");
      arr[i++] = s;
    }

    // 1-3) search
    pcode = arr[0];
    pname = arr[1];
    price = arr[2];

    if (pcode == code)
    {
      test.close();
      return;
    }
  }
  // NOT FINISHED : NEED MAX_CODE
  //	if (code == "0") {
  //		test.close();
  //		return;
  //	}
  // NOT MATCH (pcode == code)
  pcode = "";
  pname = "";
  price = "";
  test.close();
}

void shopping::search()
{
m:
  int choice;
  string icode;

  //	int i;
  //	fstream test;

  cout << " ___________________________ " << endl;
  cout << "|                           |" << endl;
  cout << "|      Search Product       |" << endl;
  cout << "|___________________________|" << endl;
  cout << "Insert Product Code : ";
  cin >> icode;

  shopping::searcher(icode);
  cout << " ___________________________ " << endl;
  cout << "|                           |" << endl;
  cout << "|   Search Product Result   |" << endl;
  cout << "|___________________________|" << endl;

  if (pcode == "")
  {
    cout << "Not found1" << endl;
  }
  else
  {
    cout << "Code : " << pcode << endl;
    cout << "Name : " << pname << endl;
    cout << "Price : " << price << endl;
  }

//
n:
  //
  cout << endl;
  cout << " ___________________________" << endl;
  cout << "|                           |" << endl;
  cout << "| 1) Again                  |" << endl;
  cout << "|                           |" << endl;
  cout << "| 2) Administaor menu       |" << endl;
  cout << "|                           |" << endl;
  cout << "| 3) Main menu              |" << endl;
  cout << "|                           |" << endl;
  cout << "| 4) Exit                   |" << endl;
  cout << "|___________________________|" << endl;
  cout << "Please select : ";
  cin >> choice;
  switch (choice)
  {
  case 1:
    goto m;
  case 2:
    shopping::admin();
  case 3:
    shopping::menu();
  case 4:
    exit(0);
  default:
    cout << " ___________________________ " << endl;
    cout << "|                           |" << endl;
    cout << "| Invalid choice.Try again. |" << endl;
    cout << "|___________________________|" << endl;
    goto n;
  }
}
void shopping::add()
{
//
m:
  //
  int choice;
  fstream test;
  string lpcode;
  string npcode;
  shopping::searcher("0");

  // 1) get info for add
  cout << " ___________________________ " << endl;
  cout << "|                           |" << endl;
  cout << "|      Add new product      |" << endl;
  cout << "|___________________________|" << endl;
  cout << "Name : ";
  cin >> pname;
  cout << "Price : ";
  cin >> price;

  // 2) read data for add
  test.open("./test.txt", ios::in);
  char str[100];
  string lp;
  while (test.getline(str, sizeof(str)))
  {
    lp = str;
  }

  // 2-1) split line to get product code;
  string arr[3];
  char separator = '|';
  string s;
  istringstream iss(lp);
  while (getline(iss, s, separator))
  {
    regex r("\\s+");
    s = regex_replace(s, r, "");
    lpcode = s;
    break;
  }
  test.close();

  // 2-2) write new product
  npcode = to_string(stoi(lpcode) + 1);
  test.open("./test.txt", ios::app);
  test << npcode << " | " << pname << " | " << price << endl;
  test.close();

  // 3) ask again
  cout << " ___________________________ " << endl;
  cout << "|                           |" << endl;
  cout << "| Complete add new product  |" << endl;
  cout << "|___________________________|" << endl;
  cout << "Code : " << npcode << endl;
  cout << "Product Name : " << pname << endl;
  cout << "Product Price : " << price << endl;
//
n:
  //
  cout << endl;
  cout << " ___________________________ " << endl;
  cout << "|                           |" << endl;
  cout << "| 1) Again                  |" << endl;
  cout << "|                           |" << endl;
  cout << "| 2) Main menu              |" << endl;
  cout << "|                           |" << endl;
  cout << "| 3) Exit                   |" << endl;
  cout << "|___________________________|" << endl;
  cout << "Please select : ";
  cin >> choice;
  switch (choice)
  {
  case 1:
    goto m;
  case 2:
    shopping::menu();
  case 3:
    exit(0);
  default:
    cout << " ___________________________ " << endl;
    cout << "|                           |" << endl;
    cout << "| Invalid choice.Try again. |" << endl;
    cout << "|___________________________|" << endl;
    goto n;
  }
};
void shopping::modify()
{
  //	//
  //	m:
  //	//
  //	int choice;
  //	fstream test;
  cout << " ___________________________ " << endl;
  cout << "|                           |" << endl;
  cout << "|  Modify existing product  |" << endl;
  cout << "|___________________________|" << endl;
}

void shopping::del(){};
int main()
{
  shopping s;
  s.menu();
}

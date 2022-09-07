//============================================================================
// Name        : MarketBillingSystem.cpp
// Author      : Allen.D.Y
// Version     :
// Copyright   : All rights reserved by Allen.D.Y
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <string>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <fstream>

using namespace std;

class shopping
{
private:
  string uname;
  string pcode;
  string pname;
  string price;

public:
  void menu();
  void greeting();
  void admin();
  void buyer();
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
  cout << "| 1) Add the product        |" << endl;
  cout << "|                           |" << endl;
  cout << "| 2) Modify the product     |" << endl;
  cout << "|                           |" << endl;
  cout << "| 3) Delete the product     |" << endl;
  cout << "|                           |" << endl;
  cout << "| 4) Go back                |" << endl;
  cout << "|___________________________|" << endl;
  cout << "Please select : ";
  cin >> choice;

  switch (choice)
  {
  case 1:
    add();
    break;
  case 2:
    modify();
    break;
  case 3:
    del();
    break;
  case 4:
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
void shopping::add(){
    //	m:
    //	fstream data;
    //	int c;
    //	int token=0;
    //	float p;
    //	float d;
    //	string n;
    //	cout << " ___________________________ " << endl;
    //	cout << "|                           |" << endl;
    //	cout << "|      Add new product      |" << endl;
    //	cout << "|___________________________|" << endl;
    //	cout << "Code : ";
    //	cin >> pcode;
    //	cout << "Name : ";
    //	cin >> pname;
    //	cout << "Price : ";
    //	cin >> price;
    //
    //	data.open("database.txt", ios::in);
    //	if(!data)
    //	{
    //		cout << "No Data" << endl;
    //		data.open("database.txt", ios::in | ios::out);
    //		data << " " << pcode << " " << pname << " " << price << "\n";
    //		data.close();
    //	}
    //	else
    //	{
    //		cout << "Data" << endl;
    //		data >> c >> n >> p >> d;
    //	}
    //	goto m;

};
void shopping::test()
{
m:
  fstream test;
  string code;
  string name;
  int price;
  int choice;
  cout << "what do you want for test? " << endl;
  cout << "1) add file" << endl;
  cout << "2) edit file" << endl;
  cout << "3) remove file" << endl;
  cout << "4) exit" << endl;
  cout << "select : ";
  cin >> choice;

  switch (choice)
  {
  case 1:
    test.open("./test.txt", ios::app);
    if (!test)
    {
      cout << "Create <test.txt> ..." << endl;
    }
    cout << "Input Infomation" << endl;
    cout << "code : ";
    cin >> code;
    cout << "name : ";
    cin >> name;
    cout << "price : ";
    cin >> price;
    test << code << " | " << name << " | " << price << endl;
    test.close();
    cout << "Finished." << endl;
    cout << "1) Go to menu" << endl;
    cout << "2) Exit" << endl;
    cout << "Please select : ";
    cin >> choice;
    if (choice == 1)
    {
      goto m;
    }
    cout << "Test closed" << endl;
    break;
  case 2:
    test.open("./test.txt", ios::in);
    char c;
    while (test.get(c))
    {
      cout << c;
    }
    test.close();
    cout << "Finished." << endl;
    cout << "1) Go to menu" << endl;
    cout << "2) Exit" << endl;
    cout << "Please select : ";
    cin >> choice;
    if (choice == 1)
    {
      goto m;
    }
    cout << "Test closed" << endl;
    break;
  case 3:
    cout << "Finished." << endl;
    cout << "1) Go to menu" << endl;
    cout << "2) Exit" << endl;
    cout << "Please select : ";
    cin >> choice;
    if (choice == 1)
    {
      goto m;
    }
    cout << "Test closed" << endl;
    break;
  case 4:
    cout << "Test closed" << endl;
    break;
  default:
    cout << "Invalid choice" << endl;
    goto m;
  }
}

void shopping::modify(){};
void shopping::del(){};
int main()
{
  shopping s;
  s.test();
}
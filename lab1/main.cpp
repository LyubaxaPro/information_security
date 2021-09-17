#include <iostream>
#include <fstream>
#include <stdio.h>
using namespace std;
#include "encoding.h"
#include "uuid.h"
#include "file_manager.h"

int main(int argc, char const *argv[]) {
  char *path_to_file = get_path();
  ifstream file(path_to_file);
  char str[100];
  file >> str;

  if (file.is_open() && strcmp(str, encoding(get_uuid())) == 0) {
    file.close();
    cout << "The application is loaded!!!!";
  }
  else {
    file.close();
    cout << "You don't have license for this program!!!";
  }
  return 0;
}
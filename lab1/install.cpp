#include <iostream>
#include <unistd.h>
#include <limits.h>
#include <fstream>
using namespace std;

#include "encoding.h"
#include "uuid.h"

int main(int argc, char const *argv[]) {
  char path_name[PATH_MAX];
  // Функция getcwd() копирует абсолютный путь к текущему рабочему каталогу в массиве, на который указывает buf
  getwd(path_name);

  char file_name[PATH_MAX] = ".license";

  char *path_to_file = new char[strlen(path_name) + strlen(file_name) + 2];
  strcpy(path_to_file, path_name);
  strcat(path_to_file, "/");
  strcat(path_to_file, file_name);
  ofstream file(path_to_file);

  char *mac_address = get_uuid();
  file << encoding(mac_address);
  file.close();
  return 0;
}
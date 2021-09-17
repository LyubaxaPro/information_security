#include "file_manager.h"

char *get_path() {
	char path_name[PATH_MAX];
  getwd(path_name);

  char file_name[PATH_MAX] = ".license";

  char *path_to_file = new char[strlen(path_name) + strlen(file_name) + 2];
  strcpy(path_to_file, path_name);
  strcat(path_to_file, "/");
  strcat(path_to_file, file_name);
  return path_to_file;
}
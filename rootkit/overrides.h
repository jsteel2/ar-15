#ifndef OVERRIDES_H_
#define OVERRIDES_H_

#include <stdio.h>
#include <dirent.h>
#include <dlfcn.h>

#define ORIG(x, ...) if (!original_##x) if (!(original_##x = dlsym(RTLD_NEXT, #x))) return __VA_ARGS__

extern int (*original_open)(const char *path, int flags, ...);
extern FILE *(*original_fopen)(const char *path, const char *mode);
extern struct dirent *(*original_readdir)(DIR *dirp);

#endif // OVERRIDES_H_

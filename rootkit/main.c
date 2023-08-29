#include <unistd.h>
#include "util.h"

#include "overrides.c"
#define dirent dirent64
#define readdir readdir64
#define original_readdir original_readdir64
#define open open64
#define original_open original_open64
#define openat openat64
#define original_openat original_openat64
#include "overrides.c"

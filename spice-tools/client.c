#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <gtk/gtk.h>
#include <spice-channel.h>
#include <spice-session.h>
#include <spice-widget.h>

static GtkWidget *main_window;
static SpiceSession *spice_session;
static SpiceDisplay *spice_display;
static char *host;
static char *port;


static void channel_new(SpiceSession *s, SpiceChannel *c, gpointer *data)
{
    int id = 0;

    g_object_get(c, "channel-id", &id, NULL);

    if (SPICE_IS_MAIN_CHANNEL(c)) {
        fprintf(stdout, "new main channel\n");
        return;
    }

    if (SPICE_IS_DISPLAY_CHANNEL(c)) {
        fprintf(stdout, "new display channel (#%d), creating window\n", id);
        spice_display = spice_display_new(s, id);
        gtk_container_add(GTK_CONTAINER(main_window), GTK_WIDGET(spice_display));
        gtk_widget_show_all(main_window);
        return;

    }

}

static void usage()
{
    fprintf(stdout, "spice-client: A spice client\n"
            "Usage: spice-client [options]...\n"
            "  -h, --host\n"
            "      Set address of spice server\n"
            "  -p, --port\n"
            "      Set port of spice server\n"
            "  -e, --help\n"
            "      Print help and exit\n"
        );
}

static void parse_cmd(int argc, char *argv[])
{
    int c, e = 0;

    if (argc == 1) {
        usage();
        exit(1);
    }

    const struct option long_options[] = {
        { "help", 0, 0, 'e' },
        { "host", 0, 0, 'h' },
        { "port", 0, 0, 'p' },
        { 0, 0, 0, 0 },
    };

    while ((c = getopt_long(argc, argv, "eh:p:",
                            long_options, NULL)) != EOF) {
        switch (c) {
        case 'e':
            goto failed;
        case 'h':
            host = optarg;
            break;
        case 'p':
            port = optarg;
            break;
        default:
            e++;
            break;
        }
    }

    if (e || argc > optind) {
        goto failed;
    }

    if (host == NULL || port == NULL) {
        fprintf(stderr, "No host or port found\n");
        goto failed;
    }

    return ;

failed:
    usage();
    exit(1);
}

int main(int argc, char *argv[])
{
    parse_cmd(argc, argv);

    gtk_init(&argc, &argv);
    main_window = gtk_window_new(GTK_WINDOW_TOPLEVEL);

    spice_session = spice_session_new();
    g_object_set(spice_session, "host", host, NULL);
    g_object_set(spice_session, "port", port, NULL);
    g_signal_connect(spice_session, "channel-new",
                     G_CALLBACK(channel_new), NULL);

    if (!spice_session_connect(spice_session)) {
        fprintf(stderr, "spice_session_connect failed\n");
        exit(1);
    }

    gtk_main();
    return 0;
}

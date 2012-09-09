spice-client: client.o
	gcc -o spice-client client.o `pkg-config --libs spice-client-gtk-3.0`
.c.o:
	gcc -c $< `pkg-config --cflags spice-client-gtk-3.0` -Wall

clean:
	rm *.o
	rm spice-client

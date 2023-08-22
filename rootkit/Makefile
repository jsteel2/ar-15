OBJ=main.o client.o util.o
PREFIX=.__EL_SNEEDIO__
BIN=$(PREFIX).so
LDFLAGS=-ldl -lutil
CFLAGS=-fPIC -shared -DPREFIX=\"$(PREFIX)\" -D_GNU_SOURCE -DHOST=\"$(HOST)\"

ifndef HOST
$(error set HOST pls)
endif

all: $(BIN)

$(BIN): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $(OBJ) $(LDFLAGS)

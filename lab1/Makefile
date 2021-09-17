key := -std=c++17 -Wall -Werror

%.o: %.cpp *.h
	g++ $(key) -c $<

install.out: encoding.o uuid.o install.o
	g++ $(key) -o $@ $^

main.out: encoding.o file_manager.o uuid.o main.o
	g++ $(key) -o $@ $^

clean:
	rm *.o *.out

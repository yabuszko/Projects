#include <SFML/Graphics.hpp>
#include "game_settings.h"
#include "Engine.h"
using namespace sf;

int main() {
	RenderWindow window{ VideoMode(width, height), "Platformer" };
	window.setFramerateLimit(60);

	Engine engine;
	engine.load_data_from_level(0);
	
	Event e;
	while (window.isOpen()) {
		while (window.pollEvent(e)) {
			switch (e.type) {
			case Event::Closed:
				window.close(); break;
			}
		}

		window.clear();
		engine.update(e, true);

		engine.show(&window);
		window.display();
	}

	return 0;
}
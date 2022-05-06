#include <SFML/Graphics.hpp>
#include <vector>
#include <iostream>
#include <cmath>

#include "Tile.h"
#include "GameManager.h"
using namespace sf;

const unsigned int width = 1152;
const unsigned int height = 640;

int main() {
	RenderWindow window{ VideoMode(width, height) , "MCTD, Oliwier Moskalewicz 2022"};
	window.setFramerateLimit(30);

	Texture grass_texture, sand_texture;
	grass_texture.loadFromFile("art/grass.png");
	sand_texture.loadFromFile("art/sand.png");

	GameManager manager(width, height);

	RenderTexture canvas_background;
	canvas_background.create(width, height);

	std::vector<std::vector<Tile*>> tiles;
	
	for (size_t i = 0; i < width / 64; i++) {
		std::vector<Tile*> row_vec;
		for (size_t j = 0; j < height / 64; j++) {
			row_vec.push_back(new Tile(&grass_texture, Vector2f(i * 64, j * 64), 'g'));
		}
		tiles.push_back(row_vec);
	}

	Event e;
	while (window.isOpen()) {
		while (window.pollEvent(e)) {
			if (e.type == Event::Closed)
				window.close();
			else if (e.type == Event::MouseButtonPressed) {
				Vector2f mousePos = static_cast<Vector2f>(Mouse::getPosition(window));
				mousePos.x = trunc(mousePos.x / 64) * 64;
				mousePos.y = trunc(mousePos.y / 64) * 64;

				manager.place_path(tiles, mousePos);
			}
			else if (e.type == Event::KeyPressed) {
				if (e.key.code == Keyboard::Space) {
					//manager.check_path(tiles);
				}
			}
		}

		canvas_background.clear();

		// canvas
		for (size_t i = 0; i < tiles.size(); i++) {
			for (size_t j = 0; j < tiles[i].size(); j++) {
				canvas_background.draw(*tiles[i][j]);
			}
		}
		canvas_background.display();

		Sprite canvas_background_sprite(canvas_background.getTexture());

		window.clear();

		window.draw(canvas_background_sprite);
		manager.show_money(&window);

		window.display();
	}

	return 0;
}
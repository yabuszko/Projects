#include "Engine.h"

Engine::Engine()
{
	this->canvas.create(width, height);

	this->brick_texture = new Texture;
	this->brick_texture->loadFromFile("art/brick.png");

	load_levels();
}

void Engine::load_levels()
{
	vector<string> row = {};
	string temp;
	ifstream file("data.txt");

	while (getline(file, temp)) {
		if (temp.find('\'') == string::npos) { // no ' in line
			row.push_back(temp);
		}
		else { // level read
			levels.push_back(row);
			row.clear();
		}
	}
}

void Engine::load_data_from_level(unsigned int level)
{
	for (size_t row = 0; row < levels[level].size(); row++) {
		for (size_t col = 0; col < levels[level][row].size(); col++) {
			float x = col * tile_size;
			float y = row * tile_size;

			switch (levels[level][row][col]) {
			case 'P':
				this->player.setPosition(Vector2f(x, y)); break;
			case 'X':
				this->bricks.push_back(Brick(x,y,brick_texture)); break;
			}
		}
	}
}

void Engine::update(Event& e, bool allowed)
{
	this->canvas.clear();

	this->player.update(e, allowed);
}

void Engine::show(RenderWindow* target)
{
	for (auto& b : bricks)
		b.render_in(&this->canvas);
	this->canvas.display();

	target->draw(Sprite(this->canvas.getTexture()));
	target->draw(this->player);
}

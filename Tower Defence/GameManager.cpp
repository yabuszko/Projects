#include <tuple>
#include <cmath>
#include "GameManager.h"

GameManager::GameManager(int width, int height)
{
	fin.open("other/data.txt");
	while (fin >> money) {
		std::cout << money << std::endl;
	};
	fin.close();

	minecraft_font.loadFromFile("other/minecraft font.otf");
	money_text.setFont(minecraft_font);
	money_text.setCharacterSize(32);
	money_text.setOutlineThickness(2);

	sand_texture.loadFromFile("art/sand.png");
	grass_texture.loadFromFile("art/grass.png");

	this->width = width;
	this->height = height;

	// markers setup
	std::vector<TileStat> row(trunc(width / tile_len), TileStat::Free); // all markers set to true by default
	markers.assign(trunc(height / tile_len), row);
}

void GameManager::show_money(RenderWindow* target)
{
	money_stream.str(std::string());
	money_stream << "Money: " << money;

	money_text.setString(money_stream.str());

	target->draw(money_text);
}

void GameManager::place_path(std::vector<std::vector<Tile*>>& tiles, Vector2f pos)
{
	if ((money - path_cost >= 0) &&
		markers[pos.y / tile_len][pos.x / tile_len] != TileStat::Disabled) {
		// path tile removal
		for (size_t i = 0; i < tiles.size(); i++) {
			for (size_t j = 0; j < tiles[i].size(); j++) {
				if (tiles[i][j]->getPosition() == pos && tiles[i][j]->type == 's') {
					markers[pos.y / tile_len][pos.x / tile_len] = TileStat::Free;
					tiles[i][j] = new Tile(&grass_texture, pos, 'g');

					this->money += this->path_cost;

					return;
				}
			}
		}

		// neighbour count
		int allowed = 0;
		int counter = 0;
		std::vector<unsigned short> temp_cts(4, 0);
		std::vector<unsigned short> temp_alw(4, 0);
		bool up = false, down = false, right = false, left = false;

		if (pos.y / tile_len == 0) { // top
			if (pos.x / tile_len + 1 == markers[0].size()) { // right
				if (markers[1][markers[0].size() - 1] == TileStat::Occupied && markers[0][markers[0].size() - 2] == TileStat::Occupied)
					return; // more than 1 neighbour
			}
			else { // max = 2
				allowed = 2;
				if (markers[pos.y / tile_len][pos.x / tile_len + 1] == TileStat::Occupied) {
					counter++; right = true;
				}
				if (markers[pos.y / tile_len + 1][pos.x / tile_len] == TileStat::Occupied) {
					counter++; down = true;
				}
				if (pos.x / tile_len != 0) {
					if (markers[pos.y / tile_len][pos.x / tile_len - 1] == TileStat::Occupied) {
						counter++; left = true;
					}
				}
			}
		}
		else if (pos.y / tile_len + 1 == markers.size()) { // bottom
			if (pos.x / tile_len == 0) { // left
				if (markers[markers.size() - 1][1] == TileStat::Occupied && markers[markers.size() - 2][0] == TileStat::Occupied)
					return; // more than 1 neighbour
			}
			else {
				allowed = 2;
				if (markers[pos.y / tile_len][pos.x / tile_len - 1] == TileStat::Occupied) {
					counter++; left = true;
				}
				if (markers[pos.y / tile_len - 1][pos.x / tile_len] == TileStat::Occupied) {
					counter++; up = true;
				}
				if (pos.x / tile_len + 1 != markers[0].size()) {
					if (markers[pos.y / tile_len][pos.x / tile_len + 1] == TileStat::Occupied) {
						counter++; right = true;
					}
				}
			}
		}
		else if (pos.x / tile_len == 0 && !(pos.y / tile_len == 0 || pos.y / tile_len + 1 == markers.size())) { // left but not corners
			allowed = 2;
			if (markers[pos.y / tile_len][pos.x / tile_len + 1] == TileStat::Occupied) {
				counter++; right = true;
			}
			if (markers[pos.y / tile_len + 1][pos.x / tile_len] == TileStat::Occupied) {
				counter++; down = true;
			}
			if (markers[pos.y / tile_len - 1][pos.x / tile_len] == TileStat::Occupied) {
				counter++; up = true;
			}
		}
		else if (pos.x / tile_len + 1 == markers[0].size() && !(pos.y / tile_len == 0 || pos.y / tile_len + 1 == markers.size())) { // right but not corners
			allowed = 2;
			if (markers[pos.y / tile_len][pos.x / tile_len - 1] == TileStat::Occupied) {
				counter++; left = true;
			}
			if (markers[pos.y / tile_len + 1][pos.x / tile_len] == TileStat::Occupied) {
				counter++; down = true;
			}
			if (markers[pos.y / tile_len - 1][pos.x / tile_len] == TileStat::Occupied) {
				counter++; up = true;
			}
		}
		else { // middle
			allowed = 2;
			if (markers[pos.y / tile_len][pos.x / tile_len - 1] == TileStat::Occupied) {
				counter++; left = true;
			}
			if (markers[pos.y / tile_len][pos.x / tile_len + 1] == TileStat::Occupied) {
				counter++; right = true;
			}
			if (markers[pos.y / tile_len + 1][pos.x / tile_len] == TileStat::Occupied) {
				counter++; down = true;
			}
			if (markers[pos.y / tile_len - 1][pos.x / tile_len] == TileStat::Occupied) {
				counter++; up = true;
			}
		}

		// if (dirs)
		int up1 = pos.y / tile_len - 1;
		int up2 = pos.y / tile_len - 2;
		int right1 = pos.x / tile_len + 1;
		int right2 = pos.x / tile_len + 2;
		int left1 = pos.x / tile_len - 1;
		int left2 = pos.x / tile_len - 2;
		int down1 = pos.y / tile_len + 1;
		int down2 = pos.y / tile_len + 2;
		if (up) {
			temp_cts[0]++;
			if (up1 == 0) { // up - top row
				if (pos.x / tile_len == 0) { // up - top left hand corner
					if (markers[up1][right1] == TileStat::Occupied) {
						temp_cts[0]++;
						temp_alw[0] = 2;
					}
				}
				else if (pos.x / tile_len + 1 == markers[0].size()) { // up - top right hand corner
					if (markers[up1][left1] == TileStat::Occupied) {
						temp_cts[0]++;
						temp_alw[0] = 1;
					}
				}
				else { // somewhere else, top row
					temp_alw[0] = 2;
					if (markers[up1][right1] == TileStat::Occupied) {
						temp_cts[0]++;
					}
					if (markers[up1][left1] == TileStat::Occupied) {
						temp_cts[0]++;
					}
				}
			}
			else if (pos.x / tile_len == 0) { // left col
				temp_alw[0] = 2;
				if (markers[up2][pos.x / tile_len] == TileStat::Occupied) {
					temp_cts[0]++;
				}
				if (markers[up1][right1] == TileStat::Occupied) {
					temp_cts[0]++;
				}
			}
			else if (pos.x / tile_len + 1 == markers.size()) { // right line
				temp_alw[0] = 2;
				if (markers[up2][pos.x / tile_len] == TileStat::Occupied) {
					temp_cts[0]++;
				}
				if (markers[up1][left1] == TileStat::Occupied) {
					temp_cts[0]++;
				}
			}
			else { // anywhere else
				temp_alw[0] = 2;
				if (markers[up2][pos.x / tile_len] == TileStat::Occupied) {
					temp_cts[0]++;
				}
				if (markers[up1][left1] == TileStat::Occupied) {
					temp_cts[0]++;
				}
				if (markers[up1][right1] == TileStat::Occupied) {
					temp_cts[0]++;
				}
			}
		}
		if (down) {
			temp_cts[1]++;
			if (down1 + 1 == static_cast<unsigned short>(markers.size())) { // bottom row
				if (pos.x / tile_len == 0) { // bottom left hand corner
					temp_alw[1] = 1;
					if (markers[down1][right1] == TileStat::Occupied) {
						temp_cts[1]++;
					}
				}
				else if (pos.x / tile_len + 1 == markers[0].size()) { // bottom right hand corner
					temp_alw[1] = 2;
					if (markers[down1][left1] == TileStat::Occupied) {
						temp_cts[1]++;
					}
				}
				else { // somewhere else, bottom row
					temp_alw[1] = 2;
					if (markers[down1][right1] == TileStat::Occupied)
						temp_cts[1]++;
					if (markers[down1][left1] == TileStat::Occupied)
						temp_cts[1]++;
				}
			}
			else if (pos.x / tile_len == 0) { // left line
				temp_alw[1] = 2;
				if (markers[down2][pos.x / tile_len] == TileStat::Occupied)
					temp_cts[1]++;
				if (markers[down1][right1] == TileStat::Occupied)
					temp_cts[1]++;
			}
			else if (pos.x / tile_len + 1 == markers[0].size()) { // right line
				temp_alw[1] = 2;
				if (markers[down2][pos.x / tile_len] == TileStat::Occupied)
					temp_cts[1]++;
				if (markers[down1][left1] == TileStat::Occupied)
					temp_cts[1]++;
			}
			else { // anywhere else
				temp_alw[1] = 2;
				if (markers[down2][pos.x / tile_len] == TileStat::Occupied)
					temp_cts[1]++;
				if (markers[down1][left1] == TileStat::Occupied)
					temp_cts[1]++;
				if (markers[down1][right1] == TileStat::Occupied)
					temp_cts[1]++;
			}
		}
		if (right) {
			temp_cts[2]++;
			if (right1 + 1 == static_cast<unsigned short>(markers[0].size())) { // right col
				if (pos.y / tile_len == 0) { // top right hand corner
					temp_alw[2] = 1;
					if (markers[down1][right1] == TileStat::Occupied)
						temp_cts[2]++;
				}
				else if (pos.y / tile_len + 1 == markers.size()) {
					temp_alw[2] = 1;
					if (markers[up1][right1] == TileStat::Occupied)
						temp_cts[2]++;
				}
				else {
					temp_alw[2] = 2;
					if (markers[up1][right1] == TileStat::Occupied)
						temp_cts[2]++;
					if (markers[down1][right1] == TileStat::Occupied)
						temp_cts[2]++;
				}
			}
			else if (pos.y / tile_len == 0) { // top row
				temp_alw[2] = 2;
				if (markers[pos.y / tile_len][right2] == TileStat::Occupied)
					temp_cts[2]++;
				if (markers[down1][right1] == TileStat::Occupied)
					temp_cts[2]++;
			}
			else if (pos.y / tile_len + 1 == markers.size()) { // bottom row
				temp_alw[2] = 2;
				if (markers[pos.y / tile_len][right2] == TileStat::Occupied)
					temp_cts[2]++;
				if (markers[up1][right1] == TileStat::Occupied)
					temp_cts[2]++;
			}
			else { // anywhere else
				temp_alw[2] = 2;
				if (markers[pos.y / tile_len][right2] == TileStat::Occupied)
					temp_cts[2]++;
				if (markers[up1][right1] == TileStat::Occupied)
					temp_cts[2]++;
				if (markers[down1][right1] == TileStat::Occupied)
					temp_cts[2]++;
			}
		}
		if (left) {
			temp_cts[3]++;
			if (left1 == 0) { // left col
				if (pos.y / tile_len == 0) { // top left hand corner
					temp_alw[3] = 2;
					if (markers[down1][left1] == TileStat::Occupied)
						temp_cts[3]++;
				}
				else if (pos.y / tile_len + 1 == markers.size()) { // bottom left hand corner
					temp_alw[3] = 1;
					if (markers[up1][left1] == TileStat::Occupied)
						temp_cts[3]++;
				}
				else {
					temp_alw[3] = 2;
					if (markers[up1][left1] == TileStat::Occupied)
						temp_cts[3]++;
					if (markers[down1][left1] == TileStat::Occupied)
						temp_cts[3]++;
				}
			}
			else if (pos.y / tile_len == 0) { // top row
				temp_alw[3] = 2;
				if (markers[pos.y / tile_len][left2] == TileStat::Occupied)
					temp_cts[3]++;
				if (markers[down1][left1] == TileStat::Occupied)
					temp_cts[3]++;
			}
			else if (pos.y / tile_len + 1 == markers.size()) { // bottom row
				temp_alw[3] = 2;
				if (markers[pos.y / tile_len][left2] == TileStat::Occupied)
					temp_cts[3]++;
				if (markers[up1][left1] == TileStat::Occupied)
					temp_cts[3]++;
			}
			else { // anywhere else
				temp_alw[3] = 2;
				if (markers[pos.y / tile_len][left2] == TileStat::Occupied)
					temp_cts[3]++;
				if (markers[up1][left1] == TileStat::Occupied)
					temp_cts[3]++;
				if (markers[down1][left1] == TileStat::Occupied)
					temp_cts[3]++;
			}
		}

		if (counter <= allowed && temp_cts[0] <= temp_alw[0] && temp_cts[1] <= temp_alw[1]
			&& temp_cts[2] <= temp_alw[2] && temp_cts[3] <= temp_alw[3]) {
			tiles[pos.x / tile_len][pos.y / tile_len] = new Tile(&sand_texture, Vector2f(pos.x, pos.y), 's');
			markers[pos.y / tile_len][pos.x / tile_len] = TileStat::Occupied;

			money -= path_cost;
		}
	}
}

void GameManager::check_path(std::vector<Tile*>& tiles)
{
	static unsigned short id = 0;
	// checking for neighbours
	for (size_t i = 0; i < tiles.size(); i++) {
		if (tiles[i]->type == 's') {
			for (size_t j = 0; j < tiles.size(); j++) {
				if (tiles[j]->type == 's') {
					if ((tiles[j]->getPosition() == Vector2f(tiles[i]->getPosition().x + tile_len, tiles[i]->getPosition().y))
						|| (tiles[j]->getPosition() == Vector2f(tiles[i]->getPosition().x - tile_len, tiles[i]->getPosition().y))
						|| (tiles[j]->getPosition() == Vector2f(tiles[i]->getPosition().x, tiles[i]->getPosition().y - tile_len))
						|| (tiles[j]->getPosition() == Vector2f(tiles[i]->getPosition().x, tiles[i]->getPosition().y + tile_len))) {
						// has neighbour(s), assign id
						tiles[i]->index = id;
						++id; j = tiles.size();
					}
				}
			}
			tiles[i]->setFillColor(Color(tiles[i]->index * 2, tiles[i]->index * 2, tiles[i]->index * 2));
		}
	}
}

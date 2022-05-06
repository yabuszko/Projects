#pragma once
#include <SFML/Graphics.hpp>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <string>

#include "Tile.h"
using namespace sf;

class GameManager
{
public:
	explicit GameManager(int width, int height);

	void show_money(RenderWindow* target);
	void place_path(std::vector<std::vector<Tile*>>& tiles, Vector2f pos);

	void check_path(std::vector<Tile*>& tiles);

	template <typename Enumeration>
	auto as_integer(Enumeration const val)
		-> typename std::underlying_type<Enumeration>::type;
private:
	enum class TileStat {Free=1, Occupied=2, Disabled=3};
	
	int money;
	const int path_cost = 50;
	const int tile_len = 64;

	int width, height;

	Texture sand_texture;
	Texture grass_texture;

	Font minecraft_font;
	Text money_text;

	std::ostringstream money_stream;

	std::vector<std::vector<TileStat>> markers;

	std::ifstream fin;
};

template<typename Enumeration>
inline auto GameManager::as_integer(Enumeration const val) -> typename std::underlying_type<Enumeration>::type
{
	return static_cast<typename std::underlying_type<Enumeration>::type>(val);
}

#pragma once
#include <vector>
#include <string>
#include <fstream>
#include <iostream>

#include "Player.h"
#include "game_settings.h"
#include "Tile.h"
using namespace std;
using namespace sf;
class Engine
{
public:
	Engine();

	void load_data_from_level(unsigned int level);

	void update(Event& e, bool allowed);
	void show(RenderWindow* target);

	Player player;
private:
	void load_levels();

	typedef vector<vector<string>> Matrix;
	typedef vector<string> Row;

	Matrix levels = {};

	// objects
	vector<Brick> bricks;

private:
	RenderTexture canvas;

	Texture* brick_texture;

public:
	unsigned int no_levels = 2;
};


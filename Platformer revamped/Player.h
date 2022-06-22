#pragma once
#include <SFML/Graphics.hpp>
using namespace sf;
class Player :public RectangleShape
{
public:
	Player(Vector2f pos);
	Player() : Player(Vector2f()) {}

	void update(Event& e, bool allowed_to_jump_mid_air);

	void jump(bool allowed);

	void show(RenderWindow* target) const;
private:
	Vector2i direction = { 0, 0 };
	float speed = 6;
	float jump_speed = -16; // y-axis is reversed

	const float gravity = 0.8;
	
	bool jumped = false;
};


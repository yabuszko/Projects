#include "Player.h"

Player::Player(Vector2f pos) {
	setSize(Vector2f(32, 64));
	setFillColor(Color::Red);
	setPosition(pos);
}

void Player::update(Event& e, bool allowed_to_jump_mid_air) {
	if (e.key.code == Keyboard::Right || e.key.code == Keyboard::D)
		this->direction.x = 1;
	if (e.key.code == Keyboard::Left || e.key.code == Keyboard::A)
		this->direction.x = -1;
	if (e.key.code != Keyboard::Left && e.key.code != Keyboard::A)
		this->direction.x = 0;

	if (e.key.code == Keyboard::Space)
		jump(allowed_to_jump_mid_air);
}

void Player::jump(bool allowed) {
	if (this->jumped != true && (this->direction.y == 0 || allowed)) {
		this->direction.y = this->jump_speed;
		this->jumped = true;
	}
}

void Player::show(RenderWindow* target) const {
	target->draw(*this);
}

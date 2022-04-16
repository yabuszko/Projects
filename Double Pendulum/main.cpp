#include <SFML/Graphics.hpp>
#include <cmath>
#include <iostream>
#include <vector>

#include "settings.h"
using namespace std;
using namespace sf;

class Ball :public CircleShape {
public:
	Ball(float r, Color col, Vector2f pos, float m=0.f) {
		setRadius(r);
		setOrigin(r, r); // centre

		this->mass = m;

		this->position = pos;
		setPosition(pos);
		setFillColor(col);
	}

	void show(RenderWindow* target) const {
		target->draw(*this);
	}

private:
	Vector2f position;

public:
	float mass;
};

class Line :public RectangleShape {
public:
	Line(Vector2f pos, float width, float angle) {
		this->thickness = width;
		this->position = pos;
		this->rotation = angle;

		this->velocity = 0;
		this->acceleration = 0;

		setPosition(this->position);
		setSize(Vector2f(this->thickness, this->length));
		setFillColor(Color(50, 50, 50));

		setRotation(this->rotation * 180 / pi);
		//setOrigin(getSize().x / 2, 0.f);
	}

	void update() {
		this->velocity += this->acceleration;

		if (to_rest)
			this->acceleration *= 0.999;

		float new_angle = getRotation() * pi / 180 + this->velocity;

		setRotation(new_angle * 180/pi);
	}

	const float getLength() const {
		return this->length;
	}

	void show(RenderWindow* target) const {
		target->draw(*this);
	}
private:
	const float length = 200;

	float thickness;
	float rotation;
	Vector2f position;

public:
	float velocity;
	float acceleration;
};

class Trace {
public:
	Trace(RenderTexture* target) 
	:position_init({0,0}), position_final({0,0})
	{
		this->body = target;
		this->body->clear();
	}

	void get_data(Vector2f pos) {
		this->position_init = pos;
	}

	void leave_dot(Vector2f pos, Color col) {
		this->point_a.position = position_init;
		this->point_a.color = col;
		
		this->point_b.position = pos;
		this->point_b.color = col;

		this->position_init = pos;

		VertexArray temp_arr(LinesStrip, 2);
		temp_arr[0] = this->point_a;
		temp_arr[1] = this->point_b;
		this->body->draw(temp_arr);
	}
private:
	Vertex point_a;
	Vertex point_b;

	RenderTexture* body;

	Vector2f position_init;
	Vector2f position_final;
};

int main() {
	read_data();

	ContextSettings settings;
	settings.antialiasingLevel = 8;

	RenderWindow window(VideoMode(0, 0), "Double pendulum", Style::Fullscreen, settings);
	window.setFramerateLimit(60);
	window.setKeyRepeatEnabled(false);

	// Pivot
	Ball pivot(10.f, Color::White, Vector2f(VideoMode::getDesktopMode().width / 2, VideoMode::getDesktopMode().height / 2));
	
	// RenderTexture
	RenderTexture canvas;
	canvas.create(VideoMode::getDesktopMode().width, VideoMode::getDesktopMode().height);

	// coords translation
	Vector2f translated = pivot.getPosition();

	// Other objects
	Line line1(pivot.getPosition(), 1.f, -pi/2);

	unsigned int faster = 0;

	Ball m1(ma1 / 2, Color(0, 255, 0, 100), Vector2f(translated.x + line1.getLength() * sin(-line1.getRotation() * pi / 180),
		translated.y + line1.getLength() * cos(line1.getRotation() * pi / 180)), ma1);

	Line line2(m1.getPosition(), 1.f, -pi/2);

	Ball m2(ma2 / 2, Color(0, 255, 0, 100), Vector2f(m1.getPosition().x + line2.getLength() * sin(-line2.getRotation() * pi / 180),
		m1.getPosition().y + line2.getLength() * cos(line2.getRotation() * pi / 180)), ma2);

	// Trace
	Trace trace_1(&canvas);
	Trace trace_2(&canvas);
	trace_1.get_data(m1.getPosition());
	trace_2.get_data(m2.getPosition());

	while (window.isOpen()) {
		Event e;
		while (window.pollEvent(e)) {
			if (e.type == Event::KeyPressed) {
				if (e.key.code == Keyboard::Escape)
					window.close();
				else if (e.key.code == Keyboard::Space) {
					if (faster == 0) faster = 1;
					else faster = 0;
				}
			}
		}
		
		// update
		//line1.setRotation(line1.getRotation() + 0.5);
		//line2.setRotation(line2.getRotation() - 0.3);
		for (size_t i = 0; i < 1 + speed_factor * faster; i++) {
			float num1 = -gravitational_acceleration * (2 * m1.mass + m2.mass) * sin(line1.getRotation() * pi / 180);
			float num2 = -m2.mass * gravitational_acceleration * sin((line1.getRotation() - 2 * line2.getRotation()) * pi / 180);
			float num3 = -2 * sin((line1.getRotation() - line2.getRotation()) * pi / 180);
			float num4 = line2.velocity * line2.velocity * line2.getLength() + line1.velocity * line1.velocity * line1.getLength() *
				cos((line1.getRotation() - line2.getRotation()) * pi / 180);
			float den = line1.getLength() * 2 * (m1.mass + m2.mass - m2.mass * cos((2 * line1.getRotation() - 2 * line2.getRotation()) * pi / 180));
			line1.acceleration = (num1 + num2 + num3 * num4) / den;

			num1 = 2 * sin((line1.getRotation() - line2.getRotation()) * pi / 180);
			num2 = line1.velocity * line1.velocity * line1.getLength() * (m1.mass + m2.mass);
			num3 = gravitational_acceleration * (m1.mass + m2.mass) * cos(line1.getRotation() * pi / 180);
			num4 = line2.velocity * line2.velocity * line2.getLength() * m2.mass * cos((line1.getRotation() - line2.getRotation()) * pi / 180);
			den = line2.getLength() * 2 * (m1.mass + m2.mass - m2.mass * cos((2 * line1.getRotation() - 2 * line2.getRotation()) * pi / 180));
			line2.acceleration = num1 * (num2 + num3 + num4) / den;

			line1.update();
			line2.update();

			m1.setPosition(Vector2f(translated.x + line1.getLength() * sin(-line1.getRotation() * pi / 180),
				translated.y + line1.getLength() * cos(line1.getRotation() * pi / 180)));
			m2.setPosition(Vector2f(m1.getPosition().x + line2.getLength() * sin(-line2.getRotation() * pi / 180),
				m1.getPosition().y + line2.getLength() * cos(line2.getRotation() * pi / 180)));
			line2.setPosition(m1.getPosition());

			trace_1.leave_dot(m1.getPosition(), Color(13, 128, 43));
			trace_2.leave_dot(m2.getPosition(), Color(72, 217, 109));
			canvas.display();
		}

		//cout << line1.getPosition().x << " " << line1.getPosition().y <<  " " << line1.acceleration << endl;

		// draw
		window.clear(Color::Black);
		Sprite container;
		container.setTexture(canvas.getTexture());
		container.setPosition(0, 0);

		window.draw(container);

		line1.show(&window);
		line2.show(&window);

		pivot.show(&window);
		m1.show(&window);
		m2.show(&window);

		window.display();
		
	}

	return 0;
}
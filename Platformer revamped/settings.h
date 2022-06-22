#pragma once
#include <fstream>
#include <iostream>
using namespace std;

float ma1 = 40;
float ma2 = 20;

float len1 = 200;
float len2 = 200;

bool to_rest = false;
bool set_new_values = false;

size_t speed_factor = 5;

const float pi = 3.1415927;
const float gravitational_acceleration = 0.1;

void read_data() {
	string line;
	ifstream file("dane.txt");
	if (file.is_open()) {
		
		while (file >> ma1 >> ma2 >> len1 >> len2 >> to_rest) {
			cout << ma1 << " " << ma2 << " " << to_rest << endl;
		}
		file.close();
	}
	else cout << "error" << endl;
}

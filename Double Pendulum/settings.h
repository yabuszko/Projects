#pragma once
#include <fstream>
using namespace std;

float ma1 = 40;
float ma2 = 20;

bool to_rest = false;

size_t speed_factor = 5;

const float pi = 3.1415927;
const float gravitational_acceleration = 0.06;

void read_data() {
	string line;
	ifstream file("dane.txt");
	if (file.is_open()) {
		
		while (file >> ma1 >> ma2 >> to_rest) {
			cout << ma1 << " " << ma2 << " " << to_rest << endl;
		}
		file.close();
	}
	else cout << "error" << endl;
}

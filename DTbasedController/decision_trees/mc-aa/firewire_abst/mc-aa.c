#include <stdio.h>

float classify(const float x[]);

int main() {
    float x[] = {0.f,0.f};
    float result = classify(x);
    return 0;
}

float classify(const float x[]) {
	if (x[1] == 0) {
		return 0.0f;
	}
	else if (x[1] == 1) {
		return 1.0f;
	}
	else if (x[1] == 2) {
		return 1.0f;
	}
	else if (x[1] == 3) {
		return 1.0f;
	}
	else if (x[1] == 4) {
		return 1.0f;
	}
	else if (x[1] == 5) {
		if (x[0] <= 25.5) {
			return 2.0f;
		}
		else {
			return 1.0f;
		}

	}
	else if (x[1] == 6) {
		if (x[0] <= 108.5) {
			return 2.0f;
		}
		else {
			return 1.0f;
		}

	}
	else if (x[1] == 7) {
		if (x[0] <= 108.5) {
			return 2.0f;
		}
		else {
			return 1.0f;
		}

	}
	else if (x[1] == 8) {
		if (x[0] <= 108.5) {
			return 2.0f;
		}
		else {
			return 1.0f;
		}

	}

}
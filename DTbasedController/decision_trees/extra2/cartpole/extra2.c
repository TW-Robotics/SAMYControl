#include <stdio.h>

float classify(const float x[]);

int main() {
    float x[] = {3.12f,-0.9f};
    float result = classify(x);
    return 0;
}

float classify(const float x[]) {
	if (x[0] <= 3.16) {
		if (x[1] <= 0.75) {
			if (x[1] <= -0.45) {
				return 2.7f;
			}
			else {
				if (x[1] <= 0.15) {
					return 3.9f;
				}
				else {
					return 0.0f;
				}

			}

		}
		else {
			return -2.2f;
		}

	}
	else {
		if (x[1] <= -0.75) {
			return 2.2f;
		}
		else {
			return -3.8f;
		}

	}

}
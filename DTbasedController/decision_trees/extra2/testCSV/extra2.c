#include <stdio.h>

void classify(const float x[], float result[]);

int main() {
    float x[] = {18.75f,20.0f,18.75f,18.75f,20.0f,18.75f,18.75f,18.75f,18.75f,18.75f};
    float result[2];
    classify(x, result);
    return 0;
}

void classify(const float x[], float result[]) {
	if (x[1] <= 20.625) {
		result[0] = 1.0f; result[1] = 1.0f;
	}
	else {
		if (x[0] <= 19.375) {
			result[0] = 0.0f; result[1] = 1.0f;
		}
		else {
			result[0] = 0.0f; result[1] = 1.0f;
		}

	}

}
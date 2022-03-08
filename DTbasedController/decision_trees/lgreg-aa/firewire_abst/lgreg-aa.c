#include <stdio.h>

float classify(const float x[]);

int main() {
    float x[] = {0.f,0.f};
    float result = classify(x);
    return 0;
}

float classify(const float x[]) {
	if (-0.07688932653759994*x[0]+2.469416111905296*x[1]-9.543779739790267 <= 0) {
		if (0.506205994256847*x[0]-67.23556195770792*x[1]+10.61441550212217 <= 0) {
			if (x[1] <= 5.5) {
				return 1.0f;
			}
			else {
				if (28.180461300703747*x[0]+1.272006324851469*x[1]-3066.078891041682 <= 0) {
					return 2.0f;
				}
				else {
					return 1.0f;
				}

			}

		}
		else {
			return 0.0f;
		}

	}
	else {
		if (x[0] <= 108.5) {
			if (24.08660690747304*x[0]-1059.9956410571963*x[1]+4686.023717296558 <= 0) {
				return 2.0f;
			}
			else {
				return 1.0f;
			}

		}
		else {
			return 1.0f;
		}

	}

}
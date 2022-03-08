#include <stdio.h>

float classify(const float x[]);

int main() {
    float x[] = {2.f,0.f,0.f,2.f,0.f,0.f,2.f,0.f,0.f,0.f,0.f,0.f,0.f,0.f,0.f,0.f,0.f};
    float result = classify(x);
    return 0;
}

float classify(const float x[]) {
	if (x[11] == 0) {
		return 0.0f;
	}
	else if (x[11] == 1) {
		if (x[2] <= 0.5) {
			if (x[12] == 0) {
				return 1.0f;
			}
			else if (x[12] == 1) {
				if (x[5] <= 0.5) {
					if (x[13] == 0) {
						return 2.0f;
					}
					else if (x[13] == 1) {
						return 3.0f;
					}
					else if (x[13] == 5) {
						return 12.0f;
					}

				}
				else {
					return 17.0f;
				}

			}
			else if (x[12] == 5) {
				return 11.0f;
			}

		}
		else {
			if (x[5] <= 0.5) {
				if (x[13] == 1) {
					return 18.0f;
				}
				else if (x[13] == 5) {
					return 12.0f;
				}

			}
			else {
				return 14.0f;
			}

		}

	}
	else if (x[11] == 2) {
		if (x[14] == 1) {
			return 19.0f;
		}
		else if (x[14] == 2) {
			if (x[7] <= 2.5) {
				if (x[6] <= 3.0) {
					return 4.0f;
				}
				else {
					return 23.0f;
				}

			}
			else {
				return 26.0f;
			}

		}

	}
	else if (x[11] == 3) {
		if (x[12] == 2) {
			if (x[14] == 1) {
				return 21.0f;
			}
			else if (x[14] == 2) {
				if (x[1] <= 2.5) {
					if (x[0] <= 3.0) {
						return 5.0f;
					}
					else {
						return 24.0f;
					}

				}
				else {
					return 27.0f;
				}

			}

		}
		else if (x[12] == 3) {
			if (x[13] == 2) {
				if (x[14] == 1) {
					return 22.0f;
				}
				else if (x[14] == 2) {
					if (x[4] <= 2.5) {
						if (x[3] <= 3.0) {
							return 6.0f;
						}
						else {
							return 25.0f;
						}

					}
					else {
						return 28.0f;
					}

				}

			}
			else if (x[13] == 3) {
				return 7.0f;
			}

		}
		else if (x[12] == 6) {
			if (x[4] <= 2.5) {
				return 25.0f;
			}
			else {
				return 28.0f;
			}

		}

	}
	else if (x[11] == 4) {
		if (x[10] == 2) {
			return 8.0f;
		}
		else if (x[10] == 3) {
			return 9.0f;
		}

	}
	else if (x[11] == 5) {
		if (x[8] <= 0.5) {
			return 10.0f;
		}
		else {
			if (x[14] == 0) {
				if (x[2] <= 0.5) {
					return 11.0f;
				}
				else {
					if (x[5] <= 0.5) {
						return 12.0f;
					}
					else {
						return 13.0f;
					}

				}

			}
			else if (x[14] == 1) {
				if (x[12] == 1) {
					if (x[5] <= 0.5) {
						return 12.0f;
					}
					else {
						return 15.0f;
					}

				}
				else if (x[12] == 5) {
					if (x[2] <= 0.5) {
						return 11.0f;
					}
					else {
						return 16.0f;
					}

				}

			}
			else if (x[14] == 2) {
				return 20.0f;
			}

		}

	}
	else if (x[11] == 6) {
		if (x[12] == 2) {
			if (x[1] <= 2.5) {
				return 24.0f;
			}
			else {
				return 27.0f;
			}

		}
		else if (x[12] == 3) {
			if (x[4] <= 2.5) {
				return 25.0f;
			}
			else {
				return 28.0f;
			}

		}
		else if (x[12] == 6) {
			if (x[4] <= 2.5) {
				return 25.0f;
			}
			else {
				return 28.0f;
			}

		}

	}

}
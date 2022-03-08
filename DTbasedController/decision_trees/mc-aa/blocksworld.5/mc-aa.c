#include <stdio.h>

float classify(const float x[]);

int main() {
    float x[] = {0.f,1.f,0.f,0.f,0.f,0.f,1.f,6.f,6.f,5.f,1.f,6.f};
    float result = classify(x);
    return 0;
}

float classify(const float x[]) {
	if (x[7] == 0) {
		if (x[1] == 0) {
			if (x[2] == 0) {
				if (x[6] == 0) {
					if (x[8] == 3) {
						if (x[5] == 0) {
							return 36.0f;
						}
						else if (x[5] == 1) {
							return 50.0f;
						}

					}
					else if (x[8] == 4) {
						if (x[11] == 3) {
							return 20.0f;
						}
						else if (x[11] == 6) {
							return 50.0f;
						}

					}
					else if (x[8] == 6) {
						if (x[10] == 3) {
							return 20.0f;
						}
						else if (x[10] == 6) {
							if (x[11] == 3) {
								if (x[5] == 0) {
									return 36.0f;
								}
								else if (x[5] == 1) {
									return 20.0f;
								}

							}
							else if (x[11] == 4) {
								return 36.0f;
							}
							else if (x[11] == 6) {
								if (x[5] == 0) {
									return 20.0f;
								}
								else if (x[5] == 1) {
									return 36.0f;
								}

							}

						}

					}

				}
				else if (x[6] == 1) {
					if (x[5] == 0) {
						if (x[10] == 3) {
							return 6.0f;
						}
						else if (x[10] == 5) {
							if (x[4] == 0) {
								return 36.0f;
							}
							else if (x[4] == 1) {
								return 50.0f;
							}

						}
						else if (x[10] == 6) {
							if (x[4] == 0) {
								if (x[8] == 5) {
									return 36.0f;
								}
								else if (x[8] == 6) {
									return 6.0f;
								}

							}
							else if (x[4] == 1) {
								return 6.0f;
							}

						}

					}
					else if (x[5] == 1) {
						if (x[8] == 3) {
							return 50.0f;
						}
						else if (x[8] == 4) {
							if (x[4] == 0) {
								if (x[9] == 5) {
									return 36.0f;
								}
								else if (x[9] == 6) {
									return 61.0f;
								}

							}
							else if (x[4] == 1) {
								return 50.0f;
							}

						}
						else if (x[8] == 5) {
							return 50.0f;
						}
						else if (x[8] == 6) {
							return 50.0f;
						}

					}

				}

			}
			else if (x[2] == 1) {
				if (x[6] == 0) {
					if (x[4] == 0) {
						if (x[9] == 2) {
							if (x[5] == 0) {
								return 36.0f;
							}
							else if (x[5] == 1) {
								return 61.0f;
							}

						}
						else if (x[9] == 4) {
							return 20.0f;
						}
						else if (x[9] == 6) {
							if (x[11] == 2) {
								return 20.0f;
							}
							else if (x[11] == 4) {
								return 61.0f;
							}
							else if (x[11] == 6) {
								return 20.0f;
							}

						}

					}
					else if (x[4] == 1) {
						if (x[5] == 0) {
							if (x[10] == 2) {
								return 20.0f;
							}
							else if (x[10] == 3) {
								if (x[9] == 2) {
									return 6.0f;
								}
								else if (x[9] == 6) {
									return 20.0f;
								}

							}
							else if (x[10] == 6) {
								return 6.0f;
							}

						}
						else if (x[5] == 1) {
							return 20.0f;
						}

					}

				}
				else if (x[6] == 1) {
					if (x[5] == 0) {
						if (x[4] == 0) {
							if (x[9] == 2) {
								if (x[8] == 5) {
									return 6.0f;
								}
								else if (x[8] == 6) {
									return 61.0f;
								}

							}
							else if (x[9] == 5) {
								return 6.0f;
							}
							else if (x[9] == 6) {
								if (x[8] == 5) {
									return 61.0f;
								}
								else if (x[8] == 6) {
									return 6.0f;
								}

							}

						}
						else if (x[4] == 1) {
							return 6.0f;
						}

					}
					else if (x[5] == 1) {
						return 61.0f;
					}

				}

			}

		}
		else if (x[1] == 1) {
			if (x[10] == 1) {
				if (x[9] == 2) {
					if (x[4] == 0) {
						if (x[6] == 0) {
							return 72.0f;
						}
						else if (x[6] == 1) {
							return 183.0f;
						}

					}
					else if (x[4] == 1) {
						return 172.0f;
					}

				}
				else if (x[9] == 5) {
					if (x[4] == 0) {
						return 72.0f;
					}
					else if (x[4] == 1) {
						return 110.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[8] == 3) {
						return 172.0f;
					}
					else if (x[8] == 5) {
						return 110.0f;
					}
					else if (x[8] == 6) {
						if (x[11] == 2) {
							return 172.0f;
						}
						else if (x[11] == 3) {
							return 172.0f;
						}
						else if (x[11] == 6) {
							return 110.0f;
						}

					}

				}

			}
			else if (x[10] == 2) {
				if (x[9] == 1) {
					if (x[5] == 0) {
						if (x[6] == 0) {
							return 100.0f;
						}
						else if (x[6] == 1) {
							return 181.0f;
						}

					}
					else if (x[5] == 1) {
						return 151.0f;
					}

				}
				else if (x[9] == 4) {
					return 167.0f;
				}
				else if (x[9] == 6) {
					if (x[4] == 0) {
						return 143.0f;
					}
					else if (x[4] == 1) {
						return 161.0f;
					}

				}

			}
			else if (x[10] == 3) {
				if (x[8] == 1) {
					if (x[5] == 0) {
						if (x[6] == 0) {
							return 160.0f;
						}
						else if (x[6] == 1) {
							return 105.0f;
						}

					}
					else if (x[5] == 1) {
						return 114.0f;
					}

				}
				else if (x[8] == 4) {
					return 113.0f;
				}
				else if (x[8] == 6) {
					return 161.0f;
				}

			}
			else if (x[10] == 5) {
				if (x[8] == 1) {
					if (x[4] == 0) {
						return 73.0f;
					}
					else if (x[4] == 1) {
						return 105.0f;
					}

				}
				else if (x[8] == 4) {
					return 75.0f;
				}
				else if (x[8] == 6) {
					if (x[2] == 0) {
						return 100.0f;
					}
					else if (x[2] == 1) {
						return 181.0f;
					}

				}

			}
			else if (x[10] == 6) {
				if (x[9] == 1) {
					if (x[11] == 2) {
						return 151.0f;
					}
					else if (x[11] == 4) {
						if (x[6] == 0) {
							return 151.0f;
						}
						else if (x[6] == 1) {
							return 75.0f;
						}

					}
					else if (x[11] == 6) {
						if (x[6] == 0) {
							return 75.0f;
						}
						else if (x[6] == 1) {
							return 100.0f;
						}

					}

				}
				else if (x[9] == 2) {
					if (x[5] == 0) {
						return 143.0f;
					}
					else if (x[5] == 1) {
						return 167.0f;
					}

				}
				else if (x[9] == 4) {
					if (x[8] == 1) {
						return 114.0f;
					}
					else if (x[8] == 3) {
						return 113.0f;
					}
					else if (x[8] == 6) {
						return 143.0f;
					}

				}
				else if (x[9] == 5) {
					return 73.0f;
				}
				else if (x[9] == 6) {
					if (x[8] == 1) {
						return 114.0f;
					}
					else if (x[8] == 3) {
						return 113.0f;
					}
					else if (x[8] == 4) {
						return 113.0f;
					}
					else if (x[8] == 6) {
						return 113.0f;
					}

				}

			}

		}

	}
	else if (x[7] == 2) {
		if (x[11] == 0) {
			if (x[10] == 1) {
				if (x[9] == 4) {
					return 24.0f;
				}
				else if (x[9] == 5) {
					return 146.0f;
				}
				else if (x[9] == 6) {
					if (x[4] == 0) {
						return 24.0f;
					}
					else if (x[4] == 1) {
						return 11.0f;
					}

				}

			}
			else if (x[10] == 3) {
				if (x[1] == 0) {
					return 47.0f;
				}
				else if (x[1] == 1) {
					return 11.0f;
				}

			}
			else if (x[10] == 5) {
				if (x[1] == 0) {
					if (x[4] == 0) {
						return 164.0f;
					}
					else if (x[4] == 1) {
						return 179.0f;
					}

				}
				else if (x[1] == 1) {
					return 179.0f;
				}

			}
			else if (x[10] == 6) {
				if (x[9] == 1) {
					return 24.0f;
				}
				else if (x[9] == 4) {
					return 47.0f;
				}
				else if (x[9] == 5) {
					if (x[5] == 0) {
						return 173.0f;
					}
					else if (x[5] == 1) {
						return 95.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[4] == 0) {
						return 24.0f;
					}
					else if (x[4] == 1) {
						return 11.0f;
					}

				}

			}

		}
		else if (x[11] == 1) {
			if (x[10] == 0) {
				if (x[9] == 4) {
					return 25.0f;
				}
				else if (x[9] == 5) {
					return 33.0f;
				}
				else if (x[9] == 6) {
					if (x[4] == 0) {
						return 33.0f;
					}
					else if (x[4] == 1) {
						return 10.0f;
					}

				}

			}
			else if (x[10] == 3) {
				if (x[9] == 0) {
					return 13.0f;
				}
				else if (x[9] == 5) {
					return 31.0f;
				}
				else if (x[9] == 6) {
					return 76.0f;
				}

			}
			else if (x[10] == 5) {
				if (x[9] == 0) {
					return 44.0f;
				}
				else if (x[9] == 4) {
					return 93.0f;
				}
				else if (x[9] == 6) {
					if (x[4] == 0) {
						return 38.0f;
					}
					else if (x[4] == 1) {
						return 123.0f;
					}

				}

			}
			else if (x[10] == 6) {
				if (x[9] == 0) {
					if (x[5] == 0) {
						return 23.0f;
					}
					else if (x[5] == 1) {
						return 12.0f;
					}

				}
				else if (x[9] == 4) {
					return 76.0f;
				}
				else if (x[9] == 5) {
					if (x[5] == 0) {
						return 15.0f;
					}
					else if (x[5] == 1) {
						return 53.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[8] == 3) {
						return 87.0f;
					}
					else if (x[8] == 4) {
						return 87.0f;
					}
					else if (x[8] == 6) {
						return 76.0f;
					}

				}

			}

		}
		else if (x[11] == 3) {
			if (x[10] == 0) {
				if (x[1] == 0) {
					return 81.0f;
				}
				else if (x[1] == 1) {
					return 10.0f;
				}

			}
			else if (x[10] == 1) {
				if (x[9] == 0) {
					return 63.0f;
				}
				else if (x[9] == 4) {
					return 112.0f;
				}
				else if (x[9] == 6) {
					return 150.0f;
				}

			}
			else if (x[10] == 5) {
				if (x[8] == 0) {
					return 106.0f;
				}
				else if (x[8] == 4) {
					return 71.0f;
				}
				else if (x[8] == 6) {
					return 139.0f;
				}

			}
			else if (x[10] == 6) {
				if (x[9] == 0) {
					if (x[5] == 0) {
						return 152.0f;
					}
					else if (x[5] == 1) {
						return 168.0f;
					}

				}
				else if (x[9] == 1) {
					if (x[5] == 0) {
						return 15.0f;
					}
					else if (x[5] == 1) {
						return 57.0f;
					}

				}
				else if (x[9] == 4) {
					if (x[8] == 0) {
						return 176.0f;
					}
					else if (x[8] == 5) {
						return 88.0f;
					}
					else if (x[8] == 6) {
						return 112.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[3] == 0) {
						return 16.0f;
					}
					else if (x[3] == 1) {
						return 176.0f;
					}

				}

			}

		}
		else if (x[11] == 4) {
			if (x[10] == 0) {
				return 43.0f;
			}
			else if (x[10] == 1) {
				if (x[9] == 0) {
					return 12.0f;
				}
				else if (x[9] == 5) {
					return 53.0f;
				}
				else if (x[9] == 6) {
					return 39.0f;
				}

			}
			else if (x[10] == 3) {
				if (x[8] == 0) {
					return 176.0f;
				}
				else if (x[8] == 5) {
					return 88.0f;
				}
				else if (x[8] == 6) {
					if (x[1] == 0) {
						return 27.0f;
					}
					else if (x[1] == 1) {
						return 137.0f;
					}

				}

			}
			else if (x[10] == 6) {
				if (x[8] == 0) {
					if (x[6] == 0) {
						return 176.0f;
					}
					else if (x[6] == 1) {
						return 79.0f;
					}

				}
				else if (x[8] == 3) {
					return 157.0f;
				}
				else if (x[8] == 5) {
					if (x[9] == 0) {
						return 46.0f;
					}
					else if (x[9] == 1) {
						return 111.0f;
					}
					else if (x[9] == 6) {
						return 5.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 23.0f;
					}
					else if (x[9] == 1) {
						return 111.0f;
					}
					else if (x[9] == 5) {
						return 67.0f;
					}
					else if (x[9] == 6) {
						return 27.0f;
					}

				}

			}

		}
		else if (x[11] == 6) {
			if (x[10] == 0) {
				if (x[9] == 1) {
					if (x[6] == 0) {
						return 10.0f;
					}
					else if (x[6] == 1) {
						return 33.0f;
					}

				}
				else if (x[9] == 4) {
					if (x[6] == 0) {
						return 102.0f;
					}
					else if (x[6] == 1) {
						return 182.0f;
					}

				}
				else if (x[9] == 5) {
					if (x[4] == 0) {
						return 33.0f;
					}
					else if (x[4] == 1) {
						return 80.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[8] == 3) {
						return 81.0f;
					}
					else if (x[8] == 5) {
						return 81.0f;
					}
					else if (x[8] == 6) {
						return 10.0f;
					}

				}

			}
			else if (x[10] == 1) {
				if (x[9] == 0) {
					return 44.0f;
				}
				else if (x[9] == 4) {
					if (x[6] == 0) {
						return 9.0f;
					}
					else if (x[6] == 1) {
						return 40.0f;
					}

				}
				else if (x[9] == 5) {
					return 0.0f;
				}
				else if (x[9] == 6) {
					if (x[8] == 3) {
						return 9.0f;
					}
					else if (x[8] == 5) {
						return 5.0f;
					}
					else if (x[8] == 6) {
						return 0.0f;
					}

				}

			}
			else if (x[10] == 3) {
				if (x[8] == 0) {
					return 106.0f;
				}
				else if (x[8] == 4) {
					if (x[6] == 0) {
						return 9.0f;
					}
					else if (x[6] == 1) {
						return 71.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[9] == 0) {
						return 48.0f;
					}
					else if (x[9] == 1) {
						return 70.0f;
					}
					else if (x[9] == 6) {
						return 88.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 48.0f;
					}
					else if (x[9] == 1) {
						return 66.0f;
					}
					else if (x[9] == 5) {
						return 31.0f;
					}
					else if (x[9] == 6) {
						return 66.0f;
					}

				}

			}
			else if (x[10] == 5) {
				if (x[9] == 0) {
					if (x[5] == 0) {
						return 44.0f;
					}
					else if (x[5] == 1) {
						return 46.0f;
					}

				}
				else if (x[9] == 1) {
					return 111.0f;
				}
				else if (x[9] == 4) {
					if (x[8] == 0) {
						return 79.0f;
					}
					else if (x[8] == 3) {
						return 157.0f;
					}
					else if (x[8] == 6) {
						return 93.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[8] == 0) {
						return 79.0f;
					}
					else if (x[8] == 3) {
						return 38.0f;
					}
					else if (x[8] == 4) {
						return 16.0f;
					}
					else if (x[8] == 6) {
						return 16.0f;
					}

				}

			}
			else if (x[10] == 6) {
				if (x[8] == 0) {
					return 79.0f;
				}
				else if (x[8] == 3) {
					if (x[6] == 0) {
						return 9.0f;
					}
					else if (x[6] == 1) {
						return 16.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[9] == 0) {
						return 46.0f;
					}
					else if (x[9] == 1) {
						return 9.0f;
					}
					else if (x[9] == 5) {
						return 53.0f;
					}
					else if (x[9] == 6) {
						return 9.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[9] == 0) {
						return 44.0f;
					}
					else if (x[9] == 1) {
						return 111.0f;
					}
					else if (x[9] == 4) {
						return 88.0f;
					}
					else if (x[9] == 6) {
						return 88.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 12.0f;
					}
					else if (x[9] == 1) {
						return 9.0f;
					}
					else if (x[9] == 4) {
						return 16.0f;
					}
					else if (x[9] == 5) {
						return 16.0f;
					}
					else if (x[9] == 6) {
						return 16.0f;
					}

				}

			}

		}

	}
	else if (x[7] == 3) {
		if (x[11] == 0) {
			if (x[10] == 1) {
				if (x[8] == 4) {
					return 26.0f;
				}
				else if (x[8] == 5) {
					return 97.0f;
				}
				else if (x[8] == 6) {
					if (x[2] == 0) {
						return 26.0f;
					}
					else if (x[2] == 1) {
						return 11.0f;
					}

				}

			}
			else if (x[10] == 2) {
				if (x[5] == 0) {
					return 11.0f;
				}
				else if (x[5] == 1) {
					return 47.0f;
				}

			}
			else if (x[10] == 5) {
				if (x[2] == 0) {
					return 98.0f;
				}
				else if (x[2] == 1) {
					return 179.0f;
				}

			}
			else if (x[10] == 6) {
				if (x[8] == 1) {
					if (x[5] == 0) {
						return 11.0f;
					}
					else if (x[5] == 1) {
						return 26.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[2] == 0) {
						return 26.0f;
					}
					else if (x[2] == 1) {
						return 47.0f;
					}

				}
				else if (x[8] == 5) {
					return 135.0f;
				}
				else if (x[8] == 6) {
					if (x[9] == 2) {
						return 47.0f;
					}
					else if (x[9] == 4) {
						return 47.0f;
					}
					else if (x[9] == 6) {
						return 11.0f;
					}

				}

			}

		}
		else if (x[11] == 1) {
			if (x[8] == 0) {
				if (x[10] == 2) {
					return 99.0f;
				}
				else if (x[10] == 5) {
					return 3.0f;
				}
				else if (x[10] == 6) {
					if (x[5] == 0) {
						return 3.0f;
					}
					else if (x[5] == 1) {
						return 42.0f;
					}

				}

			}
			else if (x[8] == 4) {
				if (x[10] == 0) {
					return 91.0f;
				}
				else if (x[10] == 5) {
					return 124.0f;
				}
				else if (x[10] == 6) {
					return 142.0f;
				}

			}
			else if (x[8] == 5) {
				if (x[10] == 0) {
					return 1.0f;
				}
				else if (x[10] == 2) {
					return 178.0f;
				}
				else if (x[10] == 6) {
					if (x[5] == 0) {
						return 28.0f;
					}
					else if (x[5] == 1) {
						return 170.0f;
					}

				}

			}
			else if (x[8] == 6) {
				if (x[10] == 0) {
					return 10.0f;
				}
				else if (x[10] == 2) {
					if (x[5] == 0) {
						return 87.0f;
					}
					else if (x[5] == 1) {
						return 142.0f;
					}

				}
				else if (x[10] == 5) {
					return 123.0f;
				}
				else if (x[10] == 6) {
					if (x[5] == 0) {
						return 15.0f;
					}
					else if (x[5] == 1) {
						return 17.0f;
					}

				}

			}

		}
		else if (x[11] == 2) {
			if (x[9] == 0) {
				if (x[6] == 0) {
					return 32.0f;
				}
				else if (x[6] == 1) {
					return 148.0f;
				}

			}
			else if (x[9] == 4) {
				if (x[8] == 0) {
					return 129.0f;
				}
				else if (x[8] == 1) {
					return 171.0f;
				}
				else if (x[8] == 6) {
					if (x[6] == 0) {
						return 78.0f;
					}
					else if (x[6] == 1) {
						return 107.0f;
					}

				}

			}
			else if (x[9] == 5) {
				if (x[10] == 0) {
					return 80.0f;
				}
				else if (x[10] == 1) {
					return 0.0f;
				}
				else if (x[10] == 6) {
					return 158.0f;
				}

			}
			else if (x[9] == 6) {
				if (x[10] == 0) {
					if (x[1] == 0) {
						return 81.0f;
					}
					else if (x[1] == 1) {
						return 10.0f;
					}

				}
				else if (x[10] == 1) {
					return 156.0f;
				}
				else if (x[10] == 5) {
					if (x[1] == 0) {
						return 38.0f;
					}
					else if (x[1] == 1) {
						return 175.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[8] == 0) {
						return 174.0f;
					}
					else if (x[8] == 1) {
						return 78.0f;
					}
					else if (x[8] == 4) {
						return 121.0f;
					}
					else if (x[8] == 6) {
						return 78.0f;
					}

				}

			}

		}
		else if (x[11] == 4) {
			if (x[10] == 0) {
				if (x[1] == 0) {
					if (x[2] == 0) {
						return 144.0f;
					}
					else if (x[2] == 1) {
						return 43.0f;
					}

				}
				else if (x[1] == 1) {
					return 43.0f;
				}

			}
			else if (x[10] == 1) {
				if (x[8] == 0) {
					return 42.0f;
				}
				else if (x[8] == 5) {
					return 28.0f;
				}
				else if (x[8] == 6) {
					if (x[2] == 0) {
						return 27.0f;
					}
					else if (x[2] == 1) {
						return 39.0f;
					}

				}

			}
			else if (x[10] == 2) {
				if (x[9] == 0) {
					return 32.0f;
				}
				else if (x[9] == 5) {
					return 158.0f;
				}
				else if (x[9] == 6) {
					return 104.0f;
				}

			}
			else if (x[10] == 6) {
				if (x[8] == 0) {
					return 14.0f;
				}
				else if (x[8] == 1) {
					return 108.0f;
				}
				else if (x[8] == 5) {
					if (x[9] == 0) {
						return 148.0f;
					}
					else if (x[9] == 2) {
						return 92.0f;
					}
					else if (x[9] == 6) {
						return 28.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 32.0f;
					}
					else if (x[9] == 2) {
						return 92.0f;
					}
					else if (x[9] == 5) {
						return 29.0f;
					}
					else if (x[9] == 6) {
						return 29.0f;
					}

				}

			}

		}
		else if (x[11] == 6) {
			if (x[8] == 0) {
				if (x[10] == 1) {
					return 3.0f;
				}
				else if (x[10] == 2) {
					if (x[6] == 0) {
						return 99.0f;
					}
					else if (x[6] == 1) {
						return 59.0f;
					}

				}
				else if (x[10] == 5) {
					if (x[5] == 0) {
						return 3.0f;
					}
					else if (x[5] == 1) {
						return 14.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[6] == 0) {
						return 42.0f;
					}
					else if (x[6] == 1) {
						return 14.0f;
					}

				}

			}
			else if (x[8] == 1) {
				if (x[10] == 0) {
					return 1.0f;
				}
				else if (x[10] == 2) {
					if (x[6] == 0) {
						return 9.0f;
					}
					else if (x[6] == 1) {
						return 109.0f;
					}

				}
				else if (x[10] == 5) {
					if (x[5] == 0) {
						return 35.0f;
					}
					else if (x[5] == 1) {
						return 108.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[9] == 4) {
						return 108.0f;
					}
					else if (x[9] == 5) {
						return 15.0f;
					}
					else if (x[9] == 6) {
						return 9.0f;
					}

				}

			}
			else if (x[8] == 4) {
				if (x[10] == 0) {
					return 149.0f;
				}
				else if (x[10] == 1) {
					if (x[6] == 0) {
						return 9.0f;
					}
					else if (x[6] == 1) {
						return 8.0f;
					}

				}
				else if (x[10] == 5) {
					if (x[9] == 0) {
						return 148.0f;
					}
					else if (x[9] == 2) {
						return 92.0f;
					}
					else if (x[9] == 6) {
						return 124.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[9] == 0) {
						return 74.0f;
					}
					else if (x[9] == 2) {
						return 9.0f;
					}
					else if (x[9] == 5) {
						return 19.0f;
					}
					else if (x[9] == 6) {
						return 9.0f;
					}

				}

			}
			else if (x[8] == 5) {
				if (x[9] == 0) {
					return 148.0f;
				}
				else if (x[9] == 2) {
					if (x[10] == 0) {
						return 80.0f;
					}
					else if (x[10] == 1) {
						return 0.0f;
					}
					else if (x[10] == 6) {
						return 29.0f;
					}

				}
				else if (x[9] == 4) {
					return 107.0f;
				}
				else if (x[9] == 6) {
					if (x[10] == 0) {
						return 81.0f;
					}
					else if (x[10] == 1) {
						return 156.0f;
					}
					else if (x[10] == 2) {
						return 141.0f;
					}
					else if (x[10] == 6) {
						return 15.0f;
					}

				}

			}
			else if (x[8] == 6) {
				if (x[10] == 0) {
					if (x[6] == 0) {
						return 10.0f;
					}
					else if (x[6] == 1) {
						return 1.0f;
					}

				}
				else if (x[10] == 1) {
					if (x[9] == 2) {
						return 0.0f;
					}
					else if (x[9] == 5) {
						return 0.0f;
					}
					else if (x[9] == 6) {
						return 9.0f;
					}

				}
				else if (x[10] == 2) {
					if (x[9] == 0) {
						return 32.0f;
					}
					else if (x[9] == 4) {
						return 9.0f;
					}
					else if (x[9] == 5) {
						return 29.0f;
					}
					else if (x[9] == 6) {
						return 9.0f;
					}

				}
				else if (x[10] == 5) {
					if (x[9] == 0) {
						return 133.0f;
					}
					else if (x[9] == 2) {
						return 92.0f;
					}
					else if (x[9] == 4) {
						return 29.0f;
					}
					else if (x[9] == 6) {
						return 38.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[9] == 0) {
						return 32.0f;
					}
					else if (x[9] == 2) {
						return 9.0f;
					}
					else if (x[9] == 4) {
						return 9.0f;
					}
					else if (x[9] == 5) {
						return 15.0f;
					}
					else if (x[9] == 6) {
						return 9.0f;
					}

				}

			}

		}

	}
	else if (x[7] == 4) {
		if (x[11] == 0) {
			if (x[8] == 1) {
				if (x[9] == 2) {
					return 24.0f;
				}
				else if (x[9] == 5) {
					return 95.0f;
				}
				else if (x[9] == 6) {
					if (x[4] == 0) {
						return 24.0f;
					}
					else if (x[4] == 1) {
						return 26.0f;
					}

				}

			}
			else if (x[8] == 3) {
				if (x[1] == 0) {
					return 47.0f;
				}
				else if (x[1] == 1) {
					return 26.0f;
				}

			}
			else if (x[8] == 5) {
				if (x[1] == 0) {
					if (x[4] == 0) {
						return 162.0f;
					}
					else if (x[4] == 1) {
						return 135.0f;
					}

				}
				else if (x[1] == 1) {
					return 135.0f;
				}

			}
			else if (x[8] == 6) {
				if (x[9] == 1) {
					if (x[2] == 0) {
						return 26.0f;
					}
					else if (x[2] == 1) {
						return 24.0f;
					}

				}
				else if (x[9] == 2) {
					return 47.0f;
				}
				else if (x[9] == 5) {
					if (x[2] == 0) {
						return 173.0f;
					}
					else if (x[2] == 1) {
						return 95.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[4] == 0) {
						return 24.0f;
					}
					else if (x[4] == 1) {
						return 47.0f;
					}

				}

			}

		}
		else if (x[11] == 1) {
			if (x[9] == 0) {
				if (x[8] == 3) {
					return 34.0f;
				}
				else if (x[8] == 5) {
					return 4.0f;
				}
				else if (x[8] == 6) {
					if (x[2] == 0) {
						return 4.0f;
					}
					else if (x[2] == 1) {
						return 23.0f;
					}

				}

			}
			else if (x[9] == 2) {
				if (x[8] == 0) {
					return 163.0f;
				}
				else if (x[8] == 5) {
					return 138.0f;
				}
				else if (x[8] == 6) {
					return 101.0f;
				}

			}
			else if (x[9] == 5) {
				if (x[8] == 0) {
					return 7.0f;
				}
				else if (x[8] == 3) {
					return 18.0f;
				}
				else if (x[8] == 6) {
					if (x[2] == 0) {
						return 17.0f;
					}
					else if (x[2] == 1) {
						return 86.0f;
					}

				}

			}
			else if (x[9] == 6) {
				if (x[8] == 0) {
					return 42.0f;
				}
				else if (x[8] == 3) {
					if (x[2] == 0) {
						return 51.0f;
					}
					else if (x[2] == 1) {
						return 101.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[4] == 0) {
						return 5.0f;
					}
					else if (x[4] == 1) {
						return 170.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[10] == 2) {
						return 101.0f;
					}
					else if (x[10] == 3) {
						return 17.0f;
					}
					else if (x[10] == 6) {
						return 5.0f;
					}

				}

			}

		}
		else if (x[11] == 2) {
			if (x[9] == 0) {
				if (x[1] == 0) {
					return 46.0f;
				}
				else if (x[1] == 1) {
					return 23.0f;
				}

			}
			else if (x[9] == 1) {
				if (x[8] == 0) {
					return 129.0f;
				}
				else if (x[8] == 3) {
					return 89.0f;
				}
				else if (x[8] == 6) {
					return 115.0f;
				}

			}
			else if (x[9] == 5) {
				if (x[10] == 0) {
					return 45.0f;
				}
				else if (x[10] == 3) {
					return 136.0f;
				}
				else if (x[10] == 6) {
					return 131.0f;
				}

			}
			else if (x[9] == 6) {
				if (x[10] == 0) {
					return 68.0f;
				}
				else if (x[10] == 3) {
					if (x[8] == 0) {
						return 129.0f;
					}
					else if (x[8] == 1) {
						return 171.0f;
					}
					else if (x[8] == 6) {
						return 78.0f;
					}

				}
				else if (x[10] == 5) {
					if (x[4] == 0) {
						return 5.0f;
					}
					else if (x[4] == 1) {
						return 159.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[3] == 0) {
						return 78.0f;
					}
					else if (x[3] == 1) {
						return 174.0f;
					}

				}

			}

		}
		else if (x[11] == 3) {
			if (x[8] == 0) {
				if (x[6] == 0) {
					return 42.0f;
				}
				else if (x[6] == 1) {
					return 14.0f;
				}

			}
			else if (x[8] == 1) {
				if (x[9] == 0) {
					return 130.0f;
				}
				else if (x[9] == 2) {
					return 55.0f;
				}
				else if (x[9] == 6) {
					if (x[6] == 0) {
						return 35.0f;
					}
					else if (x[6] == 1) {
						return 52.0f;
					}

				}

			}
			else if (x[8] == 5) {
				if (x[10] == 0) {
					return 128.0f;
				}
				else if (x[10] == 2) {
					return 30.0f;
				}
				else if (x[10] == 6) {
					return 94.0f;
				}

			}
			else if (x[8] == 6) {
				if (x[9] == 0) {
					if (x[2] == 0) {
						return 152.0f;
					}
					else if (x[2] == 1) {
						return 168.0f;
					}

				}
				else if (x[9] == 1) {
					if (x[2] == 0) {
						return 41.0f;
					}
					else if (x[2] == 1) {
						return 57.0f;
					}

				}
				else if (x[9] == 2) {
					if (x[10] == 0) {
						return 68.0f;
					}
					else if (x[10] == 5) {
						return 159.0f;
					}
					else if (x[10] == 6) {
						return 55.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[3] == 0) {
						return 65.0f;
					}
					else if (x[3] == 1) {
						return 68.0f;
					}

				}

			}

		}
		else if (x[11] == 6) {
			if (x[9] == 0) {
				if (x[8] == 1) {
					return 4.0f;
				}
				else if (x[8] == 3) {
					if (x[6] == 0) {
						return 77.0f;
					}
					else if (x[6] == 1) {
						return 34.0f;
					}

				}
				else if (x[8] == 5) {
					return 46.0f;
				}
				else if (x[8] == 6) {
					if (x[10] == 2) {
						return 46.0f;
					}
					else if (x[10] == 5) {
						return 46.0f;
					}
					else if (x[10] == 6) {
						return 4.0f;
					}

				}

			}
			else if (x[9] == 1) {
				if (x[8] == 0) {
					return 7.0f;
				}
				else if (x[8] == 3) {
					if (x[6] == 0) {
						return 9.0f;
					}
					else if (x[6] == 1) {
						return 117.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[2] == 0) {
						return 28.0f;
					}
					else if (x[2] == 1) {
						return 115.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[6] == 0) {
						return 9.0f;
					}
					else if (x[6] == 1) {
						return 17.0f;
					}

				}

			}
			else if (x[9] == 2) {
				if (x[8] == 0) {
					if (x[6] == 0) {
						return 153.0f;
					}
					else if (x[6] == 1) {
						return 163.0f;
					}

				}
				else if (x[8] == 1) {
					if (x[6] == 0) {
						return 9.0f;
					}
					else if (x[6] == 1) {
						return 54.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[10] == 0) {
						return 45.0f;
					}
					else if (x[10] == 3) {
						return 136.0f;
					}
					else if (x[10] == 6) {
						return 138.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[10] == 0) {
						return 45.0f;
					}
					else if (x[10] == 3) {
						return 9.0f;
					}
					else if (x[10] == 5) {
						return 37.0f;
					}
					else if (x[10] == 6) {
						return 37.0f;
					}

				}

			}
			else if (x[9] == 5) {
				if (x[8] == 0) {
					return 14.0f;
				}
				else if (x[8] == 1) {
					return 52.0f;
				}
				else if (x[8] == 3) {
					if (x[10] == 0) {
						return 128.0f;
					}
					else if (x[10] == 2) {
						return 30.0f;
					}
					else if (x[10] == 6) {
						return 51.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[10] == 0) {
						return 45.0f;
					}
					else if (x[10] == 2) {
						return 30.0f;
					}
					else if (x[10] == 3) {
						return 17.0f;
					}
					else if (x[10] == 6) {
						return 17.0f;
					}

				}

			}
			else if (x[9] == 6) {
				if (x[8] == 0) {
					if (x[4] == 0) {
						return 7.0f;
					}
					else if (x[4] == 1) {
						return 42.0f;
					}

				}
				else if (x[8] == 1) {
					if (x[10] == 3) {
						return 35.0f;
					}
					else if (x[10] == 5) {
						return 35.0f;
					}
					else if (x[10] == 6) {
						return 9.0f;
					}

				}
				else if (x[8] == 3) {
					if (x[10] == 0) {
						return 128.0f;
					}
					else if (x[10] == 2) {
						return 9.0f;
					}
					else if (x[10] == 5) {
						return 65.0f;
					}
					else if (x[10] == 6) {
						return 9.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[10] == 0) {
						return 128.0f;
					}
					else if (x[10] == 2) {
						return 65.0f;
					}
					else if (x[10] == 3) {
						return 136.0f;
					}
					else if (x[10] == 6) {
						return 28.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[10] == 0) {
						return 68.0f;
					}
					else if (x[10] == 2) {
						return 9.0f;
					}
					else if (x[10] == 3) {
						return 9.0f;
					}
					else if (x[10] == 5) {
						return 65.0f;
					}
					else if (x[10] == 6) {
						return 9.0f;
					}

				}

			}

		}

	}
	else if (x[7] == 5) {
		if (x[9] == 0) {
			if (x[10] == 1) {
				if (x[8] == 3) {
					return 34.0f;
				}
				else if (x[8] == 4) {
					return 4.0f;
				}
				else if (x[8] == 6) {
					if (x[2] == 0) {
						return 4.0f;
					}
					else if (x[2] == 1) {
						return 44.0f;
					}

				}

			}
			else if (x[10] == 2) {
				if (x[5] == 0) {
					return 44.0f;
				}
				else if (x[5] == 1) {
					return 46.0f;
				}

			}
			else if (x[10] == 3) {
				if (x[2] == 0) {
					return 49.0f;
				}
				else if (x[2] == 1) {
					return 48.0f;
				}

			}
			else if (x[10] == 6) {
				if (x[8] == 1) {
					if (x[5] == 0) {
						return 44.0f;
					}
					else if (x[5] == 1) {
						return 4.0f;
					}

				}
				else if (x[8] == 3) {
					if (x[5] == 0) {
						return 77.0f;
					}
					else if (x[5] == 1) {
						return 34.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[2] == 0) {
						return 4.0f;
					}
					else if (x[2] == 1) {
						return 46.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[2] == 0) {
						return 4.0f;
					}
					else if (x[2] == 1) {
						return 44.0f;
					}

				}

			}

		}
		else if (x[9] == 1) {
			if (x[10] == 0) {
				if (x[8] == 3) {
					return 1.0f;
				}
				else if (x[8] == 4) {
					return 22.0f;
				}
				else if (x[8] == 6) {
					if (x[2] == 0) {
						return 1.0f;
					}
					else if (x[2] == 1) {
						return 33.0f;
					}

				}

			}
			else if (x[10] == 2) {
				if (x[8] == 0) {
					return 59.0f;
				}
				else if (x[8] == 3) {
					return 140.0f;
				}
				else if (x[8] == 6) {
					return 103.0f;
				}

			}
			else if (x[10] == 3) {
				if (x[8] == 0) {
					return 3.0f;
				}
				else if (x[8] == 4) {
					return 132.0f;
				}
				else if (x[8] == 6) {
					return 70.0f;
				}

			}
			else if (x[10] == 6) {
				if (x[8] == 0) {
					return 7.0f;
				}
				else if (x[8] == 3) {
					if (x[5] == 0) {
						return 15.0f;
					}
					else if (x[5] == 1) {
						return 117.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[2] == 0) {
						return 19.0f;
					}
					else if (x[2] == 1) {
						return 103.0f;
					}

				}
				else if (x[8] == 6) {
					return 56.0f;
				}

			}

		}
		else if (x[9] == 2) {
			if (x[8] == 0) {
				if (x[1] == 0) {
					if (x[5] == 0) {
						return 155.0f;
					}
					else if (x[5] == 1) {
						return 163.0f;
					}

				}
				else if (x[1] == 1) {
					return 163.0f;
				}

			}
			else if (x[8] == 1) {
				if (x[10] == 0) {
					return 33.0f;
				}
				else if (x[10] == 3) {
					return 180.0f;
				}
				else if (x[10] == 6) {
					return 54.0f;
				}

			}
			else if (x[8] == 4) {
				if (x[11] == 0) {
					return 125.0f;
				}
				else if (x[11] == 3) {
					return 85.0f;
				}
				else if (x[11] == 6) {
					if (x[1] == 0) {
						return 119.0f;
					}
					else if (x[1] == 1) {
						return 120.0f;
					}

				}

			}
			else if (x[8] == 6) {
				if (x[10] == 0) {
					return 81.0f;
				}
				else if (x[10] == 1) {
					return 122.0f;
				}
				else if (x[10] == 3) {
					if (x[11] == 0) {
						return 169.0f;
					}
					else if (x[11] == 4) {
						return 83.0f;
					}
					else if (x[11] == 6) {
						return 66.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[11] == 0) {
						return 125.0f;
					}
					else if (x[11] == 3) {
						return 15.0f;
					}
					else if (x[11] == 4) {
						return 83.0f;
					}
					else if (x[11] == 6) {
						return 37.0f;
					}

				}

			}

		}
		else if (x[9] == 4) {
			if (x[11] == 0) {
				if (x[4] == 0) {
					return 125.0f;
				}
				else if (x[4] == 1) {
					return 169.0f;
				}

			}
			else if (x[11] == 2) {
				if (x[10] == 0) {
					return 182.0f;
				}
				else if (x[10] == 1) {
					return 40.0f;
				}
				else if (x[10] == 6) {
					return 84.0f;
				}

			}
			else if (x[11] == 3) {
				if (x[8] == 0) {
					return 14.0f;
				}
				else if (x[8] == 1) {
					return 82.0f;
				}
				else if (x[8] == 6) {
					if (x[2] == 0) {
						return 17.0f;
					}
					else if (x[2] == 1) {
						return 85.0f;
					}

				}

			}
			else if (x[11] == 6) {
				if (x[8] == 0) {
					return 7.0f;
				}
				else if (x[8] == 1) {
					if (x[10] == 0) {
						return 64.0f;
					}
					else if (x[10] == 2) {
						return 69.0f;
					}
					else if (x[10] == 6) {
						return 35.0f;
					}

				}
				else if (x[8] == 3) {
					return 116.0f;
				}
				else if (x[8] == 6) {
					if (x[10] == 0) {
						return 102.0f;
					}
					else if (x[10] == 1) {
						return 58.0f;
					}
					else if (x[10] == 2) {
						return 69.0f;
					}
					else if (x[10] == 6) {
						return 17.0f;
					}

				}

			}

		}
		else if (x[9] == 6) {
			if (x[8] == 0) {
				if (x[10] == 1) {
					return 3.0f;
				}
				else if (x[10] == 2) {
					if (x[4] == 0) {
						return 165.0f;
					}
					else if (x[4] == 1) {
						return 59.0f;
					}

				}
				else if (x[10] == 3) {
					if (x[5] == 0) {
						return 3.0f;
					}
					else if (x[5] == 1) {
						return 14.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[11] == 3) {
						return 3.0f;
					}
					else if (x[11] == 4) {
						return 14.0f;
					}
					else if (x[11] == 6) {
						return 7.0f;
					}

				}

			}
			else if (x[8] == 1) {
				if (x[10] == 0) {
					return 1.0f;
				}
				else if (x[10] == 2) {
					if (x[4] == 0) {
						return 5.0f;
					}
					else if (x[4] == 1) {
						return 109.0f;
					}

				}
				else if (x[10] == 3) {
					if (x[5] == 0) {
						return 35.0f;
					}
					else if (x[5] == 1) {
						return 82.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[11] == 3) {
						return 35.0f;
					}
					else if (x[11] == 4) {
						return 5.0f;
					}
					else if (x[11] == 6) {
						return 82.0f;
					}

				}

			}
			else if (x[8] == 3) {
				if (x[10] == 0) {
					if (x[2] == 0) {
						return 81.0f;
					}
					else if (x[2] == 1) {
						return 80.0f;
					}

				}
				else if (x[10] == 1) {
					if (x[2] == 0) {
						return 51.0f;
					}
					else if (x[2] == 1) {
						return 0.0f;
					}

				}
				else if (x[10] == 2) {
					if (x[11] == 0) {
						return 169.0f;
					}
					else if (x[11] == 4) {
						return 83.0f;
					}
					else if (x[11] == 6) {
						return 140.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[11] == 0) {
						return 177.0f;
					}
					else if (x[11] == 2) {
						return 119.0f;
					}
					else if (x[11] == 4) {
						return 51.0f;
					}
					else if (x[11] == 6) {
						return 15.0f;
					}

				}

			}
			else if (x[8] == 4) {
				if (x[10] == 0) {
					if (x[4] == 0) {
						return 22.0f;
					}
					else if (x[4] == 1) {
						return 149.0f;
					}

				}
				else if (x[10] == 1) {
					if (x[4] == 0) {
						return 5.0f;
					}
					else if (x[4] == 1) {
						return 8.0f;
					}

				}
				else if (x[10] == 3) {
					if (x[11] == 0) {
						return 169.0f;
					}
					else if (x[11] == 2) {
						return 84.0f;
					}
					else if (x[11] == 6) {
						return 119.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[11] == 0) {
						return 177.0f;
					}
					else if (x[11] == 2) {
						return 5.0f;
					}
					else if (x[11] == 3) {
						return 85.0f;
					}
					else if (x[11] == 6) {
						return 5.0f;
					}

				}

			}
			else if (x[8] == 6) {
				if (x[11] == 0) {
					if (x[10] == 2) {
						return 145.0f;
					}
					else if (x[10] == 3) {
						return 145.0f;
					}
					else if (x[10] == 6) {
						return 125.0f;
					}

				}
				else if (x[11] == 2) {
					if (x[10] == 0) {
						return 81.0f;
					}
					else if (x[10] == 1) {
						return 5.0f;
					}
					else if (x[10] == 3) {
						return 84.0f;
					}
					else if (x[10] == 6) {
						return 84.0f;
					}

				}
				else if (x[11] == 3) {
					if (x[10] == 0) {
						return 81.0f;
					}
					else if (x[10] == 1) {
						return 17.0f;
					}
					else if (x[10] == 2) {
						return 85.0f;
					}
					else if (x[10] == 6) {
						return 85.0f;
					}

				}
				else if (x[11] == 4) {
					if (x[10] == 2) {
						return 5.0f;
					}
					else if (x[10] == 3) {
						return 17.0f;
					}
					else if (x[10] == 6) {
						return 83.0f;
					}

				}
				else if (x[11] == 6) {
					if (x[10] == 0) {
						return 1.0f;
					}
					else if (x[10] == 1) {
						return 5.0f;
					}
					else if (x[10] == 2) {
						return 5.0f;
					}
					else if (x[10] == 3) {
						return 66.0f;
					}
					else if (x[10] == 6) {
						return 17.0f;
					}

				}

			}

		}

	}
	else if (x[7] == 6) {
		if (x[11] == 0) {
			if (x[10] == 1) {
				if (x[9] == 2) {
					return 24.0f;
				}
				else if (x[9] == 4) {
					if (x[6] == 0) {
						return 26.0f;
					}
					else if (x[6] == 1) {
						return 135.0f;
					}

				}
				else if (x[9] == 5) {
					return 95.0f;
				}
				else if (x[9] == 6) {
					if (x[8] == 3) {
						return 11.0f;
					}
					else if (x[8] == 4) {
						return 26.0f;
					}
					else if (x[8] == 5) {
						return 97.0f;
					}
					else if (x[8] == 6) {
						return 11.0f;
					}

				}

			}
			else if (x[10] == 2) {
				if (x[9] == 1) {
					if (x[4] == 0) {
						return 24.0f;
					}
					else if (x[4] == 1) {
						return 11.0f;
					}

				}
				else if (x[9] == 4) {
					return 24.0f;
				}
				else if (x[9] == 5) {
					if (x[1] == 0) {
						return 146.0f;
					}
					else if (x[1] == 1) {
						return 95.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[1] == 0) {
						return 11.0f;
					}
					else if (x[1] == 1) {
						return 24.0f;
					}

				}

			}
			else if (x[10] == 3) {
				if (x[8] == 1) {
					return 11.0f;
				}
				else if (x[8] == 4) {
					if (x[1] == 0) {
						return 47.0f;
					}
					else if (x[1] == 1) {
						return 26.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[1] == 0) {
						return 162.0f;
					}
					else if (x[1] == 1) {
						return 135.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 1) {
						return 26.0f;
					}
					else if (x[9] == 2) {
						return 47.0f;
					}
					else if (x[9] == 6) {
						return 11.0f;
					}

				}

			}
			else if (x[10] == 5) {
				if (x[8] == 1) {
					if (x[2] == 0) {
						return 134.0f;
					}
					else if (x[2] == 1) {
						return 179.0f;
					}

				}
				else if (x[8] == 3) {
					return 98.0f;
				}
				else if (x[8] == 6) {
					if (x[9] == 1) {
						return 134.0f;
					}
					else if (x[9] == 2) {
						return 134.0f;
					}
					else if (x[9] == 6) {
						return 98.0f;
					}

				}

			}
			else if (x[10] == 6) {
				if (x[8] == 1) {
					if (x[9] == 2) {
						return 24.0f;
					}
					else if (x[9] == 4) {
						return 24.0f;
					}
					else if (x[9] == 5) {
						return 126.0f;
					}
					else if (x[9] == 6) {
						return 11.0f;
					}

				}
				else if (x[8] == 3) {
					if (x[9] == 1) {
						return 11.0f;
					}
					else if (x[9] == 4) {
						return 47.0f;
					}
					else if (x[9] == 6) {
						return 26.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[9] == 1) {
						return 26.0f;
					}
					else if (x[9] == 2) {
						return 47.0f;
					}
					else if (x[9] == 5) {
						return 126.0f;
					}
					else if (x[9] == 6) {
						return 47.0f;
					}

				}
				else if (x[8] == 5) {
					return 127.0f;
				}
				else if (x[8] == 6) {
					if (x[9] == 1) {
						return 26.0f;
					}
					else if (x[9] == 2) {
						return 11.0f;
					}
					else if (x[9] == 4) {
						return 26.0f;
					}
					else if (x[9] == 5) {
						return 126.0f;
					}
					else if (x[9] == 6) {
						return 11.0f;
					}

				}

			}

		}
		else if (x[11] == 1) {
			if (x[8] == 0) {
				if (x[10] == 2) {
					if (x[6] == 0) {
						return 166.0f;
					}
					else if (x[6] == 1) {
						return 59.0f;
					}

				}
				else if (x[10] == 3) {
					return 3.0f;
				}
				else if (x[10] == 5) {
					if (x[9] == 2) {
						return 163.0f;
					}
					else if (x[9] == 4) {
						return 7.0f;
					}
					else if (x[9] == 6) {
						return 3.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[2] == 0) {
						return 7.0f;
					}
					else if (x[2] == 1) {
						return 60.0f;
					}

				}

			}
			else if (x[8] == 3) {
				if (x[9] == 0) {
					if (x[6] == 0) {
						return 154.0f;
					}
					else if (x[6] == 1) {
						return 34.0f;
					}

				}
				else if (x[9] == 4) {
					return 116.0f;
				}
				else if (x[9] == 5) {
					if (x[10] == 0) {
						return 1.0f;
					}
					else if (x[10] == 2) {
						return 140.0f;
					}
					else if (x[10] == 6) {
						return 15.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[10] == 0) {
						return 1.0f;
					}
					else if (x[10] == 2) {
						return 87.0f;
					}
					else if (x[10] == 5) {
						return 51.0f;
					}
					else if (x[10] == 6) {
						return 87.0f;
					}

				}

			}
			else if (x[8] == 4) {
				if (x[9] == 0) {
					return 4.0f;
				}
				else if (x[9] == 2) {
					return 120.0f;
				}
				else if (x[9] == 5) {
					if (x[10] == 0) {
						return 22.0f;
					}
					else if (x[10] == 3) {
						return 132.0f;
					}
					else if (x[10] == 6) {
						return 86.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[10] == 0) {
						return 91.0f;
					}
					else if (x[10] == 3) {
						return 132.0f;
					}
					else if (x[10] == 5) {
						return 5.0f;
					}
					else if (x[10] == 6) {
						return 5.0f;
					}

				}

			}
			else if (x[8] == 5) {
				if (x[9] == 0) {
					if (x[4] == 0) {
						return 44.0f;
					}
					else if (x[4] == 1) {
						return 49.0f;
					}

				}
				else if (x[9] == 2) {
					if (x[10] == 0) {
						return 33.0f;
					}
					else if (x[10] == 3) {
						return 180.0f;
					}
					else if (x[10] == 6) {
						return 37.0f;
					}

				}
				else if (x[9] == 4) {
					if (x[10] == 0) {
						return 64.0f;
					}
					else if (x[10] == 2) {
						return 69.0f;
					}
					else if (x[10] == 6) {
						return 28.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[10] == 0) {
						return 1.0f;
					}
					else if (x[10] == 2) {
						return 5.0f;
					}
					else if (x[10] == 3) {
						return 28.0f;
					}
					else if (x[10] == 6) {
						return 5.0f;
					}

				}

			}
			else if (x[8] == 6) {
				if (x[9] == 0) {
					if (x[10] == 2) {
						return 23.0f;
					}
					else if (x[10] == 3) {
						return 13.0f;
					}
					else if (x[10] == 5) {
						return 4.0f;
					}
					else if (x[10] == 6) {
						return 4.0f;
					}

				}
				else if (x[9] == 2) {
					if (x[10] == 0) {
						return 10.0f;
					}
					else if (x[10] == 3) {
						return 66.0f;
					}
					else if (x[10] == 5) {
						return 123.0f;
					}
					else if (x[10] == 6) {
						return 37.0f;
					}

				}
				else if (x[9] == 4) {
					if (x[3] == 0) {
						return 58.0f;
					}
					else if (x[3] == 1) {
						return 25.0f;
					}

				}
				else if (x[9] == 5) {
					if (x[10] == 0) {
						return 1.0f;
					}
					else if (x[10] == 2) {
						return 86.0f;
					}
					else if (x[10] == 3) {
						return 66.0f;
					}
					else if (x[10] == 6) {
						return 86.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[10] == 0) {
						return 10.0f;
					}
					else if (x[10] == 2) {
						return 5.0f;
					}
					else if (x[10] == 3) {
						return 66.0f;
					}
					else if (x[10] == 5) {
						return 38.0f;
					}
					else if (x[10] == 6) {
						return 17.0f;
					}

				}

			}

		}
		else if (x[11] == 2) {
			if (x[10] == 0) {
				if (x[9] == 1) {
					if (x[4] == 0) {
						return 33.0f;
					}
					else if (x[4] == 1) {
						return 10.0f;
					}

				}
				else if (x[9] == 4) {
					return 25.0f;
				}
				else if (x[9] == 5) {
					return 33.0f;
				}
				else if (x[9] == 6) {
					if (x[1] == 0) {
						return 10.0f;
					}
					else if (x[1] == 1) {
						return 33.0f;
					}

				}

			}
			else if (x[10] == 1) {
				if (x[8] == 0) {
					if (x[5] == 0) {
						return 90.0f;
					}
					else if (x[5] == 1) {
						return 129.0f;
					}

				}
				else if (x[8] == 3) {
					if (x[5] == 0) {
						return 0.0f;
					}
					else if (x[5] == 1) {
						return 89.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[9] == 0) {
						return 23.0f;
					}
					else if (x[9] == 5) {
						return 131.0f;
					}
					else if (x[9] == 6) {
						return 5.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 44.0f;
					}
					else if (x[9] == 4) {
						return 40.0f;
					}
					else if (x[9] == 5) {
						return 0.0f;
					}
					else if (x[9] == 6) {
						return 0.0f;
					}

				}

			}
			else if (x[10] == 3) {
				if (x[8] == 0) {
					return 90.0f;
				}
				else if (x[8] == 1) {
					if (x[9] == 0) {
						return 13.0f;
					}
					else if (x[9] == 5) {
						return 31.0f;
					}
					else if (x[9] == 6) {
						return 78.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[1] == 0) {
						return 78.0f;
					}
					else if (x[1] == 1) {
						return 121.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 13.0f;
					}
					else if (x[9] == 1) {
						return 70.0f;
					}
					else if (x[9] == 5) {
						return 2.0f;
					}
					else if (x[9] == 6) {
						return 2.0f;
					}

				}

			}
			else if (x[10] == 5) {
				if (x[9] == 0) {
					if (x[1] == 0) {
						return 46.0f;
					}
					else if (x[1] == 1) {
						return 44.0f;
					}

				}
				else if (x[9] == 1) {
					if (x[4] == 0) {
						return 38.0f;
					}
					else if (x[4] == 1) {
						return 175.0f;
					}

				}
				else if (x[9] == 4) {
					if (x[1] == 0) {
						return 2.0f;
					}
					else if (x[1] == 1) {
						return 93.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[1] == 0) {
						return 2.0f;
					}
					else if (x[1] == 1) {
						return 38.0f;
					}

				}

			}
			else if (x[10] == 6) {
				if (x[8] == 0) {
					return 118.0f;
				}
				else if (x[8] == 1) {
					if (x[9] == 0) {
						return 23.0f;
					}
					else if (x[9] == 4) {
						return 78.0f;
					}
					else if (x[9] == 5) {
						return 15.0f;
					}
					else if (x[9] == 6) {
						return 78.0f;
					}

				}
				else if (x[8] == 3) {
					if (x[9] == 1) {
						return 78.0f;
					}
					else if (x[9] == 4) {
						return 78.0f;
					}
					else if (x[9] == 6) {
						return 2.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[9] == 0) {
						return 46.0f;
					}
					else if (x[9] == 1) {
						return 121.0f;
					}
					else if (x[9] == 5) {
						return 2.0f;
					}
					else if (x[9] == 6) {
						return 78.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 12.0f;
					}
					else if (x[9] == 1) {
						return 56.0f;
					}
					else if (x[9] == 4) {
						return 2.0f;
					}
					else if (x[9] == 5) {
						return 2.0f;
					}
					else if (x[9] == 6) {
						return 2.0f;
					}

				}

			}

		}
		else if (x[11] == 3) {
			if (x[8] == 0) {
				if (x[10] == 1) {
					return 42.0f;
				}
				else if (x[10] == 2) {
					return 99.0f;
				}
				else if (x[10] == 5) {
					return 3.0f;
				}
				else if (x[10] == 6) {
					if (x[9] == 1) {
						return 42.0f;
					}
					else if (x[9] == 4) {
						return 14.0f;
					}
					else if (x[9] == 6) {
						return 3.0f;
					}

				}

			}
			else if (x[8] == 1) {
				if (x[9] == 0) {
					if (x[2] == 0) {
						return 130.0f;
					}
					else if (x[2] == 1) {
						return 63.0f;
					}

				}
				else if (x[9] == 2) {
					if (x[10] == 0) {
						return 10.0f;
					}
					else if (x[10] == 5) {
						return 139.0f;
					}
					else if (x[10] == 6) {
						return 15.0f;
					}

				}
				else if (x[9] == 4) {
					return 112.0f;
				}
				else if (x[9] == 6) {
					if (x[10] == 0) {
						return 1.0f;
					}
					else if (x[10] == 2) {
						return 109.0f;
					}
					else if (x[10] == 5) {
						return 35.0f;
					}
					else if (x[10] == 6) {
						return 35.0f;
					}

				}

			}
			else if (x[8] == 4) {
				if (x[9] == 0) {
					return 130.0f;
				}
				else if (x[9] == 1) {
					if (x[10] == 0) {
						return 91.0f;
					}
					else if (x[10] == 5) {
						return 124.0f;
					}
					else if (x[10] == 6) {
						return 41.0f;
					}

				}
				else if (x[9] == 2) {
					if (x[1] == 0) {
						return 2.0f;
					}
					else if (x[1] == 1) {
						return 55.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[10] == 0) {
						return 91.0f;
					}
					else if (x[10] == 1) {
						return 41.0f;
					}
					else if (x[10] == 5) {
						return 2.0f;
					}
					else if (x[10] == 6) {
						return 2.0f;
					}

				}

			}
			else if (x[8] == 5) {
				if (x[10] == 0) {
					return 1.0f;
				}
				else if (x[10] == 1) {
					if (x[5] == 0) {
						return 0.0f;
					}
					else if (x[5] == 1) {
						return 94.0f;
					}

				}
				else if (x[10] == 2) {
					if (x[1] == 0) {
						return 2.0f;
					}
					else if (x[1] == 1) {
						return 178.0f;
					}

				}
				else if (x[10] == 6) {
					if (x[1] == 0) {
						return 28.0f;
					}
					else if (x[1] == 1) {
						return 15.0f;
					}

				}

			}
			else if (x[8] == 6) {
				if (x[9] == 0) {
					return 63.0f;
				}
				else if (x[9] == 1) {
					if (x[10] == 0) {
						return 1.0f;
					}
					else if (x[10] == 2) {
						return 57.0f;
					}
					else if (x[10] == 5) {
						return 38.0f;
					}
					else if (x[10] == 6) {
						return 57.0f;
					}

				}
				else if (x[9] == 2) {
					if (x[10] == 0) {
						return 10.0f;
					}
					else if (x[10] == 1) {
						return 0.0f;
					}
					else if (x[10] == 5) {
						return 2.0f;
					}
					else if (x[10] == 6) {
						return 55.0f;
					}

				}
				else if (x[9] == 4) {
					if (x[1] == 0) {
						return 2.0f;
					}
					else if (x[1] == 1) {
						return 41.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[10] == 0) {
						return 10.0f;
					}
					else if (x[10] == 1) {
						return 0.0f;
					}
					else if (x[10] == 2) {
						return 2.0f;
					}
					else if (x[10] == 5) {
						return 2.0f;
					}
					else if (x[10] == 6) {
						return 17.0f;
					}

				}

			}

		}
		else if (x[11] == 4) {
			if (x[8] == 0) {
				if (x[9] == 1) {
					if (x[4] == 0) {
						return 7.0f;
					}
					else if (x[4] == 1) {
						return 42.0f;
					}

				}
				else if (x[9] == 2) {
					if (x[1] == 0) {
						return 60.0f;
					}
					else if (x[1] == 1) {
						return 163.0f;
					}

				}
				else if (x[9] == 5) {
					return 7.0f;
				}
				else if (x[9] == 6) {
					if (x[10] == 1) {
						return 42.0f;
					}
					else if (x[10] == 3) {
						return 14.0f;
					}
					else if (x[10] == 6) {
						return 7.0f;
					}

				}

			}
			else if (x[8] == 1) {
				if (x[10] == 0) {
					if (x[2] == 0) {
						return 96.0f;
					}
					else if (x[2] == 1) {
						return 43.0f;
					}

				}
				else if (x[10] == 2) {
					if (x[9] == 0) {
						return 12.0f;
					}
					else if (x[9] == 5) {
						return 53.0f;
					}
					else if (x[9] == 6) {
						return 27.0f;
					}

				}
				else if (x[10] == 3) {
					return 137.0f;
				}
				else if (x[10] == 6) {
					if (x[9] == 0) {
						return 23.0f;
					}
					else if (x[9] == 2) {
						return 27.0f;
					}
					else if (x[9] == 5) {
						return 67.0f;
					}
					else if (x[9] == 6) {
						return 35.0f;
					}

				}

			}
			else if (x[8] == 3) {
				if (x[9] == 0) {
					return 154.0f;
				}
				else if (x[9] == 1) {
					if (x[10] == 0) {
						return 43.0f;
					}
					else if (x[10] == 2) {
						return 104.0f;
					}
					else if (x[10] == 6) {
						return 117.0f;
					}

				}
				else if (x[9] == 5) {
					if (x[1] == 0) {
						return 2.0f;
					}
					else if (x[1] == 1) {
						return 51.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[10] == 0) {
						return 96.0f;
					}
					else if (x[10] == 1) {
						return 51.0f;
					}
					else if (x[10] == 2) {
						return 2.0f;
					}
					else if (x[10] == 6) {
						return 27.0f;
					}

				}

			}
			else if (x[8] == 5) {
				if (x[9] == 0) {
					if (x[1] == 0) {
						return 46.0f;
					}
					else if (x[1] == 1) {
						return 4.0f;
					}

				}
				else if (x[9] == 1) {
					if (x[4] == 0) {
						return 28.0f;
					}
					else if (x[4] == 1) {
						return 147.0f;
					}

				}
				else if (x[9] == 2) {
					if (x[1] == 0) {
						return 37.0f;
					}
					else if (x[1] == 1) {
						return 138.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[10] == 1) {
						return 5.0f;
					}
					else if (x[10] == 3) {
						return 28.0f;
					}
					else if (x[10] == 6) {
						return 2.0f;
					}

				}

			}
			else if (x[8] == 6) {
				if (x[9] == 0) {
					if (x[2] == 0) {
						return 4.0f;
					}
					else if (x[2] == 1) {
						return 23.0f;
					}

				}
				else if (x[9] == 1) {
					if (x[3] == 0) {
						return 27.0f;
					}
					else if (x[3] == 1) {
						return 62.0f;
					}

				}
				else if (x[9] == 2) {
					if (x[10] == 0) {
						return 62.0f;
					}
					else if (x[10] == 1) {
						return 39.0f;
					}
					else if (x[10] == 3) {
						return 27.0f;
					}
					else if (x[10] == 6) {
						return 37.0f;
					}

				}
				else if (x[9] == 5) {
					if (x[2] == 0) {
						return 67.0f;
					}
					else if (x[2] == 1) {
						return 2.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[10] == 0) {
						return 43.0f;
					}
					else if (x[10] == 1) {
						return 27.0f;
					}
					else if (x[10] == 2) {
						return 27.0f;
					}
					else if (x[10] == 3) {
						return 27.0f;
					}
					else if (x[10] == 6) {
						return 17.0f;
					}

				}

			}

		}
		else if (x[11] == 6) {
			if (x[10] == 0) {
				if (x[8] == 1) {
					if (x[9] == 2) {
						return 10.0f;
					}
					else if (x[9] == 4) {
						return 25.0f;
					}
					else if (x[9] == 5) {
						return 1.0f;
					}
					else if (x[9] == 6) {
						return 1.0f;
					}

				}
				else if (x[8] == 3) {
					if (x[9] == 1) {
						return 1.0f;
					}
					else if (x[9] == 5) {
						return 1.0f;
					}
					else if (x[9] == 6) {
						return 10.0f;
					}

				}
				else if (x[8] == 4) {
					return 22.0f;
				}
				else if (x[8] == 5) {
					if (x[9] == 1) {
						return 1.0f;
					}
					else if (x[9] == 2) {
						return 33.0f;
					}
					else if (x[9] == 4) {
						return 64.0f;
					}
					else if (x[9] == 6) {
						return 1.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 1) {
						return 10.0f;
					}
					else if (x[9] == 2) {
						return 10.0f;
					}
					else if (x[9] == 4) {
						return 25.0f;
					}
					else if (x[9] == 5) {
						return 1.0f;
					}
					else if (x[9] == 6) {
						return 10.0f;
					}

				}

			}
			else if (x[10] == 1) {
				if (x[8] == 0) {
					if (x[9] == 2) {
						return 60.0f;
					}
					else if (x[9] == 4) {
						return 7.0f;
					}
					else if (x[9] == 5) {
						return 3.0f;
					}
					else if (x[9] == 6) {
						return 3.0f;
					}

				}
				else if (x[8] == 3) {
					if (x[9] == 0) {
						return 21.0f;
					}
					else if (x[9] == 4) {
						return 9.0f;
					}
					else if (x[9] == 5) {
						return 0.0f;
					}
					else if (x[9] == 6) {
						return 0.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[9] == 0) {
						return 23.0f;
					}
					else if (x[9] == 2) {
						return 37.0f;
					}
					else if (x[9] == 5) {
						return 8.0f;
					}
					else if (x[9] == 6) {
						return 9.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[9] == 0) {
						return 4.0f;
					}
					else if (x[9] == 2) {
						return 0.0f;
					}
					else if (x[9] == 4) {
						return 28.0f;
					}
					else if (x[9] == 6) {
						return 28.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 4.0f;
					}
					else if (x[9] == 2) {
						return 0.0f;
					}
					else if (x[9] == 4) {
						return 9.0f;
					}
					else if (x[9] == 5) {
						return 0.0f;
					}
					else if (x[9] == 6) {
						return 5.0f;
					}

				}

			}
			else if (x[10] == 2) {
				if (x[8] == 0) {
					if (x[6] == 0) {
						return 99.0f;
					}
					else if (x[6] == 1) {
						return 59.0f;
					}

				}
				else if (x[8] == 1) {
					if (x[9] == 0) {
						return 44.0f;
					}
					else if (x[9] == 4) {
						return 9.0f;
					}
					else if (x[9] == 5) {
						return 53.0f;
					}
					else if (x[9] == 6) {
						return 9.0f;
					}

				}
				else if (x[8] == 3) {
					if (x[1] == 0) {
						return 2.0f;
					}
					else if (x[1] == 1) {
						return 9.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[9] == 0) {
						return 44.0f;
					}
					else if (x[9] == 1) {
						return 56.0f;
					}
					else if (x[9] == 4) {
						return 2.0f;
					}
					else if (x[9] == 6) {
						return 2.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 12.0f;
					}
					else if (x[9] == 1) {
						return 9.0f;
					}
					else if (x[9] == 4) {
						return 2.0f;
					}
					else if (x[9] == 5) {
						return 2.0f;
					}
					else if (x[9] == 6) {
						return 2.0f;
					}

				}

			}
			else if (x[10] == 3) {
				if (x[8] == 0) {
					if (x[9] == 1) {
						return 3.0f;
					}
					else if (x[9] == 5) {
						return 14.0f;
					}
					else if (x[9] == 6) {
						return 42.0f;
					}

				}
				else if (x[8] == 1) {
					if (x[9] == 0) {
						return 49.0f;
					}
					else if (x[9] == 2) {
						return 66.0f;
					}
					else if (x[9] == 5) {
						return 31.0f;
					}
					else if (x[9] == 6) {
						return 66.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[1] == 0) {
						return 2.0f;
					}
					else if (x[1] == 1) {
						return 9.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[9] == 0) {
						return 48.0f;
					}
					else if (x[9] == 1) {
						return 28.0f;
					}
					else if (x[9] == 2) {
						return 2.0f;
					}
					else if (x[9] == 6) {
						return 28.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 13.0f;
					}
					else if (x[9] == 1) {
						return 9.0f;
					}
					else if (x[9] == 2) {
						return 2.0f;
					}
					else if (x[9] == 5) {
						return 2.0f;
					}
					else if (x[9] == 6) {
						return 2.0f;
					}

				}

			}
			else if (x[10] == 5) {
				if (x[9] == 0) {
					if (x[4] == 0) {
						return 4.0f;
					}
					else if (x[4] == 1) {
						return 77.0f;
					}

				}
				else if (x[9] == 1) {
					if (x[8] == 0) {
						return 7.0f;
					}
					else if (x[8] == 3) {
						return 38.0f;
					}
					else if (x[8] == 4) {
						return 124.0f;
					}
					else if (x[8] == 6) {
						return 38.0f;
					}

				}
				else if (x[9] == 2) {
					if (x[8] == 0) {
						return 155.0f;
					}
					else if (x[8] == 1) {
						return 54.0f;
					}
					else if (x[8] == 4) {
						return 2.0f;
					}
					else if (x[8] == 6) {
						return 38.0f;
					}

				}
				else if (x[9] == 4) {
					if (x[8] == 0) {
						return 7.0f;
					}
					else if (x[8] == 1) {
						return 35.0f;
					}
					else if (x[8] == 3) {
						return 2.0f;
					}
					else if (x[8] == 6) {
						return 2.0f;
					}

				}
				else if (x[9] == 6) {
					if (x[8] == 0) {
						return 3.0f;
					}
					else if (x[8] == 1) {
						return 35.0f;
					}
					else if (x[8] == 3) {
						return 51.0f;
					}
					else if (x[8] == 4) {
						return 2.0f;
					}
					else if (x[8] == 6) {
						return 17.0f;
					}

				}

			}
			else if (x[10] == 6) {
				if (x[8] == 0) {
					if (x[2] == 0) {
						return 7.0f;
					}
					else if (x[2] == 1) {
						return 60.0f;
					}

				}
				else if (x[8] == 1) {
					if (x[9] == 0) {
						return 4.0f;
					}
					else if (x[9] == 2) {
						return 54.0f;
					}
					else if (x[9] == 4) {
						return 9.0f;
					}
					else if (x[9] == 5) {
						return 15.0f;
					}
					else if (x[9] == 6) {
						return 35.0f;
					}

				}
				else if (x[8] == 3) {
					if (x[9] == 0) {
						return 34.0f;
					}
					else if (x[9] == 1) {
						return 9.0f;
					}
					else if (x[9] == 4) {
						return 51.0f;
					}
					else if (x[9] == 5) {
						return 18.0f;
					}
					else if (x[9] == 6) {
						return 9.0f;
					}

				}
				else if (x[8] == 4) {
					if (x[9] == 0) {
						return 4.0f;
					}
					else if (x[9] == 1) {
						return 9.0f;
					}
					else if (x[9] == 2) {
						return 2.0f;
					}
					else if (x[9] == 5) {
						return 19.0f;
					}
					else if (x[9] == 6) {
						return 2.0f;
					}

				}
				else if (x[8] == 5) {
					if (x[9] == 0) {
						return 4.0f;
					}
					else if (x[9] == 1) {
						return 28.0f;
					}
					else if (x[9] == 2) {
						return 2.0f;
					}
					else if (x[9] == 4) {
						return 28.0f;
					}
					else if (x[9] == 6) {
						return 28.0f;
					}

				}
				else if (x[8] == 6) {
					if (x[9] == 0) {
						return 4.0f;
					}
					else if (x[9] == 1) {
						return 9.0f;
					}
					else if (x[9] == 2) {
						return 9.0f;
					}
					else if (x[9] == 4) {
						return 9.0f;
					}
					else if (x[9] == 5) {
						return 2.0f;
					}
					else if (x[9] == 6) {
						return 2.0f;
					}

				}

			}

		}

	}

}
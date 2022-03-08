#include <stdio.h>

float classify(const float x[]);

int main() {
    float x[] = {3.12f,-0.9f};
    float result = classify(x);
    return 0;
}

float classify(const float x[]) {
	if (-0.198075756*x[0]-0.178356871*x[1]+0.525857091 <= 0) {
		if (0.139542907*x[0]+0.123436563*x[1]-0.500355721 <= 0) {
			if (x[1] <= -0.75) {
				if (x[0] <= 3.64) {
					if (x[0] <= 3.56) {
						if (x[0] <= 3.48) {
							return 0.0f;
						}
						else {
							if (x[1] <= -0.85) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}

					}
					else {
						if (x[1] <= -0.85) {
							return 0.0f;
						}
						else {
							return 0.0f;
						}

					}

				}
				else {
					if (x[1] <= -0.85) {
						if (x[0] <= 3.8) {
							if (x[0] <= 3.72) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}
						else {
							return 0.0f;
						}

					}
					else {
						if (x[0] <= 3.8) {
							if (x[0] <= 3.72) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}
						else {
							return 0.0f;
						}

					}

				}

			}
			else {
				if (x[1] <= 0.75) {
					return 0.0f;
				}
				else {
					if (x[0] <= 2.6) {
						if (x[1] <= 0.85) {
							if (x[0] <= 2.52) {
								if (x[0] <= 2.44) {
									return 0.0f;
								}
								else {
									return 0.0f;
								}

							}
							else {
								return 0.0f;
							}

						}
						else {
							if (x[0] <= 2.52) {
								if (x[0] <= 2.44) {
									return 0.0f;
								}
								else {
									return 0.0f;
								}

							}
							else {
								return 0.0f;
							}

						}

					}
					else {
						if (x[0] <= 2.68) {
							if (x[1] <= 0.85) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}
						else {
							if (x[0] <= 2.76) {
								if (x[1] <= 0.85) {
									return 0.0f;
								}
								else {
									return 0.0f;
								}

							}
							else {
								return 0.0f;
							}

						}

					}

				}

			}

		}
		else {
			if (-0.0159026608*x[0]-0.0144778928*x[1]+0.0596580654 <= 0) {
				if (x[0] <= 3.4) {
					if (-0.035286136*x[0]-0.0838496014*x[1]+0.174394101 <= 0) {
						if (-0.118875638*x[0]-0.100888185*x[1]+0.456879556 <= 0) {
							if (x[0] <= 3.24) {
								return -2.2f;
							}
							else {
								return -2.4f;
							}

						}
						else {
							if (x[0] <= 3.08) {
								if (x[0] <= 3.0) {
									return 0.0f;
								}
								else {
									return 0.0f;
								}

							}
							else {
								return -0.1f;
							}

						}

					}
					else {
						if (-0.221866965*x[0]-0.226635754*x[1]+0.861024499 <= 0) {
							if (x[0] <= 3.32) {
								return -0.2f;
							}
							else {
								return -2.5f;
							}

						}
						else {
							if (x[0] <= 3.24) {
								return 0.0f;
							}
							else {
								return -0.3f;
							}

						}

					}

				}
				else {
					if (x[0] <= 3.64) {
						if (x[1] <= 0.35) {
							if (x[0] <= 3.56) {
								return -0.5f;
							}
							else {
								if (x[1] <= 0.25) {
									return -0.6f;
								}
								else {
									return -3.0f;
								}

							}

						}
						else {
							if (x[0] <= 3.48) {
								if (x[1] <= 0.45) {
									return -0.4f;
								}
								else {
									return -2.6f;
								}

							}
							else {
								return -2.8f;
							}

						}

					}
					else {
						if (x[0] <= 3.72) {
							if (x[1] <= 0.15) {
								return -0.7f;
							}
							else {
								return -3.2f;
							}

						}
						else {
							if (x[0] <= 3.8) {
								if (x[1] <= 0.05) {
									return -0.9f;
								}
								else {
									return -3.4f;
								}

							}
							else {
								return -3.7f;
							}

						}

					}

				}

			}
			else {
				if (-0.0428502858*x[0]-0.657689273*x[1]+0.530020416 <= 0) {
					if (x[0] <= 2.92) {
						if (x[1] <= 0.85) {
							return 0.0f;
						}
						else {
							return 0.0f;
						}

					}
					else {
						if (x[0] <= 3.12) {
							if (x[0] <= 3.0) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}
						else {
							return 0.0f;
						}

					}

				}
				else {
					if (x[1] <= 0.35) {
						if (-0.22388041*x[0]-0.204957485*x[1]+0.820033014 <= 0) {
							return 0.0f;
						}
						else {
							if (x[0] <= 3.64) {
								if (x[0] <= 3.48) {
									return 0.0f;
								}
								else {
									return 0.0f;
								}

							}
							else {
								if (x[0] <= 3.76) {
									return 0.0f;
								}
								else {
									return 0.0f;
								}

							}

						}

					}
					else {
						if (-0.121169709*x[0]-0.13482812*x[1]+0.456879556 <= 0) {
							if (x[0] <= 3.2) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}
						else {
							return 0.0f;
						}

					}

				}

			}

		}

	}
	else {
		if (-0.26559937*x[0]-0.224202901*x[1]+0.659241915 <= 0) {
			if (x[1] <= -0.65) {
				if (-0.158746734*x[0]+0.285971522*x[1]+0.743038297 <= 0) {
					if (x[0] <= 3.32) {
						if (x[1] <= -0.85) {
							return 0.0f;
						}
						else {
							return 0.0f;
						}

					}
					else {
						if (x[0] <= 3.4) {
							if (x[1] <= -0.85) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}
						else {
							return 0.0f;
						}

					}

				}
				else {
					if (x[0] <= 3.24) {
						if (x[0] <= 3.16) {
							return 0.0f;
						}
						else {
							if (x[1] <= -0.75) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}

					}
					else {
						return 0.0f;
					}

				}

			}
			else {
				if (-0.346818835*x[0]-0.290582836*x[1]+0.889781654 <= 0) {
					if (x[0] <= 2.6) {
						if (x[0] <= 2.48) {
							return 0.0f;
						}
						else {
							return 0.0f;
						}

					}
					else {
						if (x[0] <= 3.0) {
							if (x[0] <= 2.76) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}
						else {
							return 0.0f;
						}

					}

				}
				else {
					if (x[0] <= 2.92) {
						return 0.0f;
					}
					else {
						return 0.0f;
					}

				}

			}

		}
		else {
			if (x[1] <= -0.45) {
				if (x[0] <= 3.0) {
					if (x[0] <= 2.92) {
						if (x[0] <= 2.84) {
							return 2.7f;
						}
						else {
							if (x[1] <= -0.55) {
								return 2.5f;
							}
							else {
								return 0.4f;
							}

						}

					}
					else {
						if (x[1] <= -0.65) {
							return 2.4f;
						}
						else {
							return 0.3f;
						}

					}

				}
				else {
					if (x[0] <= 3.08) {
						if (x[1] <= -0.75) {
							return 2.3f;
						}
						else {
							return 0.2f;
						}

					}
					else {
						if (x[0] <= 3.16) {
							if (x[1] <= -0.85) {
								return 2.2f;
							}
							else {
								return 0.1f;
							}

						}
						else {
							return 0.0f;
						}

					}

				}

			}
			else {
				if (x[0] <= 2.6) {
					if (x[0] <= 2.52) {
						if (x[0] <= 2.44) {
							return 3.9f;
						}
						else {
							if (x[1] <= -0.05) {
								return 3.6f;
							}
							else {
								return 0.9f;
							}

						}

					}
					else {
						if (x[1] <= -0.15) {
							return 3.3f;
						}
						else {
							return 0.8f;
						}

					}

				}
				else {
					if (x[0] <= 2.68) {
						if (x[1] <= -0.25) {
							return 3.1f;
						}
						else {
							return 0.7f;
						}

					}
					else {
						if (x[0] <= 2.76) {
							if (x[1] <= -0.35) {
								return 2.9f;
							}
							else {
								return 0.6f;
							}

						}
						else {
							return 0.5f;
						}

					}

				}

			}

		}

	}

}
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
				if (x[1] <= -0.65) {
					if (x[0] <= 3.08) {
						if (x[0] <= 3.0) {
							return 2.4f;
						}
						else {
							if (x[1] <= -0.75) {
								return 2.3f;
							}
							else {
								return 0.2f;
							}

						}

					}
					else {
						if (x[1] <= -0.85) {
							return 2.2f;
						}
						else {
							if (x[1] <= -0.75) {
								return 0.1f;
							}
							else {
								return 0.0f;
							}

						}

					}

				}
				else {
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
						if (x[0] <= 3.0) {
							if (x[1] <= -0.55) {
								return 0.3f;
							}
							else {
								return 0.0f;
							}

						}
						else {
							if (x[0] <= 3.08) {
								if (x[1] <= -0.55) {
									return 0.0f;
								}
								else {
									return 0.0f;
								}

							}
							else {
								if (x[1] <= -0.55) {
									return 0.0f;
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
				if (x[1] <= 0.15) {
					if (x[0] <= 2.76) {
						if (x[0] <= 2.6) {
							if (x[1] <= -0.05) {
								if (x[0] <= 2.52) {
									return 3.6f;
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
								if (x[1] <= 0.05) {
									if (x[0] <= 2.44) {
										return 3.9f;
									}
									else {
										if (x[0] <= 2.52) {
											return 0.9f;
										}
										else {
											return 0.0f;
										}

									}

								}
								else {
									if (x[0] <= 2.52) {
										return 0.0f;
									}
									else {
										return 0.0f;
									}

								}

							}

						}
						else {
							if (x[1] <= -0.25) {
								if (x[0] <= 2.68) {
									return 3.1f;
								}
								else {
									if (x[1] <= -0.35) {
										return 2.9f;
									}
									else {
										return 0.6f;
									}

								}

							}
							else {
								if (x[1] <= -0.05) {
									if (x[0] <= 2.68) {
										if (x[1] <= -0.15) {
											return 0.7f;
										}
										else {
											return 0.0f;
										}

									}
									else {
										if (x[1] <= -0.15) {
											return 0.0f;
										}
										else {
											return 0.0f;
										}

									}

								}
								else {
									if (x[0] <= 2.68) {
										if (x[1] <= 0.05) {
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
					else {
						if (x[1] <= -0.15) {
							if (x[0] <= 2.92) {
								if (x[1] <= -0.35) {
									if (x[0] <= 2.84) {
										return 0.5f;
									}
									else {
										return 0.0f;
									}

								}
								else {
									if (x[0] <= 2.84) {
										if (x[1] <= -0.25) {
											return 0.0f;
										}
										else {
											return 0.0f;
										}

									}
									else {
										if (x[1] <= -0.25) {
											return 0.0f;
										}
										else {
											return 0.0f;
										}

									}

								}

							}
							else {
								if (x[0] <= 3.0) {
									if (x[1] <= -0.35) {
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
							return 0.0f;
						}

					}

				}
				else {
					if (x[0] <= 3.0) {
						return 0.0f;
					}
					else {
						if (x[1] <= 0.65) {
							if (x[1] <= 0.55) {
								return 0.0f;
							}
							else {
								if (x[0] <= 3.08) {
									return 0.0f;
								}
								else {
									return 0.0f;
								}

							}

						}
						else {
							if (x[0] <= 3.08) {
								return 0.0f;
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
			if (x[0] <= 2.76) {
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
						if (x[0] <= 2.6) {
							return 0.0f;
						}
						else {
							if (x[0] <= 2.68) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}

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
						if (x[0] <= 2.6) {
							return 0.0f;
						}
						else {
							if (x[0] <= 2.68) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}

					}

				}

			}
			else {
				if (x[1] <= 0.85) {
					if (x[0] <= 2.92) {
						if (x[0] <= 2.84) {
							return 0.0f;
						}
						else {
							return 0.0f;
						}

					}
					else {
						if (x[0] <= 3.0) {
							return 0.0f;
						}
						else {
							if (x[0] <= 3.08) {
								return 0.0f;
							}
							else {
								return -0.1f;
							}

						}

					}

				}
				else {
					if (x[0] <= 2.92) {
						return 0.0f;
					}
					else {
						if (x[0] <= 3.0) {
							return 0.0f;
						}
						else {
							if (x[0] <= 3.08) {
								return 0.0f;
							}
							else {
								return -2.2f;
							}

						}

					}

				}

			}

		}

	}
	else {
		if (x[1] <= -0.75) {
			if (x[1] <= -0.85) {
				if (x[0] <= 3.48) {
					if (x[0] <= 3.32) {
						return 0.0f;
					}
					else {
						if (x[0] <= 3.4) {
							return 0.0f;
						}
						else {
							return 0.0f;
						}

					}

				}
				else {
					if (x[0] <= 3.64) {
						if (x[0] <= 3.56) {
							return 0.0f;
						}
						else {
							return 0.0f;
						}

					}
					else {
						if (x[0] <= 3.72) {
							return 0.0f;
						}
						else {
							if (x[0] <= 3.8) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}

					}

				}

			}
			else {
				if (x[0] <= 3.48) {
					if (x[0] <= 3.32) {
						if (x[0] <= 3.24) {
							return 0.0f;
						}
						else {
							return 0.0f;
						}

					}
					else {
						if (x[0] <= 3.4) {
							return 0.0f;
						}
						else {
							return 0.0f;
						}

					}

				}
				else {
					if (x[0] <= 3.64) {
						if (x[0] <= 3.56) {
							return 0.0f;
						}
						else {
							return 0.0f;
						}

					}
					else {
						if (x[0] <= 3.72) {
							return 0.0f;
						}
						else {
							if (x[0] <= 3.8) {
								return 0.0f;
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
			if (x[1] <= 0.35) {
				if (x[1] <= -0.15) {
					if (x[1] <= -0.65) {
						if (x[0] <= 3.32) {
							if (x[0] <= 3.24) {
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
						return 0.0f;
					}

				}
				else {
					if (x[0] <= 3.64) {
						if (x[0] <= 3.48) {
							if (x[1] <= 0.15) {
								return 0.0f;
							}
							else {
								if (x[0] <= 3.4) {
									if (x[0] <= 3.32) {
										return 0.0f;
									}
									else {
										if (x[1] <= 0.25) {
											return 0.0f;
										}
										else {
											return 0.0f;
										}

									}

								}
								else {
									if (x[1] <= 0.25) {
										return 0.0f;
									}
									else {
										return 0.0f;
									}

								}

							}

						}
						else {
							if (x[1] <= 0.05) {
								if (x[0] <= 3.56) {
									return 0.0f;
								}
								else {
									if (x[1] <= -0.05) {
										return 0.0f;
									}
									else {
										return 0.0f;
									}

								}

							}
							else {
								if (x[1] <= 0.25) {
									if (x[0] <= 3.56) {
										if (x[1] <= 0.15) {
											return 0.0f;
										}
										else {
											return 0.0f;
										}

									}
									else {
										if (x[1] <= 0.15) {
											return 0.0f;
										}
										else {
											return -0.6f;
										}

									}

								}
								else {
									if (x[0] <= 3.56) {
										return -0.5f;
									}
									else {
										return -3.0f;
									}

								}

							}

						}

					}
					else {
						if (x[1] <= 0.05) {
							if (x[1] <= -0.05) {
								if (x[0] <= 3.72) {
									return 0.0f;
								}
								else {
									return 0.0f;
								}

							}
							else {
								if (x[0] <= 3.72) {
									return 0.0f;
								}
								else {
									if (x[0] <= 3.8) {
										return -0.9f;
									}
									else {
										return -3.7f;
									}

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
								return -3.4f;
							}

						}

					}

				}

			}
			else {
				if (x[1] <= 0.55) {
					if (x[0] <= 3.4) {
						if (x[0] <= 3.24) {
							if (x[1] <= 0.45) {
								return 0.0f;
							}
							else {
								return 0.0f;
							}

						}
						else {
							if (x[0] <= 3.32) {
								if (x[1] <= 0.45) {
									return 0.0f;
								}
								else {
									return 0.0f;
								}

							}
							else {
								if (x[1] <= 0.45) {
									return 0.0f;
								}
								else {
									return -0.3f;
								}

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
					if (x[0] <= 3.24) {
						if (x[1] <= 0.65) {
							return 0.0f;
						}
						else {
							if (x[1] <= 0.75) {
								return -0.2f;
							}
							else {
								return -2.2f;
							}

						}

					}
					else {
						if (x[0] <= 3.32) {
							if (x[1] <= 0.65) {
								return -0.2f;
							}
							else {
								return -2.4f;
							}

						}
						else {
							return -2.5f;
						}

					}

				}

			}

		}

	}

}
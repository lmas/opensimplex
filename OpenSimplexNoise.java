/*
 * OpenSimplex (Simplectic) Noise in Java.
 * (v1.0.1 With new gradient set and corresponding normalization factor, 9/19/14)
 */

public class OpenSimplexNoise {

	private static final double STRETCH_CONSTANT_3D = -1.0 / 6;
	private static final double SQUISH_CONSTANT_3D = 1.0 / 3;
	
	private short[] perm;
	private short[] permGradIndex3D;
	
	public OpenSimplexNoise() {
		this(PERM_DEFAULT);
	}
	
	public OpenSimplexNoise(short[] perm) {
		this.perm = perm;
		permGradIndex3D = new short[256];
		for (int i = 0; i < 256; i++) {
			permGradIndex3D[i] = (short)((perm[i] % (gradients3D.length / 3)) * 3);
		}
	}
	
	//Initializes the class using a permutation array generated from a 64-bit seed.
	//Generates a proper permutation (i.e. doesn't merely perform N successive pair swaps on a base array)
	//Uses java.util.Random
	public OpenSimplexNoise(long seed) {
		perm = new short[256];
		permGradIndex3D = new short[256];
		short[] source = new short[256];
		for (short i = 0; i < 256; i++)
			source[i] = i;
		java.util.Random random = new java.util.Random(seed);
		for (int i = 255; i >= 0; i--) {
			int r = random.nextInt(i + 1);
			perm[i] = source[r];
			permGradIndex3D[i] = (short)((perm[i] % (gradients3D.length / 3)) * 3);
			source[r] = source[i];
		}
	}
	
	//3D OpenSimplex (Simplectic) Noise.
	public double eval(double x, double y, double z) {
	
		//Place input coordinates on simplectic lattice.
		double stretchOffset = (x + y + z) * STRETCH_CONSTANT_3D;
		double xs = x + stretchOffset;
		double ys = y + stretchOffset;
		double zs = z + stretchOffset;
		
		//Floor to get simplectic lattice coordinates of rhombohedron (stretched cube) super-cell origin.
		int xsb = fastFloor(xs);
		int ysb = fastFloor(ys);
		int zsb = fastFloor(zs);
		
		//Skew out to get actual coordinates of rhombohedron origin. We'll need these later.
		double squishOffset = (xsb + ysb + zsb) * SQUISH_CONSTANT_3D;
		double xb = xsb + squishOffset;
		double yb = ysb + squishOffset;
		double zb = zsb + squishOffset;
		
		//Compute simplectic lattice coordinates relative to rhombohedral origin.
		double xins = xs - xsb;
		double yins = ys - ysb;
		double zins = zs - zsb;
		
		//Sum those together to get a value that determines which cell we're in.
		double inSum = xins + yins + zins;

		//Positions relative to origin point.
		double dx0 = x - xb;
		double dy0 = y - yb;
		double dz0 = z - zb;
		
		//We'll be defining these inside the next block and using them afterwards.
		double dx_ext0, dy_ext0, dz_ext0;
		double dx_ext1, dy_ext1, dz_ext1;
		int xsv_ext0, ysv_ext0, zsv_ext0;
		int xsv_ext1, ysv_ext1, zsv_ext1;
		
		double value = 0;
		if (inSum <= 1) { //We're inside the Tetrahedron (3-Simplex) at (0,0,0)
			
			//Determine which two of (0,0,1), (0,1,0), (1,0,0) are closest.
			byte aPoint = 0x01;
			double aScore = xins;
			byte bPoint = 0x02;
			double bScore = yins;
			if (aScore >= bScore && zins > bScore) {
				bScore = zins;
				bPoint = 0x04;
			} else if (aScore < bScore && zins > aScore) {
				aScore = zins;
				aPoint = 0x04;
			}
			
			//Now we determine the two lattice points not part of the tetrahedron that may contribute.
			//This depends on the closest two tetrahedral vertices, including (0,0,0)
			double wins = 1 - inSum;
			if (wins > aScore || wins > bScore) { //(0,0,0) is one of the closest two tetrahedral vertices.
				byte c = (bScore > aScore ? bPoint : aPoint); //Our other closest vertex is the closest out of a and b.
				
				if ((c & 0x01) == 0) {
					xsv_ext0 = xsb - 1;
					xsv_ext1 = xsb;
					dx_ext0 = dx0 + 1;
					dx_ext1 = dx0;
				} else {
					xsv_ext0 = xsv_ext1 = xsb + 1;
					dx_ext0 = dx_ext1 = dx0 - 1;
				}

				if ((c & 0x02) == 0) {
					ysv_ext0 = ysv_ext1 = ysb;
					dy_ext0 = dy_ext1 = dy0;
					if ((c & 0x01) == 0) {
						ysv_ext1 -= 1;
						dy_ext1 += 1;
					} else {
						ysv_ext0 -= 1;
						dy_ext0 += 1;
					}
				} else {
					ysv_ext0 = ysv_ext1 = ysb + 1;
					dy_ext0 = dy_ext1 = dy0 - 1;
				}

				if ((c & 0x04) == 0) {
					zsv_ext0 = zsb;
					zsv_ext1 = zsb - 1;
					dz_ext0 = dz0;
					dz_ext1 = dz0 + 1;
				} else {
					zsv_ext0 = zsv_ext1 = zsb + 1;
					dz_ext0 = dz_ext1 = dz0 - 1;
				}
			} else { //(0,0,0) is not one of the closest two tetrahedral vertices.
                		byte c = (byte)(aPoint | bPoint); //Our two extra vertices are determined by the closest two.
				
				if ((c & 0x01) == 0) {
					xsv_ext0 = xsb;
					xsv_ext1 = xsb - 1;
					dx_ext0 = dx0 - 2 * SQUISH_CONSTANT_3D;
					dx_ext1 = dx0 + 1 - SQUISH_CONSTANT_3D;
				} else {
					xsv_ext0 = xsv_ext1 = xsb + 1;
					dx_ext0 = dx0 - 1 - 2 * SQUISH_CONSTANT_3D;
					dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_3D;
				}

				if ((c & 0x02) == 0) {
					ysv_ext0 = ysb;
					ysv_ext1 = ysb - 1;
					dy_ext0 = dy0 - 2 * SQUISH_CONSTANT_3D;
					dy_ext1 = dy0 + 1 - SQUISH_CONSTANT_3D;
				} else {
					ysv_ext0 = ysv_ext1 = ysb + 1;
					dy_ext0 = dy0 - 1 - 2 * SQUISH_CONSTANT_3D;
					dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_3D;
				}

				if ((c & 0x04) == 0) {
					zsv_ext0 = zsb;
					zsv_ext1 = zsb - 1;
					dz_ext0 = dz0 - 2 * SQUISH_CONSTANT_3D;
					dz_ext1 = dz0 + 1 - SQUISH_CONSTANT_3D;
				} else {
					zsv_ext0 = zsv_ext1 = zsb + 1;
					dz_ext0 = dz0 - 1 - 2 * SQUISH_CONSTANT_3D;
					dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_3D;
				}
			}

			//Contribution (0,0,0)
			double attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0;
			if (attn0 > 0) {
				attn0 *= attn0;
				value = attn0 * attn0 * extrapolate(xsb + 0, ysb + 0, zsb + 0, dx0, dy0, dz0);
			}

			//Contribution (0,0,1)
			double dx1 = dx0 - 1 - SQUISH_CONSTANT_3D;
			double dy1 = dy0 - 0 - SQUISH_CONSTANT_3D;
			double dz1 = dz0 - 0 - SQUISH_CONSTANT_3D;
			double attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1;
			if (attn1 > 0) {
				attn1 *= attn1;
				value += attn1 * attn1 * extrapolate(xsb + 1, ysb + 0, zsb + 0, dx1, dy1, dz1);
			}

			//Contribution (0,1,0)
			double dx2 = dx0 - 0 - SQUISH_CONSTANT_3D;
			double dy2 = dy0 - 1 - SQUISH_CONSTANT_3D;
			double dz2 = dz1;
			double attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2;
			if (attn2 > 0) {
				attn2 *= attn2;
				value += attn2 * attn2 * extrapolate(xsb + 0, ysb + 1, zsb + 0, dx2, dy2, dz2);
			}

			//Contribution (1,0,0)
			double dx3 = dx2;
			double dy3 = dy1;
			double dz3 = dz0 - 1 - SQUISH_CONSTANT_3D;
			double attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3;
			if (attn3 > 0) {
				attn3 *= attn3;
				value += attn3 * attn3 * extrapolate(xsb + 0, ysb + 0, zsb + 1, dx3, dy3, dz3);
			}
		} else if (inSum >= 2) { //We're inside the Tetrahedron (3-Simplex) at (1,1,1)
		
			//Determine which two tetrahedral vertices are the closest, out of (1,1,0), (1,0,1), (0,1,1) but not (1,1,1).
			byte aPoint = 0x06;
			double aScore = xins;
			byte bPoint = 0x05;
			double bScore = yins;
			if (aScore <= bScore && zins < bScore) {
				bScore = zins;
				bPoint = 0x03;
			} else if (aScore > bScore && zins < aScore) {
				aScore = zins;
				aPoint = 0x03;
			}
			
			//Now we determine the two lattice points not part of the tetrahedron that may contribute.
			//This depends on the closest two tetrahedral vertices, including (1,1,1)
			double wins = 3 - inSum;
			if (wins < aScore || wins < bScore) { //(1,1,1) is one of the closest two tetrahedral vertices.
				byte c = (bScore < aScore ? bPoint : aPoint); //Our other closest vertex is the closest out of a and b.
				
				if ((c & 0x01) != 0) {
					xsv_ext0 = xsb + 2;
					xsv_ext1 = xsb + 1;
					dx_ext0 = dx0 - 2 - 3 * SQUISH_CONSTANT_3D;
					dx_ext1 = dx0 - 1 - 3 * SQUISH_CONSTANT_3D;
				} else {
					xsv_ext0 = xsv_ext1 = xsb;
					dx_ext0 = dx_ext1 = dx0 - 3 * SQUISH_CONSTANT_3D;
				}

				if ((c & 0x02) != 0) {
					ysv_ext0 = ysv_ext1 = ysb + 1;
					dy_ext0 = dy_ext1 = dy0 - 1 - 3 * SQUISH_CONSTANT_3D;
					if ((c & 0x01) != 0) {
						ysv_ext1 += 1;
						dy_ext1 -= 1;
					} else {
						ysv_ext0 += 1;
						dy_ext0 -= 1;
					}
				} else {
					ysv_ext0 = ysv_ext1 = ysb;
					dy_ext0 = dy_ext1 = dy0 - 3 * SQUISH_CONSTANT_3D;
				}

				if ((c & 0x04) != 0) {
					zsv_ext0 = zsb + 1;
					zsv_ext1 = zsb + 2;
					dz_ext0 = dz0 - 1 - 3 * SQUISH_CONSTANT_3D;
					dz_ext1 = dz0 - 2 - 3 * SQUISH_CONSTANT_3D;
				} else {
					zsv_ext0 = zsv_ext1 = zsb;
					dz_ext0 = dz_ext1 = dz0 - 3 * SQUISH_CONSTANT_3D;
				}
			} else { //(1,1,1) is not one of the closest two tetrahedral vertices.
                		byte c = (byte)(aPoint & bPoint); //Our two extra vertices are determined by the closest two.
				
				if ((c & 0x01) != 0) {
					xsv_ext0 = xsb + 1;
					xsv_ext1 = xsb + 2;
					dx_ext0 = dx0 - 1 - SQUISH_CONSTANT_3D;
					dx_ext1 = dx0 - 2 - 2 * SQUISH_CONSTANT_3D;
				} else {
					xsv_ext0 = xsv_ext1 = xsb;
					dx_ext0 = dx0 - SQUISH_CONSTANT_3D;
					dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D;
				}

				if ((c & 0x02) != 0) {
					ysv_ext0 = ysb + 1;
					ysv_ext1 = ysb + 2;
					dy_ext0 = dy0 - 1 - SQUISH_CONSTANT_3D;
					dy_ext1 = dy0 - 2 - 2 * SQUISH_CONSTANT_3D;
				} else {
					ysv_ext0 = ysv_ext1 = ysb;
					dy_ext0 = dy0 - SQUISH_CONSTANT_3D;
					dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D;
				}

				if ((c & 0x04) != 0) {
					zsv_ext0 = zsb + 1;
					zsv_ext1 = zsb + 2;
					dz_ext0 = dz0 - 1 - SQUISH_CONSTANT_3D;
					dz_ext1 = dz0 - 2 - 2 * SQUISH_CONSTANT_3D;
				} else {
					zsv_ext0 = zsv_ext1 = zsb;
					dz_ext0 = dz0 - SQUISH_CONSTANT_3D;
					dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D;
				}
			}
			
			//Contribution (1,1,0)
			double dx3 = dx0 - 1 - 2 * SQUISH_CONSTANT_3D;
			double dy3 = dy0 - 1 - 2 * SQUISH_CONSTANT_3D;
			double dz3 = dz0 - 0 - 2 * SQUISH_CONSTANT_3D;
			double attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3;
			if (attn3 > 0) {
				attn3 *= attn3;
				value = attn3 * attn3 * extrapolate(xsb + 1, ysb + 1, zsb + 0, dx3, dy3, dz3);
			}

			//Contribution (1,0,1)
			double dx2 = dx3;
			double dy2 = dy0 - 0 - 2 * SQUISH_CONSTANT_3D;
			double dz2 = dz0 - 1 - 2 * SQUISH_CONSTANT_3D;
			double attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2;
			if (attn2 > 0) {
				attn2 *= attn2;
				value += attn2 * attn2 * extrapolate(xsb + 1, ysb + 0, zsb + 1, dx2, dy2, dz2);
			}

			//Contribution (0,1,1)
			double dx1 = dx0 - 0 - 2 * SQUISH_CONSTANT_3D;
			double dy1 = dy3;
			double dz1 = dz2;
			double attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1;
			if (attn1 > 0) {
				attn1 *= attn1;
				value += attn1 * attn1 * extrapolate(xsb + 0, ysb + 1, zsb + 1, dx1, dy1, dz1);
			}

			//Contribution (1,1,1)
			dx0 = dx0 - 1 - 3 * SQUISH_CONSTANT_3D;
			dy0 = dy0 - 1 - 3 * SQUISH_CONSTANT_3D;
			dz0 = dz0 - 1 - 3 * SQUISH_CONSTANT_3D;
			double attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0;
			if (attn0 > 0) {
				attn0 *= attn0;
				value += attn0 * attn0 * extrapolate(xsb + 1, ysb + 1, zsb + 1, dx0, dy0, dz0);
			}
		} else { //We're inside the Octahedron (Rectified 3-Simplex) in between.
			double aScore;
			byte aPoint;
			boolean aIsFurtherSide;
			double bScore;
			byte bPoint;
			boolean bIsFurtherSide;

			//Decide between point (1,0,0) and (0,1,1) as closest
			double p1 = xins + yins;
			if (p1 > 1) {
				aScore = p1 - 1;
				aPoint = 0x03;
				aIsFurtherSide = true;
			} else {
				aScore = 1 - p1;
				aPoint = 0x04;
				aIsFurtherSide = false;
			}

			//Decide between point (0,1,0) and (1,0,1) as closest
			double p2 = xins + zins;
			if (p2 > 1) {
				bScore = p2 - 1;
				bPoint = 0x05;
				bIsFurtherSide = true;
			} else {
				bScore = 1 - p2;
				bPoint = 0x02;
				bIsFurtherSide = false;
			}
			
			//The closest out of the two (0,0,1) and (1,1,0) will replace the furthest out of the two decided above, if closer.
			double p3 = yins + zins;
			if (p3 > 1) {
				double score = p3 - 1;
				if (aScore <= bScore && aScore < score) {
					aScore = score;
					aPoint = 0x06;
					aIsFurtherSide = true;
				} else if (aScore > bScore && bScore < score) {
					bScore = score;
					bPoint = 0x06;
					bIsFurtherSide = true;
				}
			} else {
				double score = 1 - p3;
				if (aScore <= bScore && aScore < score) {
					aScore = score;
					aPoint = 0x01;
					aIsFurtherSide = false;
				} else if (aScore > bScore && bScore < score) {
					bScore = score;
					bPoint = 0x01;
					bIsFurtherSide = false;
				}
			}
			
			//Where each of the two closest points are determines how the extra two vertices are calculated.
			if (aIsFurtherSide == bIsFurtherSide) {
				if (aIsFurtherSide) { //Both closest points on (1,1,1) side

					//One of the two extra points is (1,1,1)
					dx_ext0 = dx0 - 1 - 3 * SQUISH_CONSTANT_3D;
					dy_ext0 = dy0 - 1 - 3 * SQUISH_CONSTANT_3D;
					dz_ext0 = dz0 - 1 - 3 * SQUISH_CONSTANT_3D;
					xsv_ext0 = xsb + 1;
					ysv_ext0 = ysb + 1;
					zsv_ext0 = zsb + 1;

					//Other extra point is based on the shared axis.
					byte c = (byte)(aPoint & bPoint);
					if ((c & 0x01) != 0) {
						dx_ext1 = dx0 - 2 - 2 * SQUISH_CONSTANT_3D;
						dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D;
						dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D;
						xsv_ext1 = xsb + 2;
						ysv_ext1 = ysb;
						zsv_ext1 = zsb;
					} else if ((c & 0x02) != 0) {
						dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D;
						dy_ext1 = dy0 - 2 - 2 * SQUISH_CONSTANT_3D;
						dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D;
						xsv_ext1 = xsb;
						ysv_ext1 = ysb + 2;
						zsv_ext1 = zsb;
					} else {
						dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D;
						dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D;
						dz_ext1 = dz0 - 2 - 2 * SQUISH_CONSTANT_3D;
						xsv_ext1 = xsb;
						ysv_ext1 = ysb;
						zsv_ext1 = zsb + 2;
					}
				} else {//Both closest points on (0,0,0) side

					//One of the two extra points is (0,0,0)
					dx_ext0 = dx0;
					dy_ext0 = dy0;
					dz_ext0 = dz0;
					xsv_ext0 = xsb;
					ysv_ext0 = ysb;
					zsv_ext0 = zsb;

					//Other extra point is based on the omitted axis.
					byte c = (byte)(aPoint | bPoint);
					if ((c & 0x01) == 0) {
						dx_ext1 = dx0 + 1 - SQUISH_CONSTANT_3D;
						dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_3D;
						dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_3D;
						xsv_ext1 = xsb - 1;
						ysv_ext1 = ysb + 1;
						zsv_ext1 = zsb + 1;
					} else if ((c & 0x02) == 0) {
						dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_3D;
						dy_ext1 = dy0 + 1 - SQUISH_CONSTANT_3D;
						dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_3D;
						xsv_ext1 = xsb + 1;
						ysv_ext1 = ysb - 1;
						zsv_ext1 = zsb + 1;
					} else {
						dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_3D;
						dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_3D;
						dz_ext1 = dz0 + 1 - SQUISH_CONSTANT_3D;
						xsv_ext1 = xsb + 1;
						ysv_ext1 = ysb + 1;
						zsv_ext1 = zsb - 1;
					}
				}
			} else { //One point on (0,0,0) side, one point on (1,1,1) side
				byte c1, c2;
				if (aIsFurtherSide) {
					c1 = aPoint;
					c2 = bPoint;
				} else {
					c1 = bPoint;
					c2 = aPoint;
				}

				//One contribution is a permutation of (1,1,-1)
				if ((c1 & 0x01) == 0) {
					dx_ext0 = dx0 + 1 - SQUISH_CONSTANT_3D;
					dy_ext0 = dy0 - 1 - SQUISH_CONSTANT_3D;
					dz_ext0 = dz0 - 1 - SQUISH_CONSTANT_3D;
					xsv_ext0 = xsb - 1;
					ysv_ext0 = ysb + 1;
					zsv_ext0 = zsb + 1;
				} else if ((c1 & 0x02) == 0) {
					dx_ext0 = dx0 - 1 - SQUISH_CONSTANT_3D;
					dy_ext0 = dy0 + 1 - SQUISH_CONSTANT_3D;
					dz_ext0 = dz0 - 1 - SQUISH_CONSTANT_3D;
					xsv_ext0 = xsb + 1;
					ysv_ext0 = ysb - 1;
					zsv_ext0 = zsb + 1;
				} else {
					dx_ext0 = dx0 - 1 - SQUISH_CONSTANT_3D;
					dy_ext0 = dy0 - 1 - SQUISH_CONSTANT_3D;
					dz_ext0 = dz0 + 1 - SQUISH_CONSTANT_3D;
					xsv_ext0 = xsb + 1;
					ysv_ext0 = ysb + 1;
					zsv_ext0 = zsb - 1;
				}

				//One contribution is a permutation of (0,0,2)
				if ((c2 & 0x01) != 0) {
					dx_ext1 = dx0 - 2 - 2 * SQUISH_CONSTANT_3D;
					dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D;
					dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D;
					xsv_ext1 = xsb + 2;
					ysv_ext1 = ysb;
					zsv_ext1 = zsb;
				} else if ((c2 & 0x02) != 0) {
					dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D;
					dy_ext1 = dy0 - 2 - 2 * SQUISH_CONSTANT_3D;
					dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D;
					xsv_ext1 = xsb;
					ysv_ext1 = ysb + 2;
					zsv_ext1 = zsb;
				} else {
					dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D;
					dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D;
					dz_ext1 = dz0 - 2 - 2 * SQUISH_CONSTANT_3D;
					xsv_ext1 = xsb;
					ysv_ext1 = ysb;
					zsv_ext1 = zsb + 2;
				}
			}

			//Contribution (0,0,1)
			double dx1 = dx0 - 1 - SQUISH_CONSTANT_3D;
			double dy1 = dy0 - 0 - SQUISH_CONSTANT_3D;
			double dz1 = dz0 - 0 - SQUISH_CONSTANT_3D;
			double attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1;
			if (attn1 > 0) {
				attn1 *= attn1;
				value = attn1 * attn1 * extrapolate(xsb + 1, ysb + 0, zsb + 0, dx1, dy1, dz1);
			}

			//Contribution (0,1,0)
			double dx2 = dx0 - 0 - SQUISH_CONSTANT_3D;
			double dy2 = dy0 - 1 - SQUISH_CONSTANT_3D;
			double dz2 = dz1;
			double attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2;
			if (attn2 > 0) {
				attn2 *= attn2;
				value += attn2 * attn2 * extrapolate(xsb + 0, ysb + 1, zsb + 0, dx2, dy2, dz2);
			}

			//Contribution (1,0,0)
			double dx3 = dx2;
			double dy3 = dy1;
			double dz3 = dz0 - 1 - SQUISH_CONSTANT_3D;
			double attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3;
			if (attn3 > 0) {
				attn3 *= attn3;
				value += attn3 * attn3 * extrapolate(xsb + 0, ysb + 0, zsb + 1, dx3, dy3, dz3);
			}

			//Contribution (1,1,0)
			double dx4 = dx0 - 1 - 2 * SQUISH_CONSTANT_3D;
			double dy4 = dy0 - 1 - 2 * SQUISH_CONSTANT_3D;
			double dz4 = dz0 - 0 - 2 * SQUISH_CONSTANT_3D;
			double attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4;
			if (attn4 > 0) {
				attn4 *= attn4;
				value += attn4 * attn4 * extrapolate(xsb + 1, ysb + 1, zsb + 0, dx4, dy4, dz4);
			}

			//Contribution (1,0,1)
			double dx5 = dx4;
			double dy5 = dy0 - 0 - 2 * SQUISH_CONSTANT_3D;
			double dz5 = dz0 - 1 - 2 * SQUISH_CONSTANT_3D;
			double attn5 = 2 - dx5 * dx5 - dy5 * dy5 - dz5 * dz5;
			if (attn5 > 0) {
				attn5 *= attn5;
				value += attn5 * attn5 * extrapolate(xsb + 1, ysb + 0, zsb + 1, dx5, dy5, dz5);
			}

			//Contribution (0,1,1)
			double dx6 = dx0 - 0 - 2 * SQUISH_CONSTANT_3D;
			double dy6 = dy4;
			double dz6 = dz5;
			double attn6 = 2 - dx6 * dx6 - dy6 * dy6 - dz6 * dz6;
			if (attn6 > 0) {
				attn6 *= attn6;
				value += attn6 * attn6 * extrapolate(xsb + 0, ysb + 1, zsb + 1, dx6, dy6, dz6);
			}
		}
 
		//First extra vertex
		double attn_ext0 = 2 - dx_ext0 * dx_ext0 - dy_ext0 * dy_ext0 - dz_ext0 * dz_ext0;
		if (attn_ext0 > 0)
		{
			attn_ext0 *= attn_ext0;
			value += attn_ext0 * attn_ext0 * extrapolate(xsv_ext0, ysv_ext0, zsv_ext0, dx_ext0, dy_ext0, dz_ext0);
		}

		//Second extra vertex
		double attn_ext1 = 2 - dx_ext1 * dx_ext1 - dy_ext1 * dy_ext1 - dz_ext1 * dz_ext1;
		if (attn_ext1 > 0)
		{
			attn_ext1 *= attn_ext1;
			value += attn_ext1 * attn_ext1 * extrapolate(xsv_ext1, ysv_ext1, zsv_ext1, dx_ext1, dy_ext1, dz_ext1);
		}

		//Normalization constant tested using over 4 billion evaluations to bound range within [-1,1].
		//This is a safe upper bound. Actual min/max values found over the course of the 4 billion
		//evaluations were -28.12974224468639 (min) and 28.134269887817773 (max).
		return value / 28.25;
	}
	
	private double extrapolate(int xsb, int ysb, int zsb, double dx, double dy, double dz)
	{
		short index = permGradIndex3D[(perm[(perm[xsb & 0xFF] + ysb) & 0xFF] + zsb) & 0xFF];
		return gradients3D[index] * dx
			+ gradients3D[index + 1] * dy
			+ gradients3D[index + 2] * dz;
	}
	
	private static int fastFloor(double x) {
		int xi = (int)x;
		return x < xi ? xi - 1 : xi;
	}
	
	//Array of gradient values for 3D.
	//(New gradient set 9/19/14)
	private static byte[] gradients3D = new byte[] {
		 0, 3, 2,    0, 2, 3,    3, 0, 2,    2, 0, 3,   3, 2, 0,     2, 3, 0,
		 0,-3, 2,    0, 2,-3,   -3, 0, 2,    2, 0,-3,  -3, 2, 0,     2,-3, 0,
		 0, 3,-2,    0,-2, 3,    3, 0,-2,   -2, 0, 3,   3,-2, 0,    -2, 3, 0,
		 0,-3,-2,    0,-2,-3,   -3, 0,-2,   -2, 0,-3,  -3,-2, 0,    -2,-3, 0,
	};
	
	//The standardized permutation order as used in Ken Perlin's "Improved Noise"
	//(and basically every noise implementation on the Internet).
	//Also note that there's no reason this can't be a byte array other than that this is Java.
	public static final short[] PERM_DEFAULT = new short[] {
		151,160,137, 91, 90, 15,131, 13,201, 95, 96, 53,194,233,  7,225,
		140, 36,103, 30, 69,142,  8, 99, 37,240, 21, 10, 23,190,  6,148,
		247,120,234, 75,  0, 26,197, 62, 94,252,219,203,117, 35, 11, 32,
		 57,177, 33, 88,237,149, 56, 87,174, 20,125,136,171,168, 68,175,
		 74,165, 71,134,139, 48, 27,166, 77,146,158,231, 83,111,229,122,
		 60,211,133,230,220,105, 92, 41, 55, 46,245, 40,244,102,143, 54,
		 65, 25, 63,161,  1,216, 80, 73,209, 76,132,187,208, 89, 18,169,
		200,196,135,130,116,188,159, 86,164,100,109,198,173,186,  3, 64,
		 52,217,226,250,124,123,  5,202, 38,147,118,126,255, 82, 85,212,
		207,206, 59,227, 47, 16, 58, 17,182,189, 28, 42,223,183,170,213,
		119,248,152,  2, 44,154,163, 70,221,153,101,155,167, 43,172,  9,
		129, 22, 39,253, 19, 98,108,110, 79,113,224,232,178,185,112,104,
		218,246, 97,228,251, 34,242,193,238,210,144, 12,191,179,162,241,
		 81, 51,145,235,249, 14,239,107, 49,192,214, 31,181,199,106,157,
		184, 84,204,176,115,121, 50, 45,127,  4,150,254,138,236,205, 93,
		222,114, 67, 29, 24, 72,243,141,128,195, 78, 66,215, 61,156,180
	};
}
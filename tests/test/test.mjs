import * as fc from 'fast-check';

// Code under test
const contains = (text, pattern) => text.indexOf(pattern) >= 0;

	var T = 10; // Time in seconds for one breaking iteration
	var V = 0;  // Velocity (miles/second)
	var A = 0;// Altitude (miles)
	var G = 0.001;
	var L = 0; // Time (seconds)
	var S;
	var K; // Fuel Rate (LBS/SEC)
	var M = 32500; // Total weight (LBS)
	var Z = 1.8; // Fuel exhaust velocity (miles/seconds)
	var J;
	var I;

var calcFreeFall = function() {
	S = (Math.sqrt(V * V + 2 * A * G) - V) / G;
	V = V + G * S;
	L = L + S;
};

var calcNewAltitudeAndVelocity = function() {
    var Q = S * K / M;
    // New velocity based on Tsiolkovsky rocket equation.
    // Taylor series of ln(1-Q) is used.
    J = V + G * S + Z * (-Q - Q ** 2 / 2 - Q ** 3 / 3 - Q ** 4 / 4 - Q ** 5 / 5);
    // new altitude
    I = A - G * S * S / 2 - V * S + Z * S * (Q / 2 + Q ** 2 / 6 + Q ** 3 / 12 + Q ** 4 / 20 + Q ** 5 / 30);
		A = I;
		V = J;
  };

// Properties
describe('properties', () => {
  // Tests that free falling does not decrease speed
  it('Tests that free falling does not decrease speed', () => {
    fc.assert(fc.property(fc.nat(), fc.nat(), fc.nat(), (a,b,c) => {
			V = a;
			A = b;
			L = c;
			calcFreeFall();
			return (a <= (3600*V));
		}));
  });

  // Tests that time of free falling can not be negative
	it('Tests that time of free falling can not be negative', () => {
		fc.assert(fc.property(fc.nat(), fc.nat(), fc.nat(), (a,b,c) => {
			V = a;
			A = b;
			L = c;
			calcFreeFall();
			return (c <= (L+S));
		}));
	});

	// Tests that time of free falling can not increase
	it('Tests that altitude of free falling can not increase', () => {
		fc.assert(fc.property(fc.nat(), fc.nat(), fc.nat(), (a,b,c) => {
			V = a;
			A = b;
			L = c;
			calcFreeFall();
			return (b >= A);
		}));
	});

	// Checks that for positive speed the altitude should always be lowered
	it('Checks that for positive speed the altitude should always be lowered', () => {
		fc.assert(fc.property(fc.nat(), fc.nat(), fc.nat(), fc.nat(), (a,b,c,d) => {
			V = a;
			A = b;
			L = c;
			K = d;
			calcNewAltitudeAndVelocity();
			console.log(d);
	//		console.log(A);
			return (b >= A);
		}));
	});

});

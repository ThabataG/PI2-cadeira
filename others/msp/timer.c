#include <msp430.h>
 
#define RLED BIT0
#define GLED BIT6
#define BTN BIT3
#define CYCLE 0xF	// PWM frequency = SMCLK / CYCLE

// Prototypes
void timerA_config();
void port1_config();

int main() {
	WDTCTL = WDTPW + WDTHOLD; // Stop WDT
	BCSCTL1 = CALBC1_1MHZ; // Set DCO
	DCOCTL = CALDCO_1MHZ;

	timerA_config();
	port1_config();
	
	while(1);
	//_BIS_SR(LPM0_bits+GIE);
	
	return 0;
}

/*void TimerAInt(void) __attribute__((interrupt(TIMER0_A1_VECTOR)));  
void TimerAInt(void) {
	//P1OUT ^= GLED;
	// Reset interruption flag
	TA0CTL &= ~CCIFG;
}*/

void timerA_config() {
	// It's a good practice to stop timer before changing its configuration
	TACTL = MC_0;
	// Period
	TACCR0 = CYCLE-1;
	// Duty cycle
	TACCR1 = CYCLE/4;
	// Output mode 7: reset/set
	TACCTL1 = OUTMOD_7;
	//      SMCLK      /1    	upmode
	TACTL = TASSEL_2 + ID_0 + MC_1;
}

void port1_config() {
	// Initial setup
	P1DIR = RLED + GLED;
	P1SEL |= GLED;
	// Initial state of leds
	P1OUT |= RLED;
}


/* University of Brasília - Campus Gama
 * Integration Project II - 2º/2015
 *
 * This script is used to control the duty cycle of a PWM using UART.
 * Input: Character on P1.1 RX UART.
 * Output: Two PWM signals in PWM1(TA1) and PWM2(TA2) and two binary signals (SEL1 and SEL2) indicating the motors directions.
 */

// Headings
#include <msp430.h>

// Definitions
// P1
#define RLED BIT0
#define GLED BIT6
#define RXPIN BIT1
#define TXPIN BIT2
// P2
#define PWM1 BIT1
#define SEL1 BIT2
#define SEL2 BIT3
#define PWM2 BIT4
// PWM PERIOD
#define CYCLE 0x3530	// PWM frequency = SMCLK / CYCLE

// Prototypes
void timerA_config();
void uart_config();
void port1_config();
void update();
void update_right(unsigned char);
void update_left(unsigned char);

// Global variables
unsigned char rxbuf[2];

// Main
int main() {
	WDTCTL = WDTPW + WDTHOLD; // Stop WDT
	BCSCTL1 = CALBC1_16MHZ; // Set DCO
	DCOCTL = CALDCO_16MHZ;

	timerA_config();
	uart_config();
	port1_config();
	rxbuf[0] = rxbuf[1] = 0;
	
	while(1) {
		// Blink leds (swaping their states)
		P1OUT ^= RLED + GLED;

		// Enable interruption via TimerA
		//TA1CTL |= TAIE;
		//_BIS_SR(LPM0_bits+GIE);

		/*************************************************
		 Receive data and update PWM and selectors values
		*************************************************/
		// Enable interruption via UART RX
		IE2 |= UCA0RXIE;
		// Receive data and update globals
		_BIS_SR(LPM0_bits+GIE);
		_BIS_SR(LPM0_bits+GIE);
		// Update pwm duty cycles
		update();
		// Disable interruption via UART RX
		IE2 &= ~UCA0RXIE;
	}

	return 0;
}

// Timer A interruption controller
void TIMERAInt(void) __attribute__((interrupt(TIMER0_A1_VECTOR)));
void TIMERAInt(void) {
	// Disable interruption via TimerA
	//TACTL &= ~TAIE;
	// Clear TimerA interruption flag
	TA1CTL &= ~TAIFG;
	// Exit Low Power Mode 0
	LPM0_EXIT;
}

// UART RX interruption controller
void USCI0RXInt(void) __attribute__((interrupt(USCIAB0RX_VECTOR)));
void USCI0RXInt(void) {
	// Update variable 'rxbuf' saving the last received byte
	if(!rxbuf[0] && !rxbuf[1])
		rxbuf[0] = UCA0RXBUF;
	else
		rxbuf[1] = UCA0RXBUF;
	// Exit Low Power Mode 0
	LPM0_EXIT;
}

// Update motors duty cycle
void update() {
	if(rxbuf[0] & 1) {
		update_right(rxbuf[1]);
		update_left(rxbuf[0]);
	}
	else {
		update_right(rxbuf[0]);
		update_left(rxbuf[1]);
	}
	rxbuf[0] = rxbuf[1] = 0;
}

// Update right motor
void update_left(unsigned char value) {
	if(value > 127) {
		P2OUT |= SEL1;
		TA1CCR1 = (CYCLE * (2*(long long)value - 257)) / 252;
	}
	else {
		P2OUT &= ~SEL1;
		TA1CCR1 = (CYCLE * (255 - 2*(long long)value)) / 252;
	}
}

// Update left motor
void update_right(unsigned char value) {
	if(value > 126) {
		P2OUT |= SEL2;
		TA1CCR2 = (CYCLE * (2*(long long)value - 255)) / 252;
	}
	else {
		P2OUT &= ~SEL2;
		TA1CCR2 = (CYCLE * (253 - 2*(long long)value)) / 252;
	}
}

// Initialize TimerA
void timerA_config() {
	// It's a good practice to stop timer before changing its configuration
	TA1CTL = MC_0;
	// Period
	TA1CCR0 = CYCLE-1;
	// Duty cycle
	TA1CCR1 = CYCLE/4;
	TA1CCR2 = CYCLE/4;
	// Output mode 7: reset/set
	TA1CCTL1 = OUTMOD_7;
	TA1CCTL2 = OUTMOD_7;
	//      SMCLK       upmode
	TA1CTL = TASSEL_2 + MC_1;
}

// Initialize UART
void uart_config() {
	// LSB first - 8-bit data - no parity - 1 stop bit - UART - Async
	UCA0CTL0 = 0;
	// SMCLK
	UCA0CTL1 = UCSSEL_2;
	// baud rate 9600
	UCA0BR0 = 103;
	UCA0BR1 = 6;
	// First modulation stage select
	UCA0MCTL = UCBRS2+UCBRS1;
	// Disable interruption via UART RX
	IE2 &= ~UCA0RXIE;
}

// Initialize Port1
void port1_config() {
	// Initial setup
	// UART
	P1DIR = RLED + GLED + RXPIN + TXPIN;
	P1OUT = RLED;
	P1SEL = RXPIN + TXPIN;
	P1SEL2 = RXPIN + TXPIN;
	// PWM and motors control
	P2DIR = SEL1 + SEL2 + PWM1 + PWM2; 
	P2SEL = PWM1 + PWM2;
}

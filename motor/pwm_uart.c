/* University of Brasília - Campus Gama
 * Integration Project II - 2º/2015
 *
 * This script is used to control the duty cycle of a PWM using UART.
 * Input: character on RX UART
 * Output: PWM signal in P1.6 (green LED on LaunchPad)
 */

// Headings
#include <msp430.h>
 
// Definitions
#define RLED BIT0
#define GLED BIT6
#define BTN BIT3
#define RXPIN BIT1
#define TXPIN BIT2
#define CYCLE 0xF	// PWM frequency = SMCLK / CYCLE

// Prototypes
void timerA_config();
void uart_config();
void port1_config();

// Main
int main() {
	WDTCTL = WDTPW + WDTHOLD; // Stop WDT
	BCSCTL1 = CALBC1_1MHZ; // Set DCO
	DCOCTL = CALDCO_1MHZ;

	timerA_config();
	uart_config();
	port1_config();
	
	_BIS_SR(LPM0_bits+GIE);
	
	return 0;
}

// UART RX interruption controller
void USCI0RXInt(void) __attribute__((interrupt(USCIAB0RX_VECTOR)));
void USCI0RXInt(void) {
	TACCR1 = (CYCLE * UCA0RXBUF) / 255;
}

// Initialize TimerA
void timerA_config() {
	// It's a good practice to stop timer before changing its configuration
	TACTL = MC_0;
	// Period
	TACCR0 = CYCLE-1;
	// Duty cycle
	TACCR1 = CYCLE/4;
	// Output mode 7: reset/set
	TACCTL1 = OUTMOD_7;
	//      SMCLK      /1     upmode
	TACTL = TASSEL_2 + ID_0 + MC_1;
}

// Initialize UART
void uart_config() {
	// LSB first - 8-bit data - no parity - 1 stop bit - UART - Async
	UCA0CTL0 = 0;
	// SMCLK
	UCA0CTL1 = UCSSEL_2;
	// baud rate 9600
	UCA0BR0 = 6;
	UCA0BR1 = 0;
	// ?
	UCA0MCTL = UCBRF_8 + UCOS16;
	// Enable interruption via UART RX
	IE2 |= UCA0RXIE;
}

// Initialize Port1
void port1_config() {
	// Initial setup
	P1DIR = RLED + GLED;
	P1SEL = GLED + RXPIN + TXPIN;
	P1SEL2 = RXPIN + TXPIN;
	// Initial state of leds
	P1OUT = RLED;
}


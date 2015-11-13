/* University of Brasília - Campus Gama
 * Integration Project II - 2º/2015
 *
 * This script is used to control the duty cycle of a PWM using UART.
 * Input: Character on P1.1 RX UART.
 * Output: Two PWM signals in P1.0(TA1) and P1.6(TA2) -> LEDs red and green on LaunchPad.
 */

// Headings
#include <msp430.h>
 
// Definitions
#define RLED BIT0
#define RXPIN BIT1
#define TXPIN BIT2
#define BTN BIT3
#define SEL1 BIT4
#define PWM1 BIT7
#define PWM2 BIT6
#define SEL2 BIT5
#define CYCLE 0x3530	// PWM frequency = SMCLK / CYCLE

// Prototypes
void timerA_config();
void uart_config();
void port1_config();
void update_m1();
void update_m2();

// Global variables
unsigned char rxbuf;

// Main
int main() {
	WDTCTL = WDTPW + WDTHOLD; // Stop WDT
	BCSCTL1 = CALBC1_1MHZ; // Set DCO
	DCOCTL = CALDCO_1MHZ;

	timerA_config();
	uart_config();
	port1_config();
	rxbuf = '\n';
	P1OUT |= RLED;
	
	while(1) {
		// Blink red led
		P1OUT ^= RLED;
		
		// Enable interruption via TimerA
		TACTL |= TAIE;
		_BIS_SR(LPM0_bits+GIE);
		
		/*************************************************
		 Receive data and update PWM and selectors values 
		*************************************************/
		// Enable interruption via UART RX
		IE2 |= UCA0RXIE;
		// Wait the marker byte
		while(rxbuf != '\n') 
			_BIS_SR(LPM0_bits+GIE);
		// Receive data and update motor 01
		_BIS_SR(LPM0_bits+GIE);
		update_m1();
		// Receive data and update motor 02
		_BIS_SR(LPM0_bits+GIE);
		update_m2();
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
	TACTL &= ~TAIFG;
	// Exit Low Power Mode 0
	LPM0_EXIT;
}

// UART RX interruption controller
void USCI0RXInt(void) __attribute__((interrupt(USCIAB0RX_VECTOR)));
void USCI0RXInt(void) {
	// Update variable 'rxbuf' saving the last received byte
	rxbuf = UCA0RXBUF;
	// Exit Low Power Mode 0
	LPM0_EXIT;
}

// Update motor 01
void update_m1() {
	if(rxbuf > 127) {
		P1OUT |= SEL1;
		TACCR1 = (CYCLE * (2*(long long)rxbuf - 254)) / 256;	
	}
	else {
		P1OUT &= ~SEL1;
		TACCR1 = (CYCLE * (250 - 2*(long long)rxbuf)) / 250;
	}
}

// Update motor 02
void update_m2() {
	if(rxbuf >= 127) {
		P1OUT |= SEL2;
		TACCR2 = (CYCLE * (2*(long long)rxbuf - 254)) / 255;	
	}
	else {
		P1OUT &= ~SEL2;
		TACCR2 = (CYCLE * (255 - 2*(long long)rxbuf)) / 255;
	}
}

// Initialize TimerA
void timerA_config() {
	// It's a good practice to stop timer before changing its configuration
	TACTL = MC_0;
	// Period
	TACCR0 = CYCLE-1;
	// Duty cycle
	TACCR1 = CYCLE/4;
	TACCR2 = CYCLE/4;
	// Output mode 7: reset/set
	TACCTL1 = OUTMOD_7;
	TACCTL2 = OUTMOD_7;
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
	// Disable interruption via UART RX
	IE2 &= ~UCA0RXIE;
}

// Initialize Port1
void port1_config() {
	// Initial setup
	P1DIR = PWM1 + PWM2 + SEL1 + SEL2 + RLED;
	P1SEL = PWM1 + PWM2 + RXPIN + TXPIN;
	P1SEL2 = RXPIN + TXPIN;
	P1OUT &= ~RLED;
}

